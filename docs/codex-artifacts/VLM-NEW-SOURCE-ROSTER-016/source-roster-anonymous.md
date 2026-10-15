# VLM-NEW-SOURCE-ROSTER-016 — anonymous metadata roster

2026-10-15 (Asia/Shanghai). Documentation main `4d9e2e3e8d3d47cbf403448da03520c2c922f018`; unique READY, no previous 016 result. **METADATA_ROSTER_COMPLETE / RELEASE1_METADATA_CANDIDATES / MEDIA_AVAILABILITY_NOT_TESTED.** Six conditional candidates are frozen; R1–R3 are preparation priorities. This is not permission or evidence for a new GPU experiment.

## Authorized inputs and discovery

The user explicitly authorized CPU-only existing metadata review and subsequently instructed a filename search in two named local directories. This expanded the previous exact-path-only discovery restriction; no unrelated directory search was performed. Only the supplied download root, its identifiable HourVideo sample/release/full-scale branch, and the supplied model root were listed. No model files or videos were opened. The existing metadata inputs were found in the first directory; the second contained model directories, which were not traversed.

| Private input role | Entry status | Scope |
|---|---|---|
| HourVideo dev annotation metadata | Exact regular file identified; 50 video records | Video metadata, categorical task fields and structural QA qualification only |
| Existing official-source manifest in release-1/full-scale directory | Exact regular CSV identified; 9,645 unique video rows | Canonical identity, origin/source grouping, release/validation flags and declared duration |
| Existing sample metadata and UID list | Two entries; both sets agree | Exclusion of the two already observed sources only |

The user's attestation of previously lawful acquisition/use is retained. Official-shaped canonical source references and release flags support a metadata-level source association; they do not independently prove current remote entitlement, immutable manifest provenance, object availability or applicable per-object permission. No credentials, remote entitlement, HEAD, CLI download or network source verification was attempted.

## Frozen non-answer procedure

Before ranking, the procedure was fixed as follows: exclude the two sample identities and any manifest row sharing their recorded `(video_source, origin_video_id)` group; require a matching manifest record, declared duration at least 1,200 seconds and at least 10 structurally qualified non-image tasks. Prefer release-1/canonical-validation evidence, then nonempty distinct recorded source groups, then descending structural question count, then comparable known byte size ascending, then qualifying duration ascending, then deterministic UID lexical order. Unknown comparable size is tied, not treated as zero. Retain at most one candidate per recorded group and at most six total; preparation priorities are the first three, without later swapping based on outcomes or convenience.

Question qualification checked a matching video identifier, a nonempty string question field, five nonempty string option fields, a string-typed gold-label field, and a categorical task without the explicit image marker. **No question/option/answer string value, reference timestamp value, canary or model prediction was decoded, materialized or displayed.** A streaming structural parser traversed those JSON string tokens without retaining their contents. Only permitted video identifiers/durations and task categories were interpreted. A synthetic sentinel check confirmed that protected question/label/option values were absent from the retained representation.

These counts are **schema-qualified non-image task counts, not final certified scorable denominators**. The permitted structural check cannot establish that gold values encode valid A–E labels, that reference answers are semantically correct, or that apparently textual questions have no additional asset reference inside their text. The 013 full eligibility rule included such a text-level exclusion; this restricted audit cannot reproduce that part and does not claim to. Final asset-free eligibility and scoring certification remain UNKNOWN under this authorization. Neither labels nor expected model difficulty determined the ranking.

## Candidate pool and exclusions

- All 50 dev identities join uniquely to the 9,645-row manifest. All 50 have annotation-declared duration at least 20 minutes.
- The two existing sample identities agree between the two exclusion inputs and occur in both dev metadata and manifest. They are excluded. Recorded old-source group matching added zero further exclusions; this does not prove absence of undisclosed physical overlap.
- One of the 48 remaining records has fewer than 10 structurally qualified non-image questions. The resulting metadata pool contains **47 records / 47 distinct recorded source groups**.
- All manifest rows have explicit `release_1=True` and `canonical_is_validated=True`. All six selected candidates have official-shaped canonical S3 source references and exactly matching annotation versus canonical-MP4 declared durations. This is stronger release-1 metadata evidence than a v2_1 UID intersection alone. It is not a remote v1 download test or independent release/crop/time-origin certificate.
- The manifest contains **no file-size/byte-count field**. Expected full-scale object bytes and total download/storage budget are **UNKNOWN for every candidate**. No bandwidth estimate or byte-size ranking was manufactured from duration, resolution or frame count.

