# Loop Audit Rubric

Use this rubric to distinguish an executable loop from a persuasive process document.

## 1. Control closure

| Check | Pass evidence | Typical failure |
|---|---|---|
| Set point | Named objective and owner | Broad aspiration |
| Finish/run success | Machine-checkable or evidence-checkable condition | “Agent decides when done” |
| Sensor | Named signal and collection path | Metrics listed without ingestion |
| Comparator | Rule/window/threshold tied to objective | Data collected but never compared |
| Controller | Finite decisions and authority | Free-form agent discretion |
| Actuator | Named action with side-effect path | Recommendation only |
| Feedback | New result returns to the sensor | One-time adjustment |

Classify terminal and recurring loops separately. A recurring loop has no overall finish line,
but every run must terminate with pass, no-op, retry, rollback, or stopped.

## 2. Operational reality

Fail the operational claim if the normal path requires a person to:

- copy a prompt between windows;
- remember which state comes next;
- translate a verifier paragraph into a state transition;
- manually collect evidence already available to the system;
- prevent duplicate execution by memory;
- decide whether a retry is the same failure class.

Accept a manual gate only when the contract explicitly assigns the underlying decision authority to
the human. Prompt ferrying is not an authority decision.

## 3. Persistence and recovery

Require:

- atomic state writes;
- schema/version field;
- run ID, loop ID, state, status, attempt, and timestamps;
- current step and next machine action;
- accepted artifact/evidence references and hashes;
- failure class and last error;
- source snapshot/hash;
- concurrency lease/lock;
- append-only event history;
- recovery test after deliberate interruption.

Do not use a prose `next_action` as the only controller interface.

## 4. Verification integrity

Require the verifier to be independent of the write being certified. Prefer deterministic checks
first and semantic judgment second. Record:

- exact check version;
- inputs and artifact hashes;
- pass/fail per criterion;
- evidence references;
- verifier identity/model/tool;
- timestamp and cost;
- repair routing decision.

Self-review may improve work but never replaces the independent gate.

## 5. Source and context integrity

Require source claims to be auditable against primary excerpts or records, not merely against a
second-order summary. Freeze or version accepted source packets. Distinguish:

- authoritative facts;
- user-owned decisions;
- hypotheses;
- external proposals;
- raw evidence;
- deprecated or quarantined history.

Global instructions and context-bearing skills are ambient inputs even when a prompt says “read
nothing else.” Add project adapters and provenance checks instead of claiming impossible isolation.

## 6. Failure safety

Check timeout, bounded attempts, backoff, same-failure detection, rollback, dead-letter/incident
recording, kill/pause, and fail-closed behavior. Exercise at least one injected failure.

## 7. Side-effect safety

Check idempotency keys, event deduplication, concurrency locks, authority derived from owned data,
single outbound choke point, tenant isolation, and secret handling.

## 8. Capability and skill lifecycle

Open discovery must still define capability contracts, provenance inspection, sandboxing, evals,
local registration, versioning, rollback, and removal. A skill name in a plan is not a working
capability.

## 9. Learning and replacement

Require raw trace → outcome → candidate → validation → promotion → monitoring → rollback. Confirm
that protected fields cannot be silently changed. Confirm old active truth is removed everywhere and
that a zero-context probe retrieves only the new version.

## 10. Observability and retirement

Require a status surface showing current state, last pass/failure/no-op, attempts, cost, latency,
open incident, and next action. Define pause, kill, and retirement conditions plus cleanup of triggers,
credentials, locks, and active retrieval entries.

## Verdict levels

- **OPEN LOOP**: one or more control elements are missing.
- **DOCUMENTED LOOP**: control design exists, but execution still depends on manual orchestration.
- **RUNNABLE LOOP**: one command/event advances state with persistence and evidence.
- **RELIABLE LOOP**: recovery, dedupe, failure paths, independent verification, and observability pass.
- **EVOLVING LOOP**: a candidate improvement has been validated, promoted or rejected, and measured.
