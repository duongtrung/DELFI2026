# What comes from the DELFI paper, and what comes from the wider pilot?

The DELFI paper was written from the same study programme, with its main
empirical story focused on the **normal-reading activity**. It does not report
every planned activity or every application session as a single fully linked
experiment. This release makes a wider set of application records available
and clearly separates those records from the paper's survey aggregates.

The paper is *Fit-for-Purpose Webcam Eye Tracking for Scalable Reading
Analytics: A Pilot Study with Master’s Students*, by Nghia Duong-Trung,
Alexander Zimmermann, Konstantinos Tsiakas, Michael Dietrich and Miloš
Kravčík. The supplied copy names `duongtrung/DELFI2026` as its supplementary
repository. Publication metadata beyond what is present in that copy should
be added by the authors, rather than inferred. [PAPER title, §6]

## Keep these samples separate

| Sample | Size and observation unit | What is available for this release? |
|---|---|---|
| Paper's normal-reading survey | 20 participants × 10 texts = 200 student–text responses | Reported aggregates from the paper and Survey Report. The original row-level survey workbook is absent. |
| Instructed-reading survey | 7 participants, 70 student–text responses | Survey Report aggregates; no independently reproducible row-level linkage. |
| Free-form survey | 20 participant-level records; 16 with a condition label | Survey Report aggregates, not a matched 20-person application subset. |
| Full application export | 60 session rows, 92,138 event rows, 1,880 quiz/marker rows | Prepared, pseudonymized derivatives of the three supplied CSVs, from all exported conditions. |
| Complete three-question quizzes | 405 session–text blocks retained from 600 blocks | Recomputed from the question export using the rule below. |
| Webcam configuration screen | 8 distinct configurations | Report appendix values; not eight independently validated gaze datasets. |

The session export contains **26 distinct nonmissing application user IDs**.
That is a software identifier count, not independent verification that exactly
26 distinct people participated. A person can have repeated sessions, and an
entered identifier can be missing or inconsistent.

| Application phase code | Interpretation in Raw Data Report | Sessions | Distinct nonmissing app user IDs within phase |
|---|---|---:|---:|
| `P1` | Instructed reading | 24 | 23 |
| `P2` | Normal reading | 26 | 22 |
| `P3A` | Read-to-test | 2 | 2 |
| `P3B` | Read-to-learn | 8 | 8 |
| Total | All exported conditions | 60 | 26 across phases |

Do not add the within-phase ID counts to estimate participants: the same ID
can appear in more than one phase. Do not equate the 26 `P2` sessions with the
20 completed normal-reading survey participants. The earlier Raw Data Report
described exact-ID links for 30 instructed-reading text rows, 130
normal-reading rows and 60 free-form rows. The workbook, ID mapping and those
joined tables are not available here, so that historical linkage cannot be
recreated from the three CSVs alone. [RAW §§3, 5]

## Which results can be recomputed?

### Survey ratings: reported summaries, not newly recovered responses

The paper and Survey Report provide the following normal-reading summaries.
One of the 200 responses lacked a designed-difficulty label, leaving 199
records in the grouped table. [PAPER Table 1; SURVEY §4.2]

| Designed difficulty | Reported records in group | Mean perceived difficulty, 1–5 | Mean effort, 1–5 |
|---|---:|---:|---:|
| Easy | 59 | 2.20 | 2.57 |
| Intermediate | 80 | 2.48 | 2.66 |
| Hard | 60 | 2.58 | 3.03 |

A mean is the sum of the available ratings divided by their count. The raw
ratings are absent, so the group counts above cannot be independently checked
as the number of nonmissing responses to each separate rating item. The
displayed rounded means give:

- Difficulty: 2.58 − 2.20 = **0.38 points** higher for hard than easy texts.
- Effort: 3.03 − 2.57 = **0.46 points** higher for hard than easy texts.

These are descriptive differences on a five-point response scale. They do not
prove that designed difficulty caused a change, or that the difference is
statistically significant. Each student contributed multiple responses, and
each text was read by multiple students.

The normal-reading survey strategy counts are skimming 52, mixed 49,
sequential 47, deep reading 25, keyword search 24 and other 3. The counts sum
to **200 selections**, not 200 people and not 200 webcam predictions.

### AOI assignments: directly countable from the event export

Count each event once, with no duration or quality filter. The preparation
script classifies the original `aoi` label by prefix; the released
`data/prepared/aoi_events.csv` stores that result as `aoi_category`.
Across all exported conditions:

| Software-assigned category | Event count | Share of all 92,138 events |
|---|---:|---:|
| Source text (`source_text`; originally `s:`) | 39,833 | 43.2% |
| Question/answer (`question_or_answer`; originally `q:`) | 10,832 | 11.8% |
| No recorded AOI (`unassigned`) | 41,473 | 45.0% |

The proportion with an assigned label is:

**(39,833 + 10,832) ÷ 92,138 × 100 = 55.0%, rounded.**

