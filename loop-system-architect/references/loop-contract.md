# Machine Loop Contract

The human-readable contract explains intent. `loop.contract.json` is the canonical runtime input.
Keep runtime state and append-only events outside the contract.

## Required sections

### Identity

- `schema_version`: contract schema version.
- `loop_id`: stable, lowercase identifier.
- `mode`: `terminal` or `recurring`.
- `status`: `draft`, `active`, `paused`, `retired`.

### Objective

- `statement`: what the loop changes or maintains.
- `owner`: authority over the objective.
- `completion_condition`: required for terminal loops.
- `per_run_success`: required for recurring loops and recommended for terminal loops.
- `non_goals`: excluded outcomes.

### Source policy

List authoritative sources, reference-only sources, prohibited context classes, provenance
requirements, and a freeze/version/hash mechanism. A clean-room source boundary is a provenance
policy, not a static skill allowlist.

### Control

- `sensor`: signal, collection path, freshness.
- `comparator`: rule and evaluation window.
- `controller`: finite decision space.
- `actuator`: allowed actions and feedback path.

### Triggers

Each trigger declares type (`continuous`, `schedule`, `event`, `hybrid`, `manual`), condition,
cheap preflight, dedupe key, and disabled/retirement behavior. Use code to decide whether work exists
before waking an LLM when possible.

### State

Declare state path/store, cursor fields, event log, evidence store, atomic-write method, and recovery
method. Runtime state should contain run ID, state/status, attempt, source hash, lock/lease, last error,
accepted artifacts, and a machine-readable next action.

### Roles

Declare responsibilities and write/decision boundaries. Orchestrator, executor, and verifier may be
separate models or constrained roles, but the verifier cannot certify its own writes.

### Capabilities

Declare open discovery, search locations, capability-contract matching, candidate creation,
sandboxing, evals, local registration, versioning, and rollback. Do not confuse discovery freedom
with execution authority.

A loop that never needs new capabilities may declare `discovery: "none"` with a non-empty
`reason`; the linter then waives `candidate_creation` and `sandbox_required`.

### Authority

List autonomous actions, approval-required actions, and protected fields. At minimum protect the
objective, source policy, authority model, tenant/privacy boundaries, and acceptance definition from
silent evolution.

### Verification

Declare deterministic checks, semantic checks, evidence requirements, independence, and the exact
pass rule. Include fail-closed tests, not only a happy path.

### Failure policy

Declare maximum attempts, same-failure limit, timeout, backoff, classification, exhaustion behavior,
rollback, pause, kill, and incident/dead-letter recording.

### Budgets

Declare turns, tokens, cost, and wall time. Use null only when the enclosing runtime has a documented
hard limit; do not treat an absent limit as infinite permission.

### Runtime safety

Declare idempotency key, dedupe store, concurrency lock, side-effect choke point, tenant scope,
secret handling, and fail-closed policy.

### Observability

Declare status surface, metrics, and alerts. Include pass/fail/no-op counts, cost, latency, retries,
drift, and promotion/rollback outcomes when applicable.

### Replacement

Declare single-current-version enforcement, impact scan, stale/contradiction scan, zero-context probe,
atomic promotion, and inactive history location.

### Learning

Declare triggers, typed storage layers, candidate generation, conflict checking, replay/evals,
shadow/canary, promotion authority, monitoring, rollback, and protected fields.

A minimal-profile loop may declare `enabled: false`; the linter then waives the remaining
learning fields.

### Retirement

Declare conditions and cleanup for triggers, locks, secrets, active state, knowledge visibility, and
outstanding side effects.
