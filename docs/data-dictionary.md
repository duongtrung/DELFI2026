# Data dictionary

The release uses three levels of data:

- **`data/prepared/`** contains pseudonymized application records, with direct
  identifiers and unnecessary device/session metadata removed.
- **`data/reported/`** contains small aggregate tables transcribed from the
  supplied reports. These are not recovered participant-level survey data.
- **`data/derived/`** contains summaries regenerated from the prepared files
  by `python scripts/analyze.py`.

CSV files use UTF-8 text and a header row. Numeric types below describe how
values should be read; CSV itself stores text. A blank field means missing or
not applicable as described for that column. **Do not replace every blank
with zero.**

## How the files connect

`sessions.csv` has one row per application session. Its `session_id` joins to
both other prepared files. A question or text-marker screen is identified by
**`session_id` + `step_id`**. A quiz about one text is identified by
**`session_id` + `text_id`**.

The `app_user_code` connects repeated sessions that had the same nonmissing
original app user ID. It is not a verified survey participant ID, and there
is no released app–survey join. Blank user codes must remain missing; they do
not all denote an extra shared participant.

## `data/prepared/sessions.csv`

**Unit:** one application session. **Rows:** 60. **Unique key:** `session_id`.

| Column | Type / values | Meaning |
|---|---|---|
| `session_id` | String, `S` followed by three digits | New release identifier for a session. Numbers do not encode collection order or identity. |
| `app_user_code` | String, `U` followed by three digits, or blank | New code for a nonmissing original app user ID. There are 26 distinct nonmissing codes; one session has no code. This is not independently verified participant identity. |
| `phase` | `P1`, `P2`, `P3A`, `P3B` | Recorded app condition code. Report interpretation: instructed reading, normal reading, read-to-test, read-to-learn, respectively. |

The original export also had viewport dimensions, session date/time fields
and user-agent strings. These fields are not part of the prepared release.
Their removal does not turn behavioural records into anonymous data; the
release is described as **pseudonymized**.

## `data/prepared/quiz_steps.csv`

**Unit:** one question or text-marker step in a session. **Rows:** 1,880:
1,800 question rows and 80 text-marker rows. **Unique key:**
`session_id` + `step_id`.

| Column | Type / values | Meaning |
|---|---|---|
| `session_id` | String | Join to the session table. |
| `step_id` | String such as `T17_Q2` or `Text 3` | Original task-step label, preserved because it identifies the material/step rather than a participant. |
| `step_type` | `question` or `text_marker` | Parsed type. A text-marker row is not a scored comprehension answer. |
| `text_id` | String such as `T17` | Text identity parsed from the step. Full text wording is not included. |
| `question_number` | Integer 1, 2 or 3; blank for text markers | Position of the comprehension question within a text. |
| `points` | Integer 0 or 1 | Recorded earned points. Interpret only together with `max_points`. |
| `max_points` | Integer 0 or 1 | `1` indicates a scored question slot. `0` indicates an unscored record, not proof of an incorrect answer. |

The observed scoring pairs are `(points=0, max_points=0)`, `(0,1)` and `(1,1)`.
A scored `(0,1)` is a recorded zero-point result. An unscored `(0,0)` is not
silently turned into a wrong answer. The export does not identify the reason
for every unscored slot, and does not include chosen answer text or a
separate unanswered/timeout flag.

All 600 session–text blocks have three question slots. Of these, 405 have
three scored questions, 56 have one or two scored questions, and 139 have no
scored questions. A “complete quiz” in the analysis means **all three
questions were scored**, not merely that three rows exist.

## `data/prepared/aoi_events.csv`

**Unit:** one application-recorded event interval. **Rows:** 92,138.
**Unique key:** `session_id` + `event_index`.

The source report calls these fixation events. The release describes them as
event intervals because the detection algorithm and gaze validation are not
supplied. Neither the interval nor its AOI label independently proves a
physiological fixation on a particular word.

