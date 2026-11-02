# 077 admission: execution stopped before construction

**EXECUTION_STOP_BOOTSTRAP_THREAD_LIMIT / METADATA_CONSTRUCTION_NOT_RUN / RGB_NOT_CONSTRUCTED / TRAINING_NOT_RUN**. This is an actual resource-gate failure, not missing input, an empty valid dataset, a scientific negative, or completed metadata admission.

The supplied archive was accessible. Before the formal attempt, the ZIP length (390,919 B) and SHA256 (`950ae2f6766179743f27e512948730682e444eb1c235393d034e508081224cd2`) matched the contract. The outer directory lists 12 members / 1,104,895 declared uncompressed bytes; the inner annotation archive directory lists the single expected JSON / 2,692,679 declared bytes. Preflight inspected only archive identity/directories and source description/registration/rule metadata. It did not parse action annotations or the owner's frozen selection. Full extraction, every-member manifest/CRC verification and original annotation content verification were not reached.

## Actual stopping evidence

The Windows Job supervisor observed **4 threads in one owned process versus the contract limit of 1**, at bootstrap. It terminated only its own Job. Actual outer time was **0.125 s / 300 s**, peak Job commit **11,276,288 B / 1 GiB**, observed active processes **2 / 2**, exit code **99**, killed=true, final actual active=0. Thread snapshots count native process threads; they do not establish four active scientific compute threads. The contract's literal thread gate nevertheless failed. The environment and limits were not changed; no retry was made.

No fixture result, extracted packet member, construction STARTED marker, source-row ledger, selected manifest, answers, relations, dataset independent review, owner comparison or final science summary exists. Thus constructed groups/variants/answers/relations are **0 actual outputs**, while source counts, eligibility, split membership, selected media sizes, owner agreement and dataset qualification are **NOT_RUN/NA**, never validated zero counts. The formal read counter also was not reached. Exact OS input-access history is unknown; absent durable user-code markers are not a comprehensive OS access audit.

## Targets remain declarations

The README/owner preview declares 2,135 source videos / 13,644 actions, 1,376 candidates / 280 eligible videos, 32 selected groups, 20/4/8 split, 29 texts, 192 variants / 1,152 symbolic answers / 2,304 relations (768 FLIP, 1,536 HOLD). Media reference totals are 581,426,975 compressed / 579,702,574 uncompressed bytes, maximum compressed member 70,872,100 bytes. **None of these dataset counts, members or rankings was independently reconstructed in this execution.** The four CSV rows preserve planned denominators and explicitly separate zero constructed outputs from unknown eligibility.

## Verification scope and remaining work

The full constructor and rational independent oracle were sealed before annotation/selection access. Their software fixture and formal execution were **NOT_RUN**. A separate **post-stop bookkeeping check (22 checks)** confirmed the Job failure, final active0, absent outputs and unchanged science/supervisor seals. It did not invoke the producer, parse annotations, reproduce selection, or certify the data. It is not the presealed dataset review or an independent rerun.

Required remaining work: successful newly authorized metadata admission and full independent construction; only after that, a separately approved integrated RGB/features/training package. [Training proposal](./training-plan.md) is conditional on such admission and new resources. This parent is closed, not silently repaired or restarted.

Perception Test data are CC-BY-4.0 and software Apache-2.0. Attribution: Google DeepMind, [official fixed source](https://github.com/google-deepmind/perception_test/tree/3938d2f1ba3a6b502025741cea4cd73c7b3bdfaf). Source labels describe annotated action-segment appearance order, not certified atomic completion or unique physical occurrence. Perception Test is also a TOC-Bench source; original recording/participant/pixel/pretraining overlap remains UNKNOWN. No new blind test or core innovation is established. RGB/PTS/model performance are NOT_RUN; 070 remains closed and 069 paused.
