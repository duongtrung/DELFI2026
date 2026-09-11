# DELFI2026 · Webcam reading pilot

**How do students read when a quiz score tells only part of the story?**

Two students can both answer three questions correctly while reading very
differently. This pilot combined ordinary laptop webcams, short reading tasks,
comprehension questions and learner surveys to investigate what additional
information could be collected in a classroom.

This repository explains the study, provides minimized application datasets,
and shows how to reproduce the descriptive results. It accompanies
**“Fit-for-Purpose Webcam Eye Tracking for Scalable Reading Analytics:
A Pilot Study with Master’s Students”** by Nghia Duong-Trung, Alexander
Zimmermann, Konstantinos Tsiakas, Michael Dietrich and Miloš Kravčík.

**Release candidate, prepared 11 September 2026.** The row-level files are
pseudonymized, not guaranteed anonymous. Public data-sharing authorization and
dataset reuse terms need the authors' confirmation before this candidate is
published. The existing repository's GPLv2 license is preserved for code;
[release notes](docs/release-and-rights.md) explain the remaining decisions.

## Start here

| If you want to… | Open… |
|---|---|
| Understand what students did | [Study guide](docs/study-guide.md) |
| See which part became the DELFI paper | [Paper and full-pilot coverage](docs/paper-and-pilot-scope.md) |
| Read the reproducible results without programming | [Application results](data/derived/RESULTS.md) |
| Understand each column and how files join | [Data dictionary](docs/data-dictionary.md) |
| Recalculate the results | [Step-by-step reproduction](docs/reproduce.md) |
| Understand what the webcam evidence supports | [Limitations and the next study](docs/limitations-and-next-study.md) |

## What did a student do?

1. Read a short text about multi-agent systems, such as how agents delegate work.
2. Answer three comprehension questions about that text.
3. Rate the experience and report the reading strategy used.

The normal-reading activity used ten texts. **Twenty completed survey
participants × ten texts = 200 survey records.** These are repeated responses
from twenty students, not two hundred students. The broader pilot also
included instructed reading and a comparison of answering with the text
available versus answering from memory. The paper and protocol differ on
text visibility in normal reading; this release records that unresolved detail.

## What is actually in the data?

| File | One row means… | Rows | Origin |
|---|---|---:|---|
| [sessions.csv](data/prepared/sessions.csv) | One application session or attempt | 60 | Transformed original export |
| [quiz_steps.csv](data/prepared/quiz_steps.csv) | One question slot or text-marker step | 1,880 | Transformed original export |
| [aoi_events.csv](data/prepared/aoi_events.csv) | One recorded event interval and its software AOI assignment | 92,138 | Transformed original export |
| [session_text_summary.csv](data/derived/session_text_summary.csv) | One text in one application session | 600 | Recalculated by the included script |
| [Reported survey and webcam tables](data/reported/README.md) | One aggregate category, cross-tabulation cell or camera configuration | Four small tables | Transcribed from reports and paper |

The application files cover **all pilot conditions**. Their 60 sessions contain
26 distinct nonmissing app-user IDs and one session with no app-user ID.
Neither count establishes the number of unique people. The raw survey workbook
and the app-to-survey identity mapping are not supplied. Consequently the
application exports cannot be restricted reliably to exactly the paper's
twenty survey participants, and individual survey labels are not in this release.

### Three findings you can follow

| Finding | How the number is obtained | What it means |
|---|---|---|
| **66.4% perfect complete quizzes** | 269 quizzes with three correct answers ÷ 405 fully scored three-question quizzes | Many scores are at the maximum; the quiz has limited ability to separate performance levels. This pools all conditions. |
| **55.0% of events have an AOI assignment** | (39,833 source-text + 10,832 question/answer events) ÷ 92,138 events | Assignment coverage, not the accuracy of gaze positions or percentage of reading time. |
| **Eight webcam configurations at 20–30 FPS** | Reported camera-test configurations, with resolution and frame rate listed separately | All met the study's minimum hardware screen. Passing the screen does not establish accurate eye tracking. |

For the normal-reading survey, reported strategies were skimming 52, mixed 49,
sequential 47, deep reading 25, keyword search 24 and other 3. These sum to
200 **self-reports**. They are not webcam predictions. Survey summaries can be
inspected here, but cannot be recalculated from individual responses because
the survey workbook is missing.

## Reproduce the application results

Use Python **3.10 or later**, with no additional packages. From this folder:

```bash
python scripts/validate_release.py
python scripts/analyze.py
python -m unittest discover -s tests -v
```

The first command checks the supplied release files and recomputes the shipped
outputs in a temporary directory. The second regenerates `data/derived/` and
prints the main totals. The tests use invented records to check important edge
cases. Original private data and a pseudonymization key are not needed.

For an example of what “two correct answers” means and how to filter normal
reading, see the [worked examples](docs/reproduce.md).

## Read this before interpreting gaze or training a model

- **No camera calibration was performed**, according to the technician's
  clarification relayed by the investigator. This corrects wording in the
  protocol and paper.
- An **area of interest (AOI)** is a labelled part of the displayed material.
  Word labels in the original software export have been replaced with broad
  categories and opaque codes. A code is meaningful only within one session
  and one step; it is not a validated word position.
- The files contain event intervals, not webcam video or raw gaze coordinates.
  They lack spatial validation errors, complete AOI geometry and reliable
  markers separating initial reading from question answering.
- Instruction–survey agreement is different from webcam–survey agreement.
  The latter cannot be measured from the supplied files. This is not a
  validated reading-strategy recognition benchmark.

The release supports data auditing, scoring summaries and exploratory analysis
of software-assigned regions. See the [next-study plan](docs/limitations-and-next-study.md)
for how to collect evidence that could make future modelling useful.

## Citation and provenance

Use [CITATION.cff](CITATION.cff) for the supplied paper's authors and title.
Final proceedings details and a dataset DOI have not been supplied; no DOI is
invented. Once a public release is issued, cite its exact tag or commit as well.
[Source register](docs/source-register.md) identifies the documents, CSVs,
calculation sources and known discrepancies. The repository named in the
paper is [duongtrung/DELFI2026](https://github.com/duongtrung/DELFI2026).