## Frozen anonymous roster

| Rank | Original questions | Explicit image-task exclusions | Structural non-image MCQ count | Declared duration, minutes | Full-scale bytes | Preparation priority |
|---|---:|---:|---:|---:|---|---|
| R1 | 39 | 0 | 39 | 46.39 | UNKNOWN | First |
| R2 | 39 | 0 | 39 | 73.28 | UNKNOWN | Second |
| R3 | 41 | 3 | 38 | 50.05 | UNKNOWN | Third |
| R4 | 36 | 0 | 36 | 62.01 | UNKNOWN | Reserve |
| R5 | 35 | 0 | 35 | 59.76 | UNKNOWN | Reserve |
| R6 | 34 | 0 | 34 | 58.46 | UNKNOWN | Reserve |

R1–R3 are conditional preparation recommendations under the frozen evidence/count-first order, not a claim that they are the cheapest downloads. R2 remains ahead of the shorter R3 because question count precedes unknown byte cost and duration in the contract. All six have distinct recorded origin/source groups and no recorded group match to the excluded samples. **Strict physical-capture independence remains unverified**; different identifiers/source groups do not certify different real events.

For every row: `RELEASE1_METADATA_ASSOCIATION_SUPPORTED`, `CURRENT_DOWNLOAD_ENTITLEMENT_NOT_INDEPENDENTLY_TESTED`, `OBJECT_BYTES_UNKNOWN`, `FINAL_SCORABLE_N_UNKNOWN`, and **VERSION_BRIDGE_UNKNOWN / CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**. Canonical validation is the manifest publisher's flag, not this round's pixel/PTS validation. There is no claim of a formally certified same-release scoring candidate. The current pool is not solely a v2_1-only pool, so the conditional v2_1-only rejection rule was not used to erase the observed release-1 evidence.

## Private handoff and manual download plan

Exact candidate identities and the first three single-identity command templates are provided only in the private Codex response. No identity mapping, object key, endpoint or media path is published here. Public command shape:

```text
ego4d --output_directory "<PRIVATE_DEST>" --datasets full_scale --version v1 --video_uids "<AUTHORIZED_UID>"
```

This is an **unexecuted template**: local CLI availability and installed-version `--help` semantics were not tested. The user must first confirm their existing official access, locally supported flags, available storage and an acceptable object-size/transfer budget. Do not treat old v2_1 HEAD sizes as v1 sizes. Do not install a CLI or initiate requests on the strength of this report. If using an existing authorized official CLI, request one frozen candidate at a time, retain its release/source record and verify completeness before considering another. No automatic download, mirror substitution, retry, old partial-file recovery or replacement-source search is authorized by 016.

New complete media still require source-overlap, release/crop/time-axis and final eligibility checks under a separately defined scope. Any assumption-limited future evaluation must state that limitation prospectively. A new source-level analysis plan, strong comparisons, independent-data/power rationale and explicit new GPU budget are prerequisites; 013/014 permissions are consumed. No training or parameter selection on the observed sources is admitted.

## Verification, preservation and stop

CPU stdlib checks passed for unique joins, the corroborated two-source exclusion set, deterministic ranking, six distinct recorded groups, no selected old identity/group, and exact selected annotation/manifest duration equality. Sensitive-value sentinel checks passed. No private source text or labels were reconstructed for verification. The metadata inputs, historical experiments and planning documents were not modified.

This round used **0 GPU/model calls, 0 video decode, 0 research network/AWS requests, 0 media/model downloads, 0 training and 0 dependency/environment changes**. Only Git documentation coordination used network access. Publish only this anonymous report and one appended 016 result, with a single ordinary main push, then stop. **PAUSE_FURTHER_GPU; NOVELTY=RETAIN0; Charades FINAL_MEDIA_STOP** remain.
