# Release preparation and remaining author decisions

## What this candidate contains

Version **0.1.0-rc1**, prepared 11 September 2026 for the repository named in
the paper: [duongtrung/DELFI2026](https://github.com/duongtrung/DELFI2026).
The existing repository was inspected at commit
`5af4585f91c66ebfc0e1ac8c6ac4396265852341`. It contained a two-line README and
a GNU GPL version 2 LICENSE. This candidate preserves that license file
unchanged and replaces the README with study and data documentation.

The candidate has not been pushed, merged, tagged or published. Treat it as a
reviewable release folder. Do not describe it as a public archived dataset yet.

## What was done to the participant-level records?

| Original information | Candidate handling | Effect on reuse |
|---|---|---|
| Session and app-user identifiers | Replaced with new S/U codes using keyed ordering; original null app ID stays blank | Known within-app links remain; no claim about true personal identity |
| Original row IDs | Removed; events use a within-session sequence number | Original database keys are not exposed |
| Calendar start/finish times | Removed | Exact attendance dates and elapsed session durations cannot be reconstructed from those fields |
| Browser/user-agent strings and exact viewports | Removed | Device fingerprint details and layout analysis are reduced |
| AOI word strings and numeric IDs | Replaced by broad category and within-session-step code | Repeated software assignments can be counted; words and global AOI identities are not supplied |
| Event start/stop clocks | Rebased so each session's first event begins at zero | Event durations, gaps and order are retained; the original clock origin is not exposed |
| Question steps, scores and phase labels | Retained | Scoring and phase-specific auditing remain possible |

All 60 sessions, 1,880 step rows and 92,138 events are retained. There is no
identity mapping, private pseudonymization key, video or facial image in the
package. Removing identifiers does not establish anonymity: distinctive
behavioral patterns and repeated sessions can still be linkable. The release
should be described as **pseudonymized and minimized**.

## Public sharing and reuse terms

The paper reports ethics approval, but the supplied materials do not include
the approved consent form or a statement establishing permission for public
redistribution of participant-level records. Before publishing these prepared
CSVs, the responsible investigator needs to confirm that this form of public
sharing is covered. This is a specific missing source document, not a finding
that the study lacked approval.

The original repository's GPLv2 text remains the code license. No separate
open-data license has been selected on the authors' behalf. See
[DATA_LICENSE.md](../DATA_LICENSE.md). The authors need to specify the scope
and terms for data and documentation; do not imply that ethics approval or a
software license supplies participant permission. If public row-level sharing
is not covered, keep those records under the approved access arrangement and
release documentation, code and appropriate aggregates instead.

The original paper PDF, full reports, reading passages, question wording,
logos and borrowed presentation illustrations are not bundled. The guide
summarizes the supplied evidence. Add original materials when their public
distribution terms are established. Full passages, question/answer keys,
original survey instrument/workbook and original application source were not
available for this preparation.

## Finalize the repository

1. Confirm the participant-data sharing basis and document the dataset reuse
   terms. Resolve the paper's calibration statement and the normal-reading
   text-visibility discrepancy, retaining a transparent correction note.
2. Confirm the final paper citation and whether the author list in
   `CITATION.cff` also represents the dataset's contributors. Add the DOI or
   proceedings URL when known; the current metadata deliberately omits them.
3. Install and connect GitHub, then review the changes against the repository's
   current main branch. This candidate targets the commit recorded above;
   preserve any newer work rather than overwriting it.
4. Run the documented validation and tests. After author review, remove the
   release-candidate status, update the data terms and publish a versioned
   release. Record its actual release date and tag in the citation metadata.

The prepared files can be copied into a working checkout as ordinary files.
The package intentionally contains no `.git` history or authentication data.
When updating a live repository, use a review branch and inspect the diff;
do not force-push over an existing branch.