| Column | Type / values | Meaning |
|---|---|---|
| `session_id` | String | Join to the session table. |
| `event_index` | Integer starting at 1 within each session | Order of events after sorting by their original start time. |
| `step_id` | String | Question or text-marker step to which the application attached the event. |
| `step_type` | `question` or `text_marker` | Parsed step type; not independent confirmation of what was visible on screen. |
| `text_id` | String | Parsed text identity. |
| `question_number` | Integer 1–3 or blank | Parsed question number, blank for text-marker events. |
| `aoi_category` | `source_text`, `question_or_answer`, `unassigned` | Broad software assignment. Derived from original `s:` labels, `q:` labels or missing labels, respectively. |
| `aoi_code` | String such as `A001`, or blank | New opaque code for an assigned AOI within one session and step. Blank for `unassigned`. Its numbering is order of first observed assignment within that scope. |
| `start_offset_ms` | Nonnegative integer, milliseconds | Original start time minus the first event start time in the same session. |
| `stop_offset_ms` | Positive integer, milliseconds | Original stop time minus that same within-session origin. |
| `duration_ms` | Positive integer, milliseconds | `stop_offset_ms − start_offset_ms`, preserving the source interval length. |

### Timing rules

The first event in each session starts at offset zero. That zero is **not**
the start of reading, the start of the application session, or a wall-clock
time. The original event clock's origin was undocumented; its values were
not established as epoch timestamps. Rebasing preserves within-session
order, intervals and gaps without claiming an absolute time origin.

All supplied event intervals are positive and ordered without overlapping
within a session. Summing their lengths counts only recorded intervals,
excluding gaps. It does not produce a complete reading time, because task
onset/visibility markers and the initial-reading timeline are incomplete.

### AOI scope and interpretation

An AOI code is meaningful only with **`session_id` + `step_id` + `aoi_code`**.
Original AOI IDs were reused across other screens and sessions. `A001` in two
different steps must not be treated as the same word. Code values are not
token indices, positions, coordinates or distances.

The release removes original AOI label wording and replaces original AOI IDs
with these scoped codes. It preserves within-screen repeat assignments and
broad source/question categories. It does not supply an AOI geometry map or
all possible AOIs, so it does not establish true word coverage or skipping.
`unassigned` may reflect looking elsewhere, tracking failure or assignment
failure; the data cannot identify the cause.

## `data/derived/session_text_summary.csv`

**Unit:** one text within one application session. **Rows:** 600.
**Unique key:** `session_id` + `text_id`. Generated from the three prepared
files; no survey labels are joined.

| Column | Type / values | Meaning / calculation |
|---|---|---|
| `session_id` | String | Session key. |
| `app_user_code` | String or blank | Session's app code, preserving missingness. |
| `phase` | Phase code | Session's recorded phase. |
| `text_id` | String | Text key. |
| `question_step_count` | Integer | Number of question rows in this block; 3 for every current block. |
| `scored_question_count` | Integer 0–3 | Number of question rows with `max_points = 1`. |
| `quiz_status` | `complete`, `partial`, `unscored` | All three distinct Q1–Q3 scored; some questions scored; or no questions scored. |
| `correct_answers` | Integer 0–3 or blank | Sum of the three earned points for complete quizzes only. Blank otherwise. |
| `percent_correct` | Number 0–100 or blank | Complete quizzes only: `correct_answers ÷ 3 × 100`, rounded to six decimal places. |
| `question_event_count` | Integer | Number of events in this session/text whose `step_type` is `question`. Includes assigned and unassigned events. |
| `question_assigned_event_count` | Integer | Of those question-step events, count with `aoi_category` other than `unassigned`. |
| `question_assigned_event_percent` | Number 0–100 or blank | Assigned count ÷ question-event count × 100; blank when the denominator is zero. Each event has equal weight. |
| `question_interval_sum_ms` | Integer, milliseconds | Sum of `duration_ms` for question-step events in this block, including unassigned events. Not total reading time or answer-response time. |
| `text_step_event_count` | Integer | Number of events attached to a `text_marker` step in this session/text. |

The `question_` prefix is important. Those summaries use question-step events
only. The whole-export AOI table below also includes text-marker events, so
its counts and percentages have a different denominator.

## Other generated outputs

