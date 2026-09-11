# What these data support, and what to improve next

The collection demonstrates that a classroom can produce survey, quiz and
software-assigned AOI event records using ordinary laptop webcams. It does
not establish accurate detection of exact reading strategies or individual
word movements. This distinction is central to useful reuse of the dataset.

## What can be investigated now?

| Question | Current support |
|---|---|
| Which conditions and steps produced records? | Directly auditable from sessions, steps and event counts. |
| How many complete quizzes had each score? | Directly reproducible, with unscored slots handled explicitly. |
| How often did the software assign an event to source or question material? | Directly reproducible broad assignment counts. This does not validate accuracy. |
| What strategies did learners report? | Aggregate survey counts are available from the report. Individual survey rows are missing. |
| Did students report following assigned instructions? | Aggregate instruction–survey cross-tabulation is available. This is not a webcam comparison. |
| Did a webcam accurately recognize the selected strategy? | Not estimable: independently validated gaze labels and matched individual survey responses are missing. |
| Which webcam produced the most accurate gaze? | Not estimable: hardware screening is separate from spatial accuracy, and reliable camera-session linkage is absent. |

## Concrete limitations

**Calibration and spatial validity.** The technician's clarification is that
no camera calibration was performed. No validation target errors, raw gaze
coordinates, tracking confidence or complete AOI geometry are provided. The
existence of a word-like AOI label is not evidence that a student looked at
that exact word. The eight webcam configurations passed the study's hardware
screen; that screen is not an eye-tracking accuracy test.

**Reading boundaries.** Every instructed- and normal-reading event has a
question-step label. Without explicit reading-start and completion events,
their intervals cannot be isolated as initial reading time. Summed event
durations exclude gaps and are not elapsed reading time. Long intervals are
retained; the detector algorithm and thresholds are not available.

**Incomplete linkage.** One original session has a missing app-user ID.
Known IDs are preserved as new codes, but 26 app IDs do not independently
prove 26 unique people. The survey workbook and mapping are absent. A join
by row order, approximate name, text ID alone or assumed participant count
would create unsupported labels.

**Measurement limits.** Three binary questions yield only four complete
scores: zero, one, two or three correct. Many quizzes reach three correct,
so different levels of knowledge may receive the same maximum score. Survey
ratings are subjective and repeated within students. The small, imbalanced
phase samples do not establish causal effects of reading conditions.

**Release minimization.** This candidate omits original timestamps, IDs,
browser strings, viewports and word strings. That limits device-layout
analyses and textual reconstruction. The remaining records are pseudonymized;
individual patterns across sessions can still be distinctive.

## A stronger next collection, in practical order

1. **Connect the records reliably.** Generate one study ID automatically in
   the app and survey. Give every session, text, question and survey response
   its own identifier. Check the link before the student leaves.
2. **Measure spatial quality.** Include calibration and validation targets,
   record the errors and tracking loss, and choose AOI sizes supported by
   those measurements. Establish quality rules before evaluating outcomes.
3. **Record the actual task timeline.** Log text shown, reading start,
   reading complete, question shown, answer submitted and text visibility.
   Record layout, scrolling and AOI rectangles with the same event clock.
4. **Collect independent strategy evidence.** Define observable criteria
   for each intended strategy. Use validated reference measurements and/or
   independent coding where feasible, and document disagreements. Ask for
   the student's strategy report for the same session and text. Compare
   instruction, independent observation and self-report as three different
   kinds of label, rather than assuming they are interchangeable.
5. **Improve learning measurements.** Pilot more discriminating items,
   distinguish unanswered from incorrect, and add prior-knowledge and
   delayed-comprehension measures. Balance the reading conditions and
   document completed, excluded and missing records.
6. **Test whether modelling adds useful information.** Decide the practical
   target first, then compare against simple alternatives on new students
   and new texts. Keep all observations of a student together in each split.

## How future machine learning could become meaningful

A useful example task is: **after one text, can process measurements improve
prediction of a later comprehension score beyond what quiz history and text
difficulty already tell us?** Another is agreement with independently
validated strategy labels. The current release does not supply those labels
or establish successful predictions; it contains no trained model or claimed
strategy-recognition performance.

For a future model, one observation should represent one student reading one
text under a documented condition. Candidate features would be available
before the outcome: validated broad-AOI allocation, switching patterns,
explicit reading duration, text characteristics and prior-knowledge measures.
Current `question_*` event features come from question-labelled steps and
must not silently be described as pre-quiz reading features. Including the
answer or an event occurring after the target is known would leak the outcome.

Start with a majority/mean baseline and a quiz-history/text-only baseline.
Ridge regression could provide a simple regularized comparison for numeric
ratings; random forest could test more flexible relationships once data and
labels are adequate. Fit preprocessing and choose hyperparameters inside
training folds only. Use student-grouped evaluation, additional held-out
texts, uncertainty estimates and an explicit comparison with the baselines.
More complexity cannot replace missing labels or unvalidated measurements.

The success criterion should be useful additional evidence for teachers,
supported on new students—not merely a model that fits this small pilot.
