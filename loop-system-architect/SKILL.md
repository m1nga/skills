---
name: loop-system-architect
description: Design, audit, repair, and operationalize reliable agent loops with explicit goals, triggers, persistent state, orchestration, independent verification, failure recovery, open skill discovery or creation, controlled self-improvement, and retirement conditions. Use to build a loop, an autonomous or recurring agent workflow, a multi-agent operating system, a self-improving process, a zero-context recovery flow, a permanent update/replacement loop, or to turn a prose plan or repeated prompt into a genuinely executable loop. Trigger on natural phrasings such as "I keep running this prompt by hand — automate it", "make this agent run on its own and check its own work", "why does my automation silently fail", and Chinese phrasings such as "把这个流程变成自动循环", "帮我设计一个自动跑的 agent 工作流". For a plain scheduled reminder or interval re-run without state or verification, use the host scheduler (cron/schedule tools) instead. For static product architecture and responsibility contracts, use map-product-system.
---

# Loop System Architect

Turn a repeated task into an observable control system that can execute, prove its result,
recover after interruption, and improve without rewriting its own purpose.

## Choose the mode

- **Audit**: inspect an existing workflow and report missing or open-loop parts. Do not edit unless asked.
- **Design**: produce the contract, state schema, role graph, evals, and runtime design.
- **Operationalize**: implement the controller, adapters, persistence, evidence, and one-command run path.
- **Evolve**: analyze completed runs, validate a proposed loop/knowledge/skill improvement, and promote or reject it.

When the user asks to “build” or “get it working,” include Operationalize. A Markdown plan alone
is not an operational loop.

## Start from live reality

1. Read repository instructions and the artifacts the user placed in scope.
2. Inspect the actual tools, entry points, state files, tests, schedulers, agent CLIs, and dirty worktree.
3. Separate current authoritative input from reference material. Do not use model memory to fill gaps.
4. Classify the loop:
   - **Terminal**: one goal with a demonstrable finish line.
   - **Recurring**: every run terminates, while the monitor/service continues until retired.
5. State what exists, what is missing, and what is only claimed before changing anything.

For a full audit, read [audit-rubric.md](references/audit-rubric.md).

## Require a closed control loop

Identify and connect all of these:

1. objective and owner;
2. completion condition or per-run success condition;
3. authoritative source boundary and provenance;
4. trigger and cheap preflight;
5. sensor and collected signal;
6. comparator, window, and threshold/rule;
7. controller and finite decision space;
8. actuator and the path that returns the new result to the sensor;
9. persistent state, cursor, event log, and evidence store;
10. orchestrator, executor, and independent verifier responsibilities;
11. open capability/skill discovery and candidate-skill creation;
12. authority boundaries and protected fields;
13. acceptance evals and required evidence;
14. retries, timeouts, backoff, failure classification, and rollback;
15. idempotency, deduplication, concurrency lock, and side-effect choke point;
16. token, cost, turn, and wall-time budgets;
17. observability, alerts, and a no-op success state;
18. direct replacement of superseded active truth;
19. experience distillation and controlled promotion;
20. stop, pause, kill, and retirement conditions.

Missing sensor-to-actuator feedback means open loop. Missing persistent state means a repeated
prompt. Missing verifier evidence means self-asserted completion. Missing a controller/trigger
means a procedure humans must operate.

## Minimal profile

Not every loop needs all twenty elements. For a single-operator, cron-grade loop — one user, one
machine, low blast radius, no shared side effects — a contract is sufficient with eight:

1. objective and owner;
2. success condition (completion or per-run);
3. trigger and cheap preflight;
4. actuator and its side-effect path;
5. persistent state and cursor;
6. idempotency/dedupe on the side-effect path;
7. observability: where to see the last result and next action;
8. retirement condition.

Declare the omissions explicitly instead of leaving them blank: set `learning.enabled: false`,
and set `capabilities.discovery: "none"` with a `reason` field. The linter accepts both. See
[loop.contract.minimal-example.json](assets/loop.contract.minimal-example.json) for a passing
minimal contract. Upgrade to the full contract when the loop gains shared side effects, a second
operator, external tenants, or any form of self-modification.

## Produce a loop package

Adapt names to the repository, but keep one canonical machine-readable contract and one state
record. Loop packages, state, and evidence live in the user's project, never inside this skill
package. The default package is:

```text
loop/
├── LOOP-CONTRACT.md          human-readable operating contract
├── loop.contract.json       machine-readable canonical contract
├── RUN-STATE.json           current run, cursor, attempts, next machine action
├── events/                  append-only run events or an equivalent event store
├── evidence/                verifier-readable receipts
├── evals/                   deterministic and semantic acceptance checks
├── knowledge/               typed promoted knowledge, not raw logs
├── candidates/              unpromoted lessons and skill changes
└── scripts/run-loop         one-command controller or project-native equivalent
```

Use [loop-contract.md](references/loop-contract.md) for the field contract. Copy
[loop.contract.template.json](assets/loop.contract.template.json), fill every placeholder,
then run:

