#!/usr/bin/env python3
"""Reproduce pilot summaries from the prepared release, using only Python.

No original identifiers, private keys, surveys or external packages are needed.
New analysis code, 2026-09-11. See the repository GPLv2 LICENSE.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from prepare_data import ROOT, read_csv, write_csv

TEXT_FIELDS = ['session_id','app_user_code','phase','text_id','question_step_count',
               'scored_question_count','quiz_status','correct_answers','percent_correct',
               'question_event_count','question_assigned_event_count',
               'question_assigned_event_percent','question_interval_sum_ms','text_step_event_count']

def percent(numerator, denominator):
    return 100 * numerator / denominator if denominator else None

def classify_quiz(rows):
    """An unscored or absent question cannot become an incorrect answer."""
    if len({r['question_number'] for r in rows}) != len(rows):
        raise ValueError('Duplicate question in session-text block.')
    scored = [r for r in rows if int(r['max_points']) == 1]
    complete = len(rows) == 3 and {r['question_number'] for r in rows} == {'1','2','3'} and len(scored) == 3
    status = 'complete' if complete else 'partial' if scored else 'unscored'
    return status, len(scored), sum(int(r['points']) for r in scored) if complete else ''

def analyze(data_dir, out_dir):
    sessions = read_csv(data_dir / 'sessions.csv')
    quizzes = read_csv(data_dir / 'quiz_steps.csv')
    events = read_csv(data_dir / 'aoi_events.csv')
    smap = {r['session_id']: r for r in sessions}
    if len(smap) != len(sessions):
        raise ValueError('Duplicate sessions.')
    blocks, event_blocks = defaultdict(list), defaultdict(list)
    for r in quizzes:
        if r['step_type'] == 'question':
            blocks[(r['session_id'], r['text_id'])].append(r)
    for r in events:
        event_blocks[(r['session_id'], r['text_id'])].append(r)
    text_rows = []
    for (session, text), rows in sorted(blocks.items(), key=lambda item:(item[0][0],int(item[0][1][1:]))):
        status, scored_count, correct = classify_quiz(rows)
        qevents = [r for r in event_blocks[(session,text)] if r['step_type'] == 'question']
        tevents = [r for r in event_blocks[(session,text)] if r['step_type'] == 'text_marker']
        assigned = sum(r['aoi_category'] != 'unassigned' for r in qevents)
        text_rows.append(dict(session_id=session, app_user_code=smap[session]['app_user_code'],
            phase=smap[session]['phase'], text_id=text, question_step_count=len(rows),
            scored_question_count=scored_count, quiz_status=status, correct_answers=correct,
            percent_correct=round(100*correct/3, 6) if status == 'complete' else '',
            question_event_count=len(qevents), question_assigned_event_count=assigned,
            question_assigned_event_percent=round(100*assigned/len(qevents),6) if qevents else '',
            question_interval_sum_ms=sum(int(r['duration_ms']) for r in qevents),
            text_step_event_count=len(tevents)))
    write_csv(out_dir / 'session_text_summary.csv', TEXT_FIELDS, text_rows)
    categories = Counter(r['aoi_category'] for r in events)
    categories_rows = [dict(category=k, events=categories[k], percent_of_all_events=round(100*categories[k]/len(events),6) if events else '')
                       for k in ['source_text','question_or_answer','unassigned']]
    write_csv(out_dir / 'aoi_assignment_counts.csv', list(categories_rows[0]), categories_rows)
    complete = [r for r in text_rows if r['quiz_status'] == 'complete']
    histogram = Counter(r['correct_answers'] for r in complete)
    histogram_rows = [dict(correct_answers=k,complete_quizzes=histogram[k]) for k in range(4)]
    write_csv(out_dir / 'complete_quiz_scores.csv', list(histogram_rows[0]), histogram_rows)
    phase_rows = []
    for phase in ['P1','P2','P3A','P3B']:
        ss = [r for r in sessions if r['phase'] == phase]
        ee = [r for r in events if smap[r['session_id']]['phase'] == phase]
        tt = [r for r in text_rows if r['phase'] == phase]
        status = Counter(r['quiz_status'] for r in tt)
        phase_rows.append(dict(phase=phase,sessions=len(ss),
            distinct_nonmissing_app_ids=len({r['app_user_code'] for r in ss if r['app_user_code']}),
            sessions_without_app_id=sum(not r['app_user_code'] for r in ss),
            events=len(ee),question_events=sum(r['step_type']=='question' for r in ee),
            text_marker_events=sum(r['step_type']=='text_marker' for r in ee),
            session_text_blocks=len(tt),complete_quizzes=status['complete'],
            partial_quizzes=status['partial'],unscored_quizzes=status['unscored']))
    write_csv(out_dir / 'phase_summary.csv', list(phase_rows[0]), phase_rows)
    status_counts = dict(Counter(r['quiz_status'] for r in text_rows))
    result = dict(sessions=len(sessions), distinct_nonmissing_app_ids=len({r['app_user_code'] for r in sessions if r['app_user_code']}),
        sessions_without_app_id=sum(not r['app_user_code'] for r in sessions),
        quiz_step_rows=len(quizzes), question_step_rows=sum(r['step_type']=='question' for r in quizzes),
        text_marker_rows=sum(r['step_type']=='text_marker' for r in quizzes), event_rows=len(events),
        session_text_blocks=len(text_rows), quiz_status_counts=status_counts,
        complete_quiz_score_counts={str(k):histogram[k] for k in range(4)},
        complete_quiz_perfect_percent=percent(histogram[3],len(complete)),
        aoi_event_counts=dict(categories),
        assigned_event_percent=percent(len(events)-categories['unassigned'],len(events)),
        phase_summary=phase_rows)
    (out_dir / 'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    def display_percent(value):
        return f'{value:.1f}%' if value is not None else 'not estimable (zero denominator)'
    report = f'''# Reproduced application results

Generated by `python scripts/analyze.py`. These are application exports across
all conditions, not the 200 normal-reading survey records. Every event has equal
weight in the AOI percentages. No event-duration or gaze-quality filter is used.

## How much data?

{result['sessions']} sessions, {result['distinct_nonmissing_app_ids']} distinct nonmissing application IDs,
and {result['sessions_without_app_id']} sessions with no application ID.
Sessions are attempts; neither count proves the number of people.
There are {result['quiz_step_rows']:,} step rows: {result['question_step_rows']:,} question rows
and {result['text_marker_rows']:,} text-marker rows.

## Complete quizzes

A complete quiz has Q1, Q2 and Q3, each recorded once with maximum points = 1.
Each correct answer earns one point. Of {len(text_rows)} session-text blocks,
{len(complete)} are complete, {status_counts.get('partial',0)} have only some scored questions
and {status_counts.get('unscored',0)} have no scored questions. The last two
groups are retained in the dataset but excluded from the complete-quiz histogram.

| Correct answers | Complete quizzes |
|---|---:|
| 0 out of 3 | {histogram[0]} |
| 1 out of 3 | {histogram[1]} |
| 2 out of 3 | {histogram[2]} |
| 3 out of 3 | {histogram[3]} |

Perfect quizzes / complete quizzes = {histogram[3]} / {len(complete)};
percentage = **{display_percent(result['complete_quiz_perfect_percent'])}**.
The maximum score is the ceiling.
Many scores at that maximum make it hard to distinguish students' performance.
This does not establish why the scores were high or compare reading conditions
causally. A two-out-of-two partial record does not mean three-out-of-three.

## Software AOI assignments

| Category | Events | Percentage of all {len(events):,} events |
|---|---:|---:|
| Source text | {categories['source_text']:,} | {display_percent(percent(categories['source_text'],len(events)))} |
| Question or answer | {categories['question_or_answer']:,} | {display_percent(percent(categories['question_or_answer'],len(events)))} |
| Unassigned | {categories['unassigned']:,} | {display_percent(percent(categories['unassigned'],len(events)))} |

Assigned events / all events = ({categories['source_text']:,} + {categories['question_or_answer']:,}) / {len(events):,};
percentage = **{display_percent(result['assigned_event_percent'])}**.
This measures software assignment coverage. It is not gaze accuracy, percentage
of reading time, or strategy-recognition accuracy. Unassigned events cannot be
attributed uniquely to inattention, tracking problems or gaze outside labelled areas.

## Coverage by condition

| Export phase | Sessions | Events | Complete quizzes |
|---|---:|---:|---:|
'''
    for r in phase_rows:
        report += f"| {r['phase']} | {r['sessions']} | {r['events']:,} | {r['complete_quizzes']} |\n"
    report += '''
Phase definitions: P1 = instructed reading; P2 = normal reading; P3A = read-to-test;
P3B = read-to-learn. These are labels in the export, interpreted using the protocol
and reports. They do not independently verify the interface or participant compliance.
See [study guide](../../docs/study-guide.md) and [limitations](../../docs/limitations-and-next-study.md).
'''
    (out_dir / 'RESULTS.md').write_text(report,encoding='utf-8')
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=ROOT / 'data/prepared')
    parser.add_argument('--out-dir',type=Path,default=ROOT / 'data/derived')
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=True)
    result = analyze(args.data_dir,args.out_dir)
    print(json.dumps({k:v for k,v in result.items() if k!='phase_summary'},indent=2))

if __name__ == '__main__':
    main()
