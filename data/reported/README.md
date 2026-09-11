# Reported aggregates: read these separately from application data

These four tables transcribe findings from the supplied paper and reports.
They are **not individual survey responses** reconstructed from the app CSVs.
Source IDs refer to the [source register](../../docs/source-register.md).

| Table | Contents | Source |
|---|---|---|
| [normal_strategy_counts.csv](normal_strategy_counts.csv) | Six strategy categories totalling 200 reports from 20 students | SURVEY §4.2; PAPER Table 1 |
| [normal_ratings.csv](normal_ratings.csv) | Three designed-difficulty groups, 199 records, reported mean difficulty and effort | SURVEY §4.2; PAPER Table 1 |
| [instruction_strategy_counts.csv](instruction_strategy_counts.csv) | All 16 cells of the assigned-instruction × self-reported-strategy table, including zeros | SURVEY Figure 3 |
| [webcam_configurations.csv](webcam_configurations.csv) | Eight camera-test configurations with context, resolution and FPS | CAMERA Appendix A |

`group_records` is the reported group size; the available files do not establish
the nonmissing count for every separate rating. One of 200 normal-reading
records lacked a designed-difficulty label. Values such as 2.20 are published
rounded means, not raw ratings. Do not create 199 artificial individual ratings
from those means or treat aggregate cells as independent learners.

For instructed reading, the matrix totals 70 responses. Restricting assigned
instructions to SKIM, SEQ and DEEP leaves 55 responses; 17 + 16 + 4 = 37 have
the same reported strategy. **37 / 55 = 67.3% instruction–survey agreement**.
The excluded 15 OTHER assignments are not an intended instruction condition.
This calculation compares an instruction with a survey response, not a webcam
prediction with a survey response.

Camera codes C01–C08 identify configurations, not students or sessions. There
is no camera-to-session mapping in the release. A/B distinguish two entries
with the same Integrated Camera label; they are not manufacturer model names.
The minimum screen used here is width ≥ 1280 pixels, height ≥ 720 pixels and
FPS ≥ 20. The preferred screen is width ≥ 1920, height ≥ 1080 and FPS ≥ 25.
These are study criteria, not demonstrated spatial accuracy requirements.
