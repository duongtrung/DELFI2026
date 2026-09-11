"""Research-critical scoring, join and pseudonymization checks.

Fixtures are invented. No participant records, original identifiers or private
mapping keys are included. Run: python -m unittest discover -s tests -v
"""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import analyze
import prepare_data


def question(number, points=1, maximum=1):
    return {'question_number': str(number), 'points': str(points),
            'max_points': str(maximum)}


class QuizScoringTests(unittest.TestCase):
    def test_three_scored_questions_can_form_a_complete_quiz(self):
        self.assertEqual(analyze.classify_quiz([
            question(1), question(2, 0), question(3)]), ('complete', 3, 2))

    def test_two_out_of_two_is_not_a_perfect_complete_quiz(self):
        self.assertEqual(analyze.classify_quiz([
            question(1), question(2)]), ('partial', 2, ''))

    def test_unscored_third_slot_is_not_an_incorrect_answer(self):
        self.assertEqual(analyze.classify_quiz([
            question(1), question(2), question(3, 0, 0)]), ('partial', 2, ''))

    def test_all_unscored_slots_do_not_form_a_zero_score(self):
        self.assertEqual(analyze.classify_quiz([
            question(i, 0, 0) for i in (1, 2, 3)]), ('unscored', 0, ''))

    def test_duplicate_question_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate question'):
            analyze.classify_quiz([question(1), question(1), question(3)])


class PreparedDataTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raw_dir = Path(self.tmp.name) / 'private-input'
        self.prepared_dir = Path(self.tmp.name) / 'prepared'
        self.derived_dir = Path(self.tmp.name) / 'derived'
        self.raw_dir.mkdir()
        self.derived_dir.mkdir()
        self.sessions = [
            {'id': 'fixture-session-alpha', 'user_id': 'fixture-reader', 'phase': 'P1'},
            {'id': 'fixture-session-beta', 'user_id': 'fixture-reader', 'phase': 'P2'},
            {'id': 'fixture-session-gamma', 'user_id': 'NULL', 'phase': 'P3A'},
            {'id': 'fixture-session-delta', 'user_id': '', 'phase': 'P3B'},
        ]
        self.quizzes = []
        for session in self.sessions:
            # One complete block, one partial block, two unscored blocks.
            for number in (1, 2, 3):
                scored = session['phase'] == 'P1' or (
                    session['phase'] == 'P2' and number < 3)
                self.quizzes.append({
                    'id': 'fixture-quiz-' + str(len(self.quizzes)),
                    'trial_id': session['id'], 'step_id': f'T1_Q{number}',
                    'points': '1' if scored else '0',
                    'max_points': '1' if scored else '0',
                })
        self.events = []
        self.add_event('fixture-session-alpha', 'T1_Q1', 's:fixtureA', '41', 1000, 1050)
        self.add_event('fixture-session-alpha', 'T1_Q1', 's:fixtureB', '42', 1100, 1140)
        self.add_event('fixture-session-alpha', 'T1_Q1', 's:fixtureA', '41', 1200, 1250)
        # Original AOI 41 is reused with a different label on a different screen.
        self.add_event('fixture-session-alpha', 'T1_Q2', 'q:fixtureC', '41', 1500, 1580)
        # It is also reused with a different label in a different session.
        self.add_event('fixture-session-beta', 'T1_Q1', 's:fixtureD', '41', 2000, 2060)
        self.add_event('fixture-session-gamma', 'T1_Q1', '', '-1', 3000, 3070)
        self.add_event('fixture-session-delta', 'T1_Q1', 'NULL', '-1', 4000, 4040)

    def add_event(self, session, step, aoi, aoi_id, start, stop):
        self.events.append({
            'id': 'fixture-event-' + str(len(self.events)), 'trial_id': session,
            'step_id': step, 'aoi': aoi, 'aoi_id': aoi_id,
            'start_ts': str(start), 'stop_ts': str(stop),
        })

    def prepare(self):
        for name, rows in [('sessions', self.sessions), ('quiz_steps', self.quizzes),
                           ('aoi_events', self.events)]:
            prepare_data.write_csv(self.raw_dir / prepare_data.RAW_FILES[name],
                                   list(rows[0]), rows)
        # Synthetic test key, never used to prepare research data.
        return prepare_data.prepare(self.raw_dir, self.prepared_dir,
                                    b'fixture-only-key-not-for-research!!')

    def prepared(self, name):
        return prepare_data.read_csv(self.prepared_dir / (name + '.csv'))

    def test_missing_users_remain_missing_and_repeated_known_user_links_survive(self):
        result = self.prepare()
        by_phase = {r['phase']: r for r in self.prepared('sessions')}
        self.assertEqual(result['distinct_nonmissing_app_ids'], 1)
        self.assertEqual(result['sessions_without_app_id'], 2)
        self.assertTrue(by_phase['P1']['app_user_code'])
        self.assertEqual(by_phase['P1']['app_user_code'], by_phase['P2']['app_user_code'])
        self.assertEqual(by_phase['P3A']['app_user_code'], '')
        self.assertEqual(by_phase['P3B']['app_user_code'], '')

    def test_aoi_identity_is_local_to_session_and_step(self):
        self.prepare()
        sessions = {r['phase']: r['session_id'] for r in self.prepared('sessions')}
        events = self.prepared('aoi_events')
        primary = [r for r in events if r['session_id'] == sessions['P1']]
        self.assertEqual(primary[0]['aoi_code'], primary[2]['aoi_code'])
        self.assertNotEqual(primary[0]['aoi_code'], primary[1]['aoi_code'])
        # Local A001 is reused, but these are three different compound identities.
        chosen = [primary[0], primary[3],
                  next(r for r in events if r['session_id'] == sessions['P2'])]
        self.assertEqual({r['aoi_code'] for r in chosen}, {'A001'})
        self.assertEqual(len({(r['session_id'], r['step_id'], r['aoi_code'])
                              for r in chosen}), 3)
        self.assertTrue(all(r['aoi_code'] == '' for r in events
                            if r['aoi_category'] == 'unassigned'))

    def test_offsets_keep_durations_and_gaps_without_original_clock_origin(self):
        self.prepare()
        session = next(r['session_id'] for r in self.prepared('sessions')
                       if r['phase'] == 'P1')
        rows = [r for r in self.prepared('aoi_events') if r['session_id'] == session]
        self.assertEqual([int(r['event_index']) for r in rows], [1, 2, 3, 4])
        self.assertEqual([int(r['start_offset_ms']) for r in rows], [0, 100, 200, 500])
        self.assertEqual([int(r['duration_ms']) for r in rows], [50, 40, 50, 80])
        self.assertEqual(int(rows[1]['start_offset_ms']) - int(rows[0]['stop_offset_ms']), 50)

    def test_end_to_end_histogram_excludes_partial_and_unscored_blocks(self):
        self.prepare()
        result = analyze.analyze(self.prepared_dir, self.derived_dir)
        self.assertEqual(result['quiz_status_counts'], {
            'complete': 1, 'partial': 1, 'unscored': 2})
        self.assertEqual(result['complete_quiz_score_counts'], {'0': 0, '1': 0, '2': 0, '3': 1})
        summaries = prepare_data.read_csv(self.derived_dir / 'session_text_summary.csv')
        partial = next(r for r in summaries if r['phase'] == 'P2')
        self.assertEqual(partial['scored_question_count'], '2')
        self.assertEqual(partial['correct_answers'], '')
        self.assertEqual(partial['percent_correct'], '')
        for row in summaries:
            if row['phase'] in {'P3A', 'P3B'}:
                self.assertEqual(row['quiz_status'], 'unscored')
                self.assertEqual(row['correct_answers'], '')

    def test_all_unscored_data_has_no_estimated_perfect_percentage(self):
        session = 'fixture-session-gamma'
        self.sessions = [r for r in self.sessions if r['id'] == session]
        self.quizzes = [r for r in self.quizzes if r['trial_id'] == session]
        self.events = [r for r in self.events if r['trial_id'] == session]
        self.prepare()
        result = analyze.analyze(self.prepared_dir, self.derived_dir)
        self.assertEqual(result['sessions'], 1)
        self.assertEqual(result['quiz_status_counts'], {'unscored': 1})
        self.assertIsNone(result['complete_quiz_perfect_percent'])
        self.assertEqual(sum(result['complete_quiz_score_counts'].values()), 0)
        written = json.loads((self.derived_dir / 'summary.json').read_text())
        self.assertIsNone(written['complete_quiz_perfect_percent'])
        report = (self.derived_dir / 'RESULTS.md').read_text()
        self.assertIn('1 sessions, 0 distinct nonmissing application IDs', report)
        self.assertNotIn('60 sessions', report)
        self.assertIn('| 3 out of 3 | 0 |', report)
        self.assertIn('not estimable (zero denominator)', report)

    def test_empty_inputs_produce_empty_summary_and_unestimated_percentages(self):
        for name, fields in prepare_data.SCHEMAS.items():
            prepare_data.write_csv(self.prepared_dir / (name + '.csv'), fields, [])
        result = analyze.analyze(self.prepared_dir, self.derived_dir)
        self.assertEqual(result['sessions'], 0)
        self.assertEqual(result['session_text_blocks'], 0)
        self.assertEqual(result['event_rows'], 0)
        self.assertIsNone(result['complete_quiz_perfect_percent'])
        self.assertIsNone(result['assigned_event_percent'])
        self.assertEqual(prepare_data.read_csv(
            self.derived_dir / 'session_text_summary.csv'), [])
        categories = prepare_data.read_csv(self.derived_dir / 'aoi_assignment_counts.csv')
        self.assertEqual(len(categories), 3)
        self.assertTrue(all(r['events'] == '0' and r['percent_of_all_events'] == ''
                            for r in categories))
        report = (self.derived_dir / 'RESULTS.md').read_text()
        self.assertIn('0 sessions, 0 distinct nonmissing application IDs', report)
        self.assertIn('Percentage of all 0 events', report)
        self.assertIn('not estimable (zero denominator)', report)

    def test_duplicate_original_row_identifier_is_rejected(self):
        self.events.append(dict(self.events[0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate original row'):
            self.prepare()

    def test_duplicate_session_step_with_a_new_row_id_is_rejected(self):
        duplicate = dict(self.quizzes[0], id='fixture-other-row')
        self.quizzes.append(duplicate)
        with self.assertRaisesRegex(ValueError, 'Duplicate session-step'):
            self.prepare()

    def test_conflicting_aoi_label_in_same_session_step_is_rejected(self):
        self.events[2]['aoi'] = 's:fixtureConflict'
        with self.assertRaisesRegex(ValueError, 'conflicting labels'):
            self.prepare()

    def test_event_without_a_matching_step_is_rejected(self):
        self.events[0]['step_id'] = 'T99_Q1'
        with self.assertRaisesRegex(ValueError, 'does not match'):
            self.prepare()

    def test_overlapping_event_interval_is_rejected(self):
        self.events[1]['start_ts'] = '1040'
        with self.assertRaisesRegex(ValueError, 'overlapping event interval'):
            self.prepare()


if __name__ == '__main__':
    unittest.main()
