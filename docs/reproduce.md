# Reproduce the results, step by step

## 1. Look at the prepared data

The CSV files are ordinary UTF-8 text and can be opened in a spreadsheet or
read with Python. No account, API key or original source files are needed to
reproduce the released application summaries.

Use Python 3.10 or later. Run commands from the top-level repository folder.
No third-party Python packages are required.

```bash
python scripts/validate_release.py
python scripts/analyze.py
```

The validator checks schemas, file hashes, row counts, joins, event timing,
quiz exclusions and reported-table totals. It recalculates the application
outputs in a temporary folder and compares them with the shipped outputs.
The analysis command writes CSV summaries, JSON totals and a readable
`data/derived/RESULTS.md`. It never modifies `data/prepared/` or `data/reported/`.

Expected application totals: **60 sessions; 1,880 step rows; 92,138 events;
600 session-text blocks; 405 complete scored quizzes**. Expected histogram:
24, 55, 57 and 269 quizzes with respectively zero, one, two and three correct
answers. These count quizzes, not unique students.

## 2. Understand a quiz through an example

The following is an invented example, not a participant record:

| Question | Correct? | Earned points | Maximum points |
|---|---|---:|---:|
| Q1 | Yes | 1 | 1 |
| Q2 | No | 0 | 1 |
| Q3 | Yes | 1 | 1 |

Add the earned points: 1 + 0 + 1 = **two correct answers out of three**.
The equivalent percentage is 2 ÷ 3 × 100 = **66.7%**. The released summary
keeps both `correct_answers = 2` and `percent_correct = 66.666667`. There is
no continuous comprehension measurement between those three question outcomes.

The original data include question slots with `max_points = 0`. Such slots
are **unscored**. A stored zero in this case does not establish an incorrect
answer. The export does not explain whether the question was unanswered,
skipped or affected by another application state. The pipeline therefore:

1. Groups question steps by session and text.
2. Checks Q1, Q2 and Q3 occur exactly once.
3. Requires every question to have `max_points = 1` for a complete quiz.
4. Sums earned points only for that complete quiz summary.

All 600 blocks in this release have three question slots, but only 405 have
three **scored** slots. The remaining 56 partially scored and 139 unscored
blocks stay in `session_text_summary.csv` with blank complete-quiz scores.
A two-out-of-two scored partial record is not counted as three-out-of-three.

## 3. Understand the two AOI categories

AOI means **area of interest**, a label attached to displayed material. In the
original export, labels starting with `s:` were interpreted as source text and
labels starting with `q:` as question/answer material. The release replaces
these strings with `source_text` and `question_or_answer`. Missing assignments
become `unassigned`.

Count 39,833 source-text events and 10,832 question/answer events. Together,
50,665 events have a label. Divide 50,665 by all 92,138 events and multiply by
100: **55.0% assignment coverage**.

This computation gives the same weight to a 50 ms event and a 500 ms event.
It is therefore not a duration share. Nor is the result a spatial accuracy
score: a software assignment may be inaccurate. The unassigned group could
include gaze outside labelled areas or tracking/mapping problems.

`aoi_code` preserves repeated hits to the same exported software AOI within a
single session-step, without publishing its word string. Use the compound key
`session_id + step_id + aoi_code`; never compare `A001` alone across screens.
AOI repeats do not independently establish rereading or regressions.

## 4. Analyze normal-reading sessions only

The released session table marks normal reading as `phase = P2`. For example:

```python
import csv
from collections import Counter

with open('data/prepared/sessions.csv', newline='', encoding='utf-8') as f:
    sessions = list(csv.DictReader(f))
normal_ids = {r['session_id'] for r in sessions if r['phase'] == 'P2'}
with open('data/prepared/aoi_events.csv', newline='', encoding='utf-8') as f:
    counts = Counter(r['aoi_category'] for r in csv.DictReader(f)
                     if r['session_id'] in normal_ids)
print(len(normal_ids))       # 26 application sessions
print(sum(counts.values()))  # 30,228 recorded events
print(counts)
```

This selects 26 normal-reading **application sessions**. It does not recover
the paper's exact twenty survey participants, because the necessary matched
survey data and identity mapping are absent. Multiple sessions or texts from
one app ID are not independent people.

## 5. Inspect the reported survey calculations

The tables in `data/reported/` are transcribed aggregates. You can verify the
strategy totals and reproduce the instruction–survey match calculation, but
cannot reconstruct individual responses or recalculate rating means.

For the normal-reading means, the difference between displayed hard-text and
easy-text effort is 3.03 − 2.57 = **0.46 points on the 1–5 scale**. This uses
rounded reported means and is descriptive; it is not a significance test.

## 6. Rebuild minimized files from the private originals (maintainers)

Most readers can skip this section. The original CSV filenames are listed in
`scripts/prepare_data.py` and the source register. Keep them outside the repo.

```bash
python scripts/prepare_data.py --raw-dir ../private-originals --private-key-file ../private-release/key.bin
python scripts/analyze.py
```

The script creates a private random key if one does not exist and uses it to
assign opaque session and app-user codes. The same originals and key reproduce
the same codes; a new key changes codes but preserves aggregate results. No
identity mapping or key is included in the public candidate. The input files
are read only. The packaged dataset itself is sufficient for all published
application calculations; reproducing its byte-identical pseudonyms from
original IDs additionally needs the original private key.

All input rows are retained. Calendar timestamps, browser strings, exact
viewports, original IDs and AOI word strings are omitted. Relative event
times are rebased to the first event of each session, preserving intervals,
gaps and ordering. This origin is not the session start or reading onset.
The preparation is a minimization step, not proof of anonymous data.

For an intentional future dataset update, regenerate data hashes in
`release-manifest.json`, update expected release-specific totals in
`validate_release.py`, and issue a new version with a change log. Do not
silently replace the current release's source files or expected counts.

## 7. Check the analysis behavior

```bash
python -m unittest discover -s tests -v
```

Tests use explicitly invented records. They check that missing/unscored
questions are not treated as wrong answers, duplicate question rows fail,
AOI codes remain scoped correctly, and transformations preserve useful links
without copying original identifiers into the prepared schema.
