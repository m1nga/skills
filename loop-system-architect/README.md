# loop-system-architect

Turns "I keep running this prompt by hand" into a loop that executes, proves its result, and recovers after interruption — with a linter that fails contracts that only look complete.

## What it does

Designs, audits, repairs, and operationalizes agent loops as closed control
systems: sensor, comparator, controller, actuator, and the feedback path back
to the sensor — plus persistent state, independent verification, failure
classification, budgets, and retirement conditions. Ships a machine-readable
contract template and a deterministic linter (`scripts/loop_lint.py`) that
rejects placeholder-ware, and an audit rubric whose verdict ladder (OPEN LOOP
to EVOLVING LOOP) tells you honestly what you have. A minimal profile covers
solo cron-grade loops with eight required elements instead of twenty.

## When it fires

- "I keep running this prompt by hand — automate it."
- "Make this agent run on its own and check its own work."
- "Why does my automation silently fail?"
- "Turn this runbook into something that actually runs."
- 「把这个流程变成自动循环」
- 「帮我设计一个自动跑的 agent 工作流」

It is not for plain reminders: a scheduled re-run with no state and no
verification belongs in your host scheduler (cron, schedule tools). Static
product architecture is [`map-product-system`](../map-product-system/);
knowledge distillation as its own workflow is
[`experience-pack`](../experience-pack/).

## Install

```
npx skills add ming4uk/skills@loop-system-architect
```

## Example

> **User:** Every night I paste the same prompt to scan our docs for broken
> links and copy the result into an issue file. Automate this.
>
> **Agent:** Classifies it as a recurring loop, writes `loop.contract.json`
> under the minimal profile (learning off, capability discovery "none" with a
> stated reason), runs it through `loop_lint.py` until it passes, then builds
> a one-command controller with a lock file, a per-run dedupe key, atomic
> state writes, and a verifier that re-reads the scan report instead of
> trusting the executor's summary. A night with no changes terminates as a
> cheap recorded no-op — not a silent skip.

## Works well with

- [`map-product-system`](../map-product-system/) — draws the static
  architecture that tells you which capabilities deserve a loop at all.
- [`experience-pack`](../experience-pack/) — owns lesson distillation as a
  standalone concern; this skill's learning layer hands off to the same
  promotion discipline instead of reinventing it.

## Design notes

- **Self-asserted completion is the core failure.** The linter hard-requires
  a verifier that cannot write the work product, because the loops this skill
  was rebuilt from reported success on work they had silently skipped. The
  skill also names the floor for each engine: a fresh-context subagent where
  subagents exist, a separate process re-reading evidence where they don't —
  and if neither is possible, it calls the result self-review, not
  verification.
- **A Markdown plan is not a loop.** Operationalize mode exists because
  well-written process documents kept turning out to need a human ferrying
  prompts between windows. The audit rubric makes that distinction
  inspectable instead of arguable.
- **The minimal profile is deliberate.** Most personal loops need eight
  elements, not twenty. The linter accepts `learning.enabled: false` and
  `discovery: "none"` with a stated reason, so declaring a loop small costs
  nothing — while leaving the fields blank still fails.

## Field-tested

Probed 7 scenarios across 5 personas · 4 fired correctly · 2 correctly stayed quiet · linter live-fired on 5 contract variants.

> **"Every morning I literally paste the same prompt to check my feeds, then copy the output into a note. This is dumb — automate it."** → Fired. Classified as a recurring loop under the minimal profile: eight design elements, `learning.enabled: false` declared instead of left blank, contract linted to PASS.

> **"Remind me to check the deploy every hour."** → Correctly stayed quiet. A schedule with no state and no verification belongs to your host scheduler, and the description says so out loud.

> **Live-fire:** `loop_lint.py` passed the shipped minimal example (exit 0), rejected the unfilled template with 27 named errors, and failed closed on every trap we set — a blank justification for `discovery: "none"`, and `"false"` as a string instead of a boolean.

Probe method: [scenario-probe](../scenario-probe/)