| File under `data/derived/` | Unit and columns | Interpretation |
|---|---|---|
| `aoi_assignment_counts.csv` | One row per `category`; `events`, `percent_of_all_events` | Counts across all 92,138 events, including text-marker events. Percent = category count ÷ all events × 100. |
| `complete_quiz_scores.csv` | One row per `correct_answers` value 0–3; `complete_quizzes` | Histogram of the 405 complete scored quizzes. |
| `phase_summary.csv` | One row per `phase`; columns defined below | Coverage and quiz-scoring completeness within each exported condition. |
| `summary.json` | One JSON object | Machine-readable totals, quiz-status counts, score histogram, pooled AOI counts/percentages and phase summaries. |
| `RESULTS.md` | Human-readable report | Plain-language explanation of the reproduced counts and denominators. |

`phase_summary.csv` columns are:

| Column | Meaning |
|---|---|
| `phase` | App condition code. |
| `sessions` | Number of session rows in the phase. |
| `distinct_nonmissing_app_ids` | Distinct nonblank app codes in the phase; do not sum across phases to count people. |
| `sessions_without_app_id` | Sessions with blank app code. |
| `events` | All event rows in the phase. |
| `question_events` | Event rows labelled as question steps. |
| `text_marker_events` | Event rows labelled as text markers. |
| `session_text_blocks` | Number of session–text quiz blocks. |
| `complete_quizzes` | Blocks with all three questions scored. |
| `partial_quizzes` | Blocks with one or two questions scored. |
| `unscored_quizzes` | Blocks with no scored questions. |

## Reported tables are a separate evidence layer

The following files are aggregates from the supplied paper/reports. They must
not be joined to individual event rows as if they were a student's survey
answers. The source workbook and camera-to-session mapping are absent.

| File under `data/reported/` | What a row represents | Source / main caution |
|---|---|---|
| `normal_strategy_counts.csv` | A normal-reading survey strategy category and its reported count | 200 selections across 20 students and 10 texts. These are survey choices, not model labels inferred from gaze. |
| `normal_ratings.csv` | A designed-difficulty group and its reported rating summaries | 199 grouped records; group sizes are not independently verified nonmissing counts for each rating item. |
| `instruction_strategy_counts.csv` | Assigned-instruction/self-reported-strategy aggregate counts | Instructed-reading survey; comparison concerns reported instruction following, not webcam accuracy. |
| `webcam_configurations.csv` | One of eight reported webcam configurations | Browser-test settings/results. Not an individual participant record or validated gaze sampling rate. |

All four tables include `source_id` and `source_location`. `source_id` refers
to the identifiers in the source register; a semicolon separates multiple
sources. `source_location` identifies the relevant section, table or figure.
The other columns are:

| File | Column | Type / meaning |
|---|---|---|
| `normal_strategy_counts.csv` | `strategy` | Survey category name: `skimming`, `mixed`, `sequential`, `deep_reading`, `keyword_search` or `other`. |
| | `reports` | Integer count of selections in that category. Six rows total. |
| `normal_ratings.csv` | `designed_difficulty` | Researcher-assigned category: easy, intermediate or hard. |
| | `group_records` | Integer reported group size, summing to 199 across three rows. |
| | `mean_difficulty_1_to_5` | Reported mean difficulty rating on a 1–5 scale. |
| | `mean_effort_1_to_5` | Reported mean effort rating on a 1–5 scale. |
| `instruction_strategy_counts.csv` | `assigned_instruction` | `SKIM`, `SEQ`, `DEEP` or `OTHER`, as recorded in the report. `OTHER` was not one of the three planned instructions. |
| | `reported_strategy` | Student's reported category: `SKIM`, `SEQ`, `DEEP` or `OTHER`. |
| | `records` | Integer count for that instruction/strategy combination. All 16 combinations are represented, including zero counts; total 70. |
| `webcam_configurations.csv` | `configuration_code` | Release table row identifier, `C01`–`C08`; not linked to an app user or session. |
| | `camera_label` | Reported camera name, with A/B suffixes distinguishing two Integrated Camera entries. |
| | `reported_device_context` | Device/OS wording from the report, including unresolved ambiguous labels. |
| | `width_px`, `height_px` | Integer webcam-test image dimensions in pixels; not display dimensions. |
| | `frames_per_second` | Integer browser webcam-test FPS; not the app's measured gaze sampling rate. |

See the [source register](source-register.md) for the source documents and
[paper and pilot scope](paper-and-pilot-scope.md) for reported calculations.
The [study guide](study-guide.md) explains the experimental scenario and why
the application, survey and webcam samples should remain distinct.