```bash
python3 scripts/loop_lint.py /path/to/loop.contract.json
```

Use the copy inside this skill when the project has not vendored the linter. If nothing can be
written to disk, output the contract and controller as copyable text and say what remains to be
placed on disk before the loop is operational.

## Build the controller, not only the instructions

The controller must make one invocation advance the loop without asking the user to copy and
paste between agents:

1. acquire a concurrency lock and derive an idempotency key;
2. load and lint the contract and state;
3. verify frozen-source hashes or current source authority;
4. run the cheap trigger/preflight and record a no-op success when no work exists;
5. resolve required capabilities;
6. create a minimal context packet for the orchestrator/executor;
7. execute in an isolated workspace when changes are possible;
8. capture outputs, costs, tool calls, diffs, and evidence;
9. run an independent verifier that cannot certify its own writes;
10. on failure, classify and route a bounded repair, retry, rollback, or stop;
11. on pass, atomically promote the result and update current state;
12. append an immutable event/receipt;
13. invoke distillation only when its trigger is satisfied;
14. release the lock and expose the next machine-executable action.

Minimal verifier independence, by engine:

- **Claude Code (or any runtime with subagents)**: run the verifier as a fresh-context subagent
  that receives only the contract, the acceptance checks, and the evidence paths — not the
  executor's conversation.
- **No subagent mechanism**: run the verifier as a separate process or separate invocation that
  re-reads the evidence from disk and returns a verdict against the acceptance checks.
- **Neither available**: the same context checking its own work is self-review — performance,
  not verification. Say so in the audit instead of labeling it a verifier.

Prefer deterministic code for triggers, state transitions, schema checks, permissions, retries,
hashes, and promotion. Use LLMs for judgment, planning, diagnosis, and content that cannot be
decided mechanically.

## Discover or create skills without a static allowlist

Use open discovery with controlled execution:

1. Derive a capability contract from the task: input, output, side effects, evidence, risk.
2. Search installed skills and project capabilities by metadata and contract fit.
3. Inspect provenance and dependencies; do not import embedded project identity as truth.
4. Sandbox a candidate skill and run capability-specific evals.
5. If none fits, create a candidate skill in isolation with its own examples and evals.
6. Promote a version only after it passes security, privacy, functional, and regression checks.
7. Register locally by default. External publication follows the owning environment's separate policy.

Open discovery does not grant open authority. Mandates, data scope, side-effect policy, and runtime
permissions still constrain every skill.

## Distill experience into usable knowledge

Never feed an ever-growing log to every agent. Keep raw evidence, episodic summaries, candidate
lessons, canonical knowledge, procedural skills, and evals separate.

Run the promotion path:

```text
trace + outcome
→ normalized episode
→ candidate lesson
→ deduplicate and conflict-check
→ replay against prior runs and counterexamples
→ shadow or canary
→ promote a version
→ monitor the next runs
→ keep or rollback
```

Trigger distillation on repeated failure, repeated manual work, drift, cost regression, meaningful
outcome evidence, or a configured sample size—not merely because time passed. Read
[distillation.md](references/distillation.md) before designing or changing the learning layer.
If a dedicated distillation skill (such as experience-pack) is installed, let it own the
distillation workflow itself; this skill designs the loop that invokes it.

The evolution process may improve SOPs, triggers, context packing, scripts, skills, retrieval, and
operational thresholds within delegated authority. It may not silently rewrite the objective,
source boundary, tenant/privacy boundary, authority model, or the eval that defines success.

## Replace active truth cleanly

For any accepted update:

1. compute the impact graph across contract, state schema, code, tests, docs, views, and skills;
2. declare `REPLACES`, `REMOVES`, and `KEEPS`;
3. update all dependents;
4. remove superseded wording and values from active retrieval;
5. run contradiction/stale-value scans;
6. run affected happy and failure-path evals;
7. run a zero-context probe that must recover exactly one current answer;
8. promote atomically; retain prior versions only in version control/event history, not active context.

## Calibrate autonomy

- Auto-run reversible, bounded actions when deterministic and independent verification passes.
- Use canary, shadow, dual verification, and rollback for higher-risk automated actions.
- Stop for the user only when authority is missing, a required decision changes the objective,
  or the action is materially irreversible and not already authorized.
- Never make routine human approval a hidden actuator in a loop advertised as autonomous.

## Verify completion

Do not call the loop operational until all are true:

- one command or configured event can advance it without prompt ferrying;
- interruption recovery resumes from persisted state without redoing accepted work;
- duplicate triggers cannot duplicate side effects;
- verifier failure causes bounded repair or a clean stop;
- both success and fail-closed paths have evidence;
- a no-work run terminates successfully and cheaply;
- the current status, last result, cost, open failure, and next action are observable;
- one evolution candidate has been replayed and either promoted or correctly rejected
  (waived under the minimal profile with `learning.enabled: false`);
- a zero-context agent can explain the current contract and next action from active files alone.

Report separately: what is implemented, what was exercised, what remains dormant for lack of a
live sensor, and what still requires the user's authority.
