# A guide to the reading study

Two students can answer the same three questions correctly while approaching a
text differently. One might read from beginning to end; another might scan for
relevant passages. This pilot explored whether an ordinary laptop webcam,
short quizzes and learner surveys could provide useful information about that
reading process in a classroom.

The released application data make the collection auditable. They do **not**
establish that a webcam recognized a student's exact reading strategy. The
survey results describe what students reported; the event data describe what
the software recorded and assigned to areas on the page. Connecting these two
kinds of evidence remains work for a better-linked, validated collection.

## The classroom scenario

The supplied DELFI paper describes volunteer master's students at Gisma
University of Applied Sciences, Potsdam, in the Data Science, AI and Digital
Business programme. Students completed reading activities about multi-agent
systems after a regular lesson. The paper places collection in May and June
2026; the survey report identifies completed submissions on 3–4 June 2026.
These describe different scopes and should not be treated as an exact date
for every application session. [PAPER §3; SURVEY §§1.2, 3.3]

For the normal-reading activity, the practical sequence was:

1. **Read a short text at your own pace.** Topics included agent delegation,
   memory, computer-use agents and evaluation.
2. **Answer three comprehension questions.** The materials assigned one easy,
   one intermediate and one hard question to each text.
3. **Describe the experience in a survey.** Students rated difficulty, mental
   effort, understanding, familiarity and confidence, and selected their main
   reading strategy.
4. **Repeat for ten texts.** Twenty completed survey participants produced
   20 × 10 = **200 student–text records**. A record is one student's response
   about one text; it is not a new participant.

The paper says text and questions were visible together during normal reading.
The protocol says the text disappeared before questions. The supplied exports
do not resolve this implementation difference. Consequently this guide does
not assume that the normal-reading quiz was answered from memory or with the
text available. [PAPER §3; PROTOCOL §7]

## How the broader pilot was organized

The protocol specified preparation followed by three reading activities. The
table separates the intended procedure from the evidence actually available.

| Protocol activity | Intended task | Available evidence and limits |
|---|---|---|
| Preparation (Phase 0) | Study information, consent, background questions, webcam setup and practice; calibration was planned. | The investigator relayed the technician's correction: **no camera calibration was performed**. The export contains no calibration or validation results. |
| Instructed reading (Phase 1; app code `P1`) | Before a text, follow an instruction to skim, read sequentially or read deeply. Then answer questions and report the strategy used. | The survey report summarizes 70 student–text responses from 7 completed participants. The application export contains 24 sessions; those sessions are not the same count or a fully matched sample. |
| Normal reading (Phase 2; app code `P2`) | Read at your own pace across texts of different designed difficulties, then answer questions and report the experience. | The paper's main survey sample: 200 responses from 20 participants. The application export contains 26 sessions. Normal-reading screen visibility is unresolved as described above. |
| Free-form reading (Phase 3; app codes `P3A`, `P3B`) | Choose a strategy; compare answering with the text visible (read-to-test) against answering after it disappears (read-to-learn). | The survey report has 20 participant-level records: 11 read-to-test, 5 read-to-learn and 4 without a condition label. The app has 2 `P3A` and 8 `P3B` sessions. The Raw Data Report maps these to read-to-test and read-to-learn respectively. The supplied files do not independently verify random assignment or screen visibility. |

The protocol's planned durations are not measured durations for each released
session. The paper estimates about 45 minutes for its activity. The survey
report gives a median submission duration of 37.1 minutes and a maximum of
252.6 minutes; a survey elapsed time can include pauses and is not a direct
reading-time measure. [PROTOCOL §§4–8, 11; SURVEY §§3.3, 4.1–4.3; RAW §§1–3]

## Which texts belonged to each activity?

The protocol supplies the following IDs. An ID is a join key, not the text
itself. The complete reading passages, question wording and answer key were
not supplied for this repository preparation, so this is a materials index,
not a reproducible copy of the task. [PROTOCOL §2, materials table]

| Activity | Text IDs | Designed difficulty |
|---|---|---|
| Instructed reading | T12, T15, T18, T20, T24, T27, T28, T30, T37, T41 | Mainly intermediate |
| Normal reading | T2, T5, T17, T26, T33, T42, T45, T47, T48, T49 | 3 easy, 4 intermediate, 3 hard |
| Free-form reading | T3, T4, T9, T10, T19, T29, T31, T32, T46, T50 | Mixed easy, intermediate and hard |

For normal reading, the reported text-level metadata are:

| Text ID | Topic/title reported in the Survey Report | Designed difficulty |
|---|---|---|
| T2 | Why complex tasks may need multiple agents | Easy |
| T5 | What is a multi-agent system? | Easy |
| T17 | Cost-aware action delegation | Intermediate |
| T26 | Long-term memory and retrieval | Intermediate |
| T33 | Computer use agents | Hard |
| T42 | Round-robin orchestration | Easy |
| T45 | Backend and frontend in agent web applications | Intermediate |
| T47 | Evaluating multi-agent frameworks | Intermediate |
| T48 | Trajectory-based evaluation | Hard |
| T49 | LLM-as-a-judge and evaluation metrics | Hard |

These are researcher-assigned difficulty categories, not difficulty inferred
from the webcam or a proven ranking for every student. [SURVEY §4.2, text table]

## What an area of interest means here

An **area of interest (AOI)** is a part of a screen that the software gives a
label. It can correspond to a word or token. Several small AOIs can then be
grouped into a larger category, such as the source text or the question panel.

The original event export contains labels interpreted in the Raw Data Report
as follows. The prepared release replaces their wording with a broad category
and an opaque AOI code:

