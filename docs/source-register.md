# Source register

This register identifies the files supplied by the investigator and used to
prepare the release documentation. It distinguishes direct CSV calculations,
reported aggregates and protocol intentions. Original source documents are
not copied wholesale into this repository by this register.

The SHA-256 values below fingerprint the **original supplied files**, not
renamed, transformed or de-identified release files. Checksums demonstrate
which source bytes were inspected; they are not a claim that every original
file is included in the release.

## Study documents

| ID | Supplied file | Role and useful locations |
|---|---|---|
| PAPER | `5af204b1-1e68-4f36-af4e-784a1cb47148.pdf` | Supplied DELFI paper, *Fit-for-Purpose Webcam Eye Tracking for Scalable Reading Analytics: A Pilot Study with Master’s Students*. §3: classroom, normal-reading sample, materials, procedure and AOIs. Table 1 and §4: hardware and survey summaries. §6: supplementary-repository address. |
| SURVEY | `59559b83-f4d4-4706-91e2-2495a2f54595.docx` | *Survey Report*. §3: source workbook and cleaning/submission audit. §4.1: instruction–survey agreement. §4.2: normal-reading means and strategy counts. §4.3: free-form condition counts. §6: missing data and future exports. |
| RAW | `7cc5ea10-37b8-4557-bbcb-fc738bf995cb.docx` | *Raw Data Report*. §3: app row counts and phase coverage. §4: parsing/AOI interpretations and derived datasets. §5: historical exact-ID linkage. §6: descriptive summaries. §§7–8: prototype-model limitations and next collection. |
| CAMERA | `a5485bc2-77c1-4f97-9fe2-0fb24b793689.docx` | Webcam feasibility report. §3: interpretation of browser webcam-test metrics. §6: proposed technical criteria. Appendix A: eight configuration entries. Introduction's seven-entry statement conflicts with appendix. |
| PROTOCOL | `f3a3ce7a-ca3e-4a93-b759-086c87e66cee.docx` | *Protocol: Webcam-Based Eye-Tracking Study Using the Multi-Agent Systems Reading Section*. §§2, 4–8: materials and phase design. §§9–10: intended measurements and expected dataset. §11: planned participant flow. This is a plan, not proof that each step was implemented. |

Section names are used because Word pagination can change across renderers.
The paper's method spans PDF pages 2–3 and its results begin on page 3
(one-based physical page numbering). No DOI, proceedings page range or public
publication URL for this paper was present in the supplied copy; none is
invented here.

| ID | Original bytes | SHA-256 |
|---|---:|---|
| PAPER | 169060 | `ae2682ca09e63b67e119284bbf94fbe4745528acf2e27c84b9c15d59472fac03` |
| SURVEY | 834422 | `890bbf5abc6bf903057914f1a7a4e7c1c59246ab72306c8fab2ac5a7dab4e397` |
| RAW | 298329 | `9b875a41686fd2fe101d6dd591e3a18c3caacabf38e8883e8377a31e4ba91f43` |
| CAMERA | 46372 | `82f9205e920f4c569049139dff9ab5a93db4d3de6c4ec25997f9fa0478b1f04b` |
| PROTOCOL | 36957 | `1996e27e1068b9ff080e4501e861f18a088b92283c7000b985e26f117cf24514` |

## Original application exports

The original reports call these `fixation.csv`, `quiz.csv` and `trial.csv`.
The investigator supplied them under the following upload filenames.

| ID | Supplied file | Rows | Original schema |
|---|---|---:|---|
| EVENTS | `d60e873e-b56d-4538-b833-5e95d3b86d7b.csv` | 92,138 | `id, step_id, trial_id, aoi, aoi_id, start_ts, stop_ts` |
| QUIZ | `75263db0-d740-4af3-8a2a-70927758a315.csv` | 1,880 | `id, step_id, points, max_points, trial_id` |
| SESSIONS | `bf1f096f-8713-45eb-918c-998ce3501ce9.csv` | 60 | `id, viewport_w, viewport_h, start_datetime, finish_datetime, user_agent, user_id, phase` |

| ID | Original bytes | SHA-256 |
|---|---:|---|
| EVENTS | 5251974 | `065d6f02caca39da76148b13a2d0018fa61b14e23ef695f043984b56931e7237` |
| QUIZ | 57897 | `56df2232be618c1085683294edfd887c2866063507c00c402842e4131bf0c518` |
| SESSIONS | 12720 | `bc89660c1d03f985b386febb246327681ccfc1a0d161571b621e44fefad3037f` |

The repository's data dictionary and transformation notes define the actual
release columns and identifier handling. Original source schemas above do not
override those release definitions.

## Investigator clarification and interpretation precedence

The investigator stated during preparation of the poster and data release:
“My technician told me that there was no camera calibration.” This is a
user-supplied correction, not a calibration log or an independently inspected
technical record. The current documentation therefore states **no camera
calibration was performed**, and flags the conflicting calibration wording
in the protocol and paper.

Use the following order when interpreting a claim:

1. **Released CSV calculation:** counts and calculations whose rows and rule
   are present can be reproduced. Preserve the unit and denominator.
2. **Investigator correction:** report it explicitly when it changes the
   implemented procedure, while retaining the source discrepancy.
3. **Reported aggregate:** a number copied from the paper/report is labelled
   as reported if its underlying rows are absent.
4. **Protocol intention:** intended calibration, random assignment, logging
   fields or predictions are not evidence that those steps occurred.

The original reports discuss external literature. This repository guide does
not independently review or adopt every general claim in those reports; its
purpose is to document this particular data collection.

## Claim-to-source map

| Claim | Evidence used | Reproducibility boundary |
|---|---|---|
| 20 normal-reading survey participants, 200 student–text records | PAPER §3/Table 1; SURVEY §4.2 | Reported; no survey workbook supplied here |
| Group means and six strategy counts | PAPER Table 1; SURVEY §4.2 | Reported aggregates; rounded-mean differences can be checked |
| 37/55 = 67.3% instruction–survey agreement | SURVEY §4.1 instruction-match tables | Reported numerator/denominator; no gaze classifier involved |
| 60 app sessions and phase counts | SESSIONS; RAW §3 | Directly countable |
| 92,138 events and 55.0% with an AOI label | EVENTS | Directly countable by released `aoi_category`, derived from original prefix/missingness; not gaze accuracy |
| 405 complete quizzes; 269 perfect | QUIZ | Directly countable with the documented complete-quiz rule |
| Eight configurations, 20–30 FPS | CAMERA Appendix A; PAPER §3/Table 1 | Reported browser-test values; not effective gaze sampling |
| No calibration performed | Investigator's technician clarification | Corrected implementation account; no validation files supplied |
| Source text/question visibility in normal reading | PROTOCOL §7 versus PAPER §3 | Unresolved source conflict |
| Historical exact app–survey linking | RAW §5 | Joined data and mapping absent; not independently reproducible here |

For interpretation, see the [study guide](study-guide.md). For sample
boundaries and differences from the paper, see
[paper and pilot scope](paper-and-pilot-scope.md).