This is software assignment coverage across events. It is not percentage of
reading time, an average of student-level ratios, word-level accuracy or
strategy agreement. Unassigned events cannot be interpreted directly as
inattention.

The paper also mentions valid-AOI ratios of .604 and .577, and high-quality
text-row ratios of .750 and .700, for a much smaller linked camera subset.
Those are different denominators. The supplied material does not provide
enough traceable row membership and quality-threshold detail to reproduce
those camera-specific ratios. They must not be substituted for the pooled
event calculation above. [PAPER Table 1, §4; CAMERA; RAW §4]

### Quiz scores: use complete three-question quizzes

The unit is **one text within one application session**. For example, if a
student gets two questions right and one wrong, the score is 2 out of 3. As a
proportion that is 2 ÷ 3, about 0.667; as a percentage it is about 66.7%.

The reproducible complete-quiz rule is:

1. Select question-step IDs of the form `T<number>_Q1`, `_Q2` or `_Q3`.
2. Group rows by session and text. There are 600 such blocks.
3. Keep only blocks with Q1, Q2 and Q3 present once each and each with
   `max_points = 1`. In these retained rows the outcome is 0 or 1.
4. Sum the three earned points. This leaves 405 complete quizzes.

All 600 blocks contain three question slots. The other 195 blocks are
excluded because not all slots are scored: 56 have one or two scored
questions and 139 have none. A row with `max_points = 0` is unscored, not
evidence of a wrong answer.

| Correct answers | Complete quizzes |
|---|---:|
| 0 out of 3 | 24 |
| 1 out of 3 | 55 |
| 2 out of 3 | 57 |
| 3 out of 3 | 269 |
| Total | 405 |

**269 ÷ 405 × 100 = 66.4%, rounded**, received the maximum score. The maximum
is the **ceiling**. A **ceiling effect** means many observations pile up at
that maximum, so the quiz cannot distinguish additional differences in
performance above it. It does not tell us whether the cause was easy
questions, prior knowledge, text availability or something else.

This calculation pools all exported conditions and is not restricted to the
paper's 200 survey responses. The earlier Raw Data Report summarized 461
blocks with at least one scored question. That broader count includes 56
partial quizzes, so a “perfect” partial quiz need not contain three correct
answers. The present complete-quiz rule makes the denominator explicit.

## Corrections and unresolved implementation details

| Topic | Sources differ or are incomplete | Treatment in this release |
|---|---|---|
| Calibration | Protocol planned calibration; paper mentions calibration/practice. The investigator later relayed the technician's statement that there was no camera calibration. | State **no camera calibration was performed**. No validation metrics exist in the supplied exports. Retain the discrepancy visibly instead of silently rewriting source history. |
| Normal-reading text visibility | Protocol says the text disappears before questions; paper says text and questions appear together. | Treat actual visibility as unresolved. Neither a memory-only task nor a text-visible task is assumed for `P2`. |
| Number of webcams | Webcam report introduction says seven; its appendix contains eight rows, consistent with the paper. | Use the eight appendix configurations. |
| AOI granularity | Paper discusses coarse regions but also word-level AOIs. The export stores token-like labels without geometry. | Explain that small software labels can be grouped into broad categories; neither grouping validates gaze accuracy. |
| App user agents | Some strings and viewports could be read as mobile devices. Raw Data Report says collection used laptop webcams. | Treat browser/device fields as recorded metadata, not proof of phone collection. |
| Free-form groups | Survey has 11/5 known assignments; app has 2/8 sessions. Protocol proposes random assignment. | Report each sample separately. No balanced randomised comparison is established from these files. |
| Reading time | Most events carry question-step labels; no complete task-timeline export is present. | Event intervals are not automatically initial-reading durations. |

The paper reports ethics approval and the protocol includes paper consent, but
neither the approval record nor signed consent documents were supplied for
this release preparation. A claim that participation was approved is not
documentation of permission for unrestricted public redistribution. The
release's separate publication/reuse notes should govern that decision.

## What would make a fuller reproducibility package?

These items are **not supplied in the present source set**, even where an
earlier report says they were available to its author:

- Row-level survey workbook, survey form export and a safe app–survey linkage.
- Full reading texts, question wording, answer keys and material versions.
- Application source code, dependency versions and a definition of how
  “fixation” events were detected and timed.
- AOI geometry, token positions and layout/visibility versions.
- Raw gaze coordinates, confidence values and calibration/validation logs.
- Counterbalancing or randomisation schedule and verified condition events.
- Original model-ready tables, training code and model configurations.

The reports name exploratory Ridge and random-forest analyses, but the
released CSVs are not the complete labelled dataset needed to reproduce
those analyses. No validated reading-strategy classifier or successful
prediction result is supplied. The most useful next step is to improve
measurement and linkage before expanding predictive modelling.

Source identifiers such as PAPER and RAW are defined in the
[source register](source-register.md). For a participant-facing explanation
of the study, start with the [study guide](study-guide.md).
