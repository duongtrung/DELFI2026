#!/usr/bin/env python3
"""Prepare minimized application exports. Python standard library only.

Original files and a private pseudonymization key must remain outside this
repository. This script does not establish consent or anonymous data status.
New analysis code, 2026-09-11. See the repository GPLv2 LICENSE.
"""
import argparse
import csv
import hashlib
import hmac
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILES = {
    'sessions': 'bf1f096f-8713-45eb-918c-998ce3501ce9.csv',
    'quiz_steps': '75263db0-d740-4af3-8a2a-70927758a315.csv',
    'aoi_events': 'd60e873e-b56d-4538-b833-5e95d3b86d7b.csv',
}
SCHEMAS = {
    'sessions': ['session_id', 'app_user_code', 'phase'],
    'quiz_steps': ['session_id', 'step_id', 'step_type', 'text_id',
                   'question_number', 'points', 'max_points'],
    'aoi_events': ['session_id', 'event_index', 'step_id', 'step_type', 'text_id',
                   'question_number', 'aoi_category', 'aoi_code',
                   'start_offset_ms', 'stop_offset_ms', 'duration_ms'],
}

def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))

def write_csv(path, fields, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

def parse_step(step):
    match = re.fullmatch(r'(T\d+)_Q([123])', step)
    if match:
        return 'question', match[1], match[2]
    match = re.fullmatch(r'Text (\d+)', step)
    if match:
        return 'text_marker', 'T' + match[1], ''
    raise ValueError('Unexpected step label: release requires author review.')

def is_missing(value):
    return value.strip().lower() in {'', 'null', 'nan', 'na', 'n/a', 'none'}

def pseudonyms(values, key, domain, prefix):
    # Keyed ordering avoids exposing original CSV ordering or original IDs.
    ordered = sorted(set(values), key=lambda value: hmac.new(
        key, (domain + ':' + value).encode(), hashlib.sha256).digest())
    return {value: f'{prefix}{i:03d}' for i, value in enumerate(ordered, 1)}

def prepare(raw_dir, output_dir, key):
    raw = {name: read_csv(raw_dir / filename) for name, filename in RAW_FILES.items()}
    sessions, quizzes, events = (raw[n] for n in ('sessions', 'quiz_steps', 'aoi_events'))
    for rows in raw.values():
        if len({r['id'] for r in rows}) != len(rows):
            raise ValueError('Duplicate original row identifiers.')
    session_ids = {r['id'] for r in sessions}
    if any(r['trial_id'] not in session_ids for r in quizzes + events):
        raise ValueError('Unlinked session identifier.')
    if any(r['phase'] not in {'P1', 'P2', 'P3A', 'P3B'} for r in sessions):
        raise ValueError('Unknown phase.')
    quiz_keys = {(r['trial_id'], r['step_id']) for r in quizzes}
    if len(quiz_keys) != len(quizzes):
        raise ValueError('Duplicate session-step quiz records.')
    if any((r['trial_id'], r['step_id']) not in quiz_keys for r in events):
        raise ValueError('Event does not match a quiz or text-marker step.')
    smap = pseudonyms(session_ids, key, 'session', 'S')
    users = [r['user_id'] for r in sessions if not is_missing(r['user_id'])]
    umap = pseudonyms(users, key, 'app_user', 'U')
    prepared_sessions = sorted([
        {'session_id': smap[r['id']], 'app_user_code': umap.get(r['user_id'], ''),
         'phase': r['phase']} for r in sessions], key=lambda r: r['session_id'])
    prepared_quizzes = []
    for r in quizzes:
        kind, text, question = parse_step(r['step_id'])
        points, maximum = int(r['points']), int(r['max_points'])
        if (points, maximum) not in {(0, 0), (0, 1), (1, 1)}:
            raise ValueError('Unexpected scoring values.')
        prepared_quizzes.append(dict(session_id=smap[r['trial_id']],
            step_id=r['step_id'], step_type=kind, text_id=text,
            question_number=question, points=points, max_points=maximum))
    prepared_quizzes.sort(key=lambda r: (r['session_id'], int(r['text_id'][1:]),
                                        r['step_type'], r['question_number']))
    grouped = defaultdict(list)
    for r in events:
        grouped[r['trial_id']].append(r)
    prepared_events = []
    for original_session in sorted(grouped, key=smap.get):
        rows = sorted(grouped[original_session], key=lambda r: int(r['start_ts']))
        origin = int(rows[0]['start_ts'])
        aoi_maps, labels = defaultdict(dict), {}
        previous_stop = -1
        for i, r in enumerate(rows, 1):
            start, stop = int(r['start_ts']), int(r['stop_ts'])
            if stop <= start or start < previous_stop:
                raise ValueError('Nonpositive or overlapping event interval.')
            previous_stop = stop
            kind, text, question = parse_step(r['step_id'])
            if is_missing(r['aoi']):
                if r['aoi_id'] != '-1':
                    raise ValueError('Unexpected missing AOI sentinel.')
                category, code = 'unassigned', ''
            else:
                category = {'s:': 'source_text', 'q:': 'question_or_answer'}.get(r['aoi'][:2])
                if category is None or r['aoi_id'] == '-1':
                    raise ValueError('Unexpected AOI label or identifier.')
                scope = (r['step_id'], r['aoi_id'])
                if scope in labels and labels[scope] != r['aoi']:
                    raise ValueError('AOI ID has conflicting labels within one session-step.')
                labels[scope] = r['aoi']
                local = aoi_maps[r['step_id']]
                if r['aoi_id'] not in local:
                    local[r['aoi_id']] = f'A{len(local) + 1:03d}'
                code = local[r['aoi_id']]
            prepared_events.append(dict(session_id=smap[original_session], event_index=i,
                step_id=r['step_id'], step_type=kind, text_id=text, question_number=question,
                aoi_category=category, aoi_code=code, start_offset_ms=start-origin,
                stop_offset_ms=stop-origin, duration_ms=stop-start))
    for name, rows in [('sessions', prepared_sessions), ('quiz_steps', prepared_quizzes),
                       ('aoi_events', prepared_events)]:
        write_csv(output_dir / (name + '.csv'), SCHEMAS[name], rows)
    return {'sessions': len(prepared_sessions), 'quiz_steps': len(prepared_quizzes),
            'aoi_events': len(prepared_events), 'distinct_nonmissing_app_ids': len(umap),
            'sessions_without_app_id': sum(not r['app_user_code'] for r in prepared_sessions)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-dir', required=True, type=Path)
    parser.add_argument('--private-key-file', required=True, type=Path)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'data/prepared')
    args = parser.parse_args()
    for private_path in (args.raw_dir, args.private_key_file):
        if private_path.resolve().is_relative_to(ROOT):
            parser.error('Original exports and the private key must stay outside the repository.')
    key_path = args.private_key_file
    if not key_path.exists():
        import secrets
        key_path.parent.mkdir(parents=True, exist_ok=True)
        with key_path.open('xb') as handle:
            handle.write(secrets.token_bytes(32))
        key_path.chmod(0o600)
    key = key_path.read_bytes()
    if len(key) < 32:
        parser.error('Private key must contain at least 32 bytes.')
    result = prepare(args.raw_dir, args.output_dir, key)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