| Original label | Released `aoi_category` | Interpretation |
|---|---|---|
| Begins with `s:` | `source_text` | Software assignment to source-text content |
| Begins with `q:` | `question_or_answer` | Software assignment to question/answer content |
| Missing | `unassigned` | No AOI assignment recorded |

For example, counting all `source_text` events answers “How many exported
events were assigned to source text?” It does **not** answer “How many words did the
student understand?” A missing label may reflect a look outside the labelled
regions, tracking problems or mapping problems. The export cannot distinguish
these possibilities.

The supplied data contain event start/stop intervals and AOI labels, but no
raw gaze x/y coordinates, AOI bounding boxes, calibration results or spatial
validation errors. Therefore a word label is a software assignment, not
independent evidence that the student fixated that exact word. True word
coverage, skipped words and backward eye movements cannot be reconstructed
reliably from these files. [RAW §§2, 4; investigator correction]

The released `aoi_code` has meaning only within its `session_id` and `step_id`.
The same code on another screen can represent something different. It is not
a word position or a coordinate. See the [data dictionary](data-dictionary.md).

Most events are attached to question-step identifiers such as `T17_Q2`. All
`P1` and `P2` events use question-step labels. Only `P3B` also includes events
with `Text` step labels. These names alone do not establish when the text was
visible or identify a clean initial-reading interval.

## Three different meanings of “reading strategy”

| Evidence | What it tells us | What it does not establish |
|---|---|---|
| Assigned instruction | What the researcher asked the student to do | Whether the student actually did it |
| Survey selection | How the student described their main approach | A directly observed eye-movement pattern |
| Independently validated behavioural label | What a specified measurement procedure can distinguish | This label is not available in the current release |

In the instructed-reading survey, 55 of the 70 responses had one of the three
planned instruction labels. Of these, 37 reported the same strategy as the
instruction: **37 ÷ 55 × 100 = 67.3%**. The other 15 responses had `OTHER` as
the assigned instruction and are excluded from this agreement calculation.
This is **instruction–survey agreement**, not webcam classification accuracy.
[SURVEY §4.1, instruction-match tables]

To measure webcam–survey agreement, researchers would need a reliably matched
student/text record, a pre-specified and validated way to label behaviour from
gaze, and a survey label for that same observation. The current application
CSVs do not include those matched survey labels.

## What the hardware screen established

The webcam report's appendix lists eight distinct configurations. Camera names
and device contexts below preserve the report's wording, including ambiguous
entries; they are not manufacturer model identifications. “A” and “B” simply
distinguish the two entries called Integrated Camera. [CAMERA Appendix A]

| Camera label | Reported device / OS | Test resolution | Test FPS |
|---|---|---:|---:|
| HP HD Camera | HP / Windows 11 | 1280 × 720 | 25 |
| Integrated Camera A | Acer/Asus / Windows 11 | 1280 × 720 | 30 |
| Integrated Camera B | Acer/Asus / Windows 11 | 1280 × 720 | 29 |
| Integrated Webcam | Dell / Windows 11 | 2560 × 1440 | 30 |
| Samsung Camera Front | Motorola / Windows 11 | 1920 × 1080 | 29 |
| MacBook Air Camera | MacBook / macOS | 1920 × 1080 | 28 |
| USB2.0 HD UVC Webcam | Legion / Windows 11 | 1280 × 720 | 20 |
| ASUS HD webcam | Acer/Asus / Windows 11 | 1280 × 720 | 30 |

Every configuration met the study's minimum screen of 1280 × 720 and 20 FPS.
Three also met the preferred screen of 1920 × 1080 and 25 FPS. The lowest
recorded rate was **20 FPS**, or one frame every **50 milliseconds**, for the
Legion USB2.0 HD UVC webcam. These are browser webcam-test readings, not the
measured sampling rate or spatial accuracy of the reading application.

The screen shows that these cameras could provide a video stream meeting the
chosen technical thresholds. It does not validate gaze accuracy. Only two
camera-metadata records were fully linked to gaze logs in the earlier
analysis, which prevents a meaningful ranking of the eight configurations by
gaze quality. [CAMERA §§3, 6, Appendix A; PAPER Table 1]

## A sensible next experiment

1. **Make records join automatically.** Use one pseudonymous study ID across
   the app and survey, and record the text, instruction and condition with
   every response.
2. **Check where the tracker thinks a person is looking.** Calibrate, present
   known targets, measure errors, and repeat quality checks during the task.
   Start with large, separated screen regions.
3. **Record the actual task sequence.** Export text-onset, text-hidden,
   question-onset and answer-submission events, the layout and complete AOI
   geometry. Preserve the software version and logging definitions.
4. **Make strategy comparisons interpretable.** Specify observable criteria
   for each strategy, collect independent reference labels and compare them
   with the matched survey responses. An instruction alone is not ground
   truth for actual behaviour.
5. **Use quizzes that distinguish learning.** Pilot items across difficulty
   levels, measure prior knowledge and consider later retention questions.
   Many perfect three-question quizzes leave little variation to explain.
6. **Test whether gaze adds useful information.** Only after the earlier
   steps, compare future models with simple text-only, quiz-history and
   learner-background baselines on students not used for training. Repeated
   rows from one student must remain together during train/test splitting.

The current release supports data auditing, transparent descriptive summaries
and planning such a follow-up. It is not a validated strategy-recognition
benchmark. See [paper and pilot scope](paper-and-pilot-scope.md) for exact
sample boundaries and [source register](source-register.md) for provenance.
