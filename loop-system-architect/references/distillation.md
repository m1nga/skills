# Experience Distillation and Controlled Evolution

## Keep six stores distinct

1. **Raw evidence**: immutable inputs, tool traces, outputs, diffs, screenshots, and outcomes.
2. **Episodic memory**: one normalized summary per run, scoped to loop/tenant/task.
3. **Candidate lessons**: hypotheses about what may be reusable; never treated as fact.
4. **Canonical knowledge**: verified descriptive facts and patterns with provenance and expiry.
5. **Procedural skills**: executable methods with capability contracts and evals.
6. **Evaluation assets**: fixtures, counterexamples, rubrics, regression tests, and expected evidence.

Do not let raw logs become an always-loaded prompt. Retrieve the minimum context by task, tenant,
role, recency, sensitivity, confidence, and provenance.

## Candidate record

Record:

- candidate ID and type (`knowledge`, `rule`, `sop`, `script`, `skill`, `trigger`, `retrieval`);
- scope (`platform`, `domain`, `tenant`, `loop`, `task`);
- source run IDs and evidence hashes;
- observed outcome and delay window;
- proposed change and predicted benefit;
- confidence, counterexamples, and known confounders;
- protected fields touched;
- validation plan, promotion authority, and rollback target.

## Trigger evolution from evidence

Useful triggers include:

- the same failure class repeats;
- the same manual step repeats;
- cost or latency regresses;
- state/context grows past budget;
- a source or environment drifts;
- a promoted change underperforms;
- enough comparable outcomes exist to evaluate a pattern.

An arbitrary “every N runs” may schedule a review, but never proves a change deserves promotion.

## Validate before promotion

1. Deduplicate against current knowledge and open candidates.
2. Identify conflicts and which authority owns them.
3. Replay on historical fixtures, including failures and counterexamples.
4. Run deterministic and semantic evals with fixed versions.
5. Shadow the change without side effects when possible.
6. Canary on a bounded scope with guardrail metrics.
7. Promote one version atomically.
8. Monitor a defined outcome window.
9. Keep or rollback; append the decision and evidence.

## Prevent self-corruption

The evolution agent may propose changes to protected fields, but it cannot promote them. It must not:

- change the objective to match observed output;
- weaken the verifier or remove hard failures;
- broaden its own data/tool authority;
- merge tenant-specific learning into platform knowledge without isolation and validation;
- promote a single successful episode as a universal rule;
- hide old active truth instead of removing it from retrieval.

## Retrieval contract

Create a minimal task context packet containing:

- active mandate/policy and runtime scope;
- current verified facts;
- relevant canonical knowledge;
- selected skill contracts;
- recent task state and unresolved failure;
- acceptance checks.

Exclude unrelated tenants, raw history, inactive versions, rejected candidates, and embedded identity
from context-bearing skills unless explicitly authorized as evidence.
