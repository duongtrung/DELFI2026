#!/usr/bin/env python3
"""Validate this fixed release, including data checksums and reproducibility.

Standard library only. Deliberate future releases must update the manifest
and release-specific expectations. New code, 2026-09-11; see GPLv2 LICENSE.
"""
import csv
import hashlib
import json
import re
import tempfile
from collections import Counter
from pathlib import Path
from analyze import analyze
from prepare_data import ROOT, SCHEMAS, read_csv, parse_step

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    manifest = json.loads((ROOT / 'release-manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        path = (ROOT / item['path']).resolve()
        require(path.is_relative_to(ROOT), 'Manifest path outside repository.')
        require(path.is_file(), 'Missing file: ' + item['path'])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == item['sha256'], 'Checksum mismatch: ' + item['path'])
        require(path.stat().st_size == item['bytes'], 'File size mismatch: ' + item['path'])
    data = {}
    for name, fields in SCHEMAS.items():
        path = ROOT / 'data/prepared' / (name + '.csv')
        with path.open(newline='',encoding='utf-8') as handle:
            require(next(csv.reader(handle)) == fields, 'Unexpected schema: ' + name)
        data[name] = read_csv(path)
    ss, qq, ee = (data[k] for k in ['sessions','quiz_steps','aoi_events'])
    require([len(ss),len(qq),len(ee)] == [60,1880,92138], 'Unexpected release row counts.')
    session_map = {r['session_id']:r for r in ss}
    require(len(session_map)==60, 'Duplicate sessions.')
    require(all(re.fullmatch(r'S\d{3}',r['session_id']) for r in ss), 'Session code format.')
    require(all(not r['app_user_code'] or re.fullmatch(r'U\d{3}',r['app_user_code']) for r in ss), 'App-user code format.')
    require(sum(not r['app_user_code'] for r in ss)==1, 'Missing app-user count changed.')
    require(len({r['app_user_code'] for r in ss if r['app_user_code']})==26, 'App-user count changed.')
    require(Counter(r['phase'] for r in ss)=={'P1':24,'P2':26,'P3A':2,'P3B':8}, 'Phase counts changed.')
    quiz_map = {(r['session_id'],r['step_id']):r for r in qq}
    require(len(quiz_map)==len(qq), 'Duplicate quiz step.')
    for row in qq + ee:
        require(row['session_id'] in session_map, 'Unlinked session.')
        require(parse_step(row['step_id']) == (row['step_type'],row['text_id'],row['question_number']), 'Step parsing inconsistent.')
    require(all((int(r['points']),int(r['max_points'])) in {(0,0),(0,1),(1,1)} for r in qq), 'Unexpected scoring values.')
    require(sum(r['step_type']=='text_marker' for r in qq)==80, 'Text-marker count changed.')
    require(sum(r['max_points']=='0' and r['step_type']=='question' for r in qq)==481, 'Unscored question slots changed.')
    last, category_by_aoi = {}, {}
    for r in ee:
        sid = r['session_id']
        require((sid,r['step_id']) in quiz_map, 'Unlinked event step.')
        require(r['aoi_category'] in {'source_text','question_or_answer','unassigned'}, 'Unknown AOI category.')
        require((r['aoi_code']=='') == (r['aoi_category']=='unassigned'), 'AOI missing code/category mismatch.')
        if r['aoi_code']:
            require(re.fullmatch(r'A\d{3,}',r['aoi_code']) is not None, 'AOI code format.')
            key = (sid,r['step_id'],r['aoi_code'])
            require(key not in category_by_aoi or category_by_aoi[key]==r['aoi_category'], 'Conflicting scoped AOI category.')
            category_by_aoi[key] = r['aoi_category']
        index, start, stop, duration = [int(r[k]) for k in ['event_index','start_offset_ms','stop_offset_ms','duration_ms']]
        require(start>=0 and duration>0 and stop-start==duration, 'Invalid event interval.')
        if sid not in last:
            require(index==1 and start==0, 'Incorrect session event origin.')
        else:
            require(index==last[sid][0]+1 and start>=last[sid][1], 'Invalid event sequence.')
        last[sid]=(index,stop)
    require(len(last)==60, 'Sessions with events changed.')
    with tempfile.TemporaryDirectory() as directory:
        out = Path(directory)
        result = analyze(ROOT / 'data/prepared', out)
        require(result['complete_quiz_score_counts']=={'0':24,'1':55,'2':57,'3':269}, 'Quiz histogram changed.')
        require(result['quiz_status_counts']=={'complete':405,'partial':56,'unscored':139}, 'Quiz exclusions changed.')
        require(result['aoi_event_counts']=={'source_text':39833,'question_or_answer':10832,'unassigned':41473}, 'AOI counts changed.')
        for file in sorted(out.iterdir()):
            require(file.read_bytes()==(ROOT/'data/derived'/file.name).read_bytes(), 'Shipped derived output differs: '+file.name)
    strategy = read_csv(ROOT/'data/reported/normal_strategy_counts.csv')
    require(sum(int(r['reports']) for r in strategy)==200, 'Normal survey strategy total.')
    ratings = read_csv(ROOT/'data/reported/normal_ratings.csv')
    require(sum(int(r['group_records']) for r in ratings)==199, 'Normal rating group total.')
    matrix = read_csv(ROOT/'data/reported/instruction_strategy_counts.csv')
    require(len(matrix)==16 and sum(int(r['records']) for r in matrix)==70, 'Instruction matrix total.')
    eligible = [r for r in matrix if r['assigned_instruction'] in {'SKIM','SEQ','DEEP'}]
    require(sum(int(r['records']) for r in eligible)==55, 'Eligible instruction total.')
    require(sum(int(r['records']) for r in eligible if r['assigned_instruction']==r['reported_strategy'])==37, 'Instruction-survey matches.')
    cameras = read_csv(ROOT/'data/reported/webcam_configurations.csv')
    require(len(cameras)==8, 'Webcam configuration count.')
    minimum = sum(int(r['width_px'])>=1280 and int(r['height_px'])>=720 and int(r['frames_per_second'])>=20 for r in cameras)
    preferred = sum(int(r['width_px'])>=1920 and int(r['height_px'])>=1080 and int(r['frames_per_second'])>=25 for r in cameras)
    require((minimum,preferred)==(8,3), 'Hardware-screen counts changed.')
    print('PASS: release hashes, schemas, joins, timing, scoring, aggregate tables and reproducible outputs.')
    print('This validates file consistency, not consent, anonymity or spatial gaze accuracy.')

if __name__ == '__main__':
    main()
