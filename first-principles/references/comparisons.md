# Sources considered for this release

Author sources inspected on 2026-11-03. These are design comparisons, not runtime
instructions or dependencies. No third-party code or instruction text is bundled.

| Source | Decision and application |
|---|---|
| [First Principles Thinking](https://github.com/awesome-skills/first-principles-skill/blob/main/SKILL.md) | Adapt the separation of outcome, assumptions and constraints. Omit its fixed five-part report and exhaustive assumption inventory for routine execution. |
| [Boring Engineering](https://github.com/alvindemesadev/boring-engineering/blob/main/SKILL.md) | Adapt reuse and necessary-complexity checks beyond code. Finding an existing component must lead to completing the task; it is not a stopping point. Do not adopt compact-code formatting rules. |
| [Redesign From First Principles](https://github.com/backnotprop/pstack/blob/main/skills/principle-redesign-from-first-principles/SKILL.md) | Retain the useful counterfactual about requirements; reject redesign as the default action. Existing working systems, users and migration costs are real constraints. |
| [Context Optimization](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-optimization/SKILL.md) | Adapt bounded evidence retrieval and accounting for coordination overhead. Do not adopt unverified percentage targets, mandatory partitioning or unsupported runtime controls. |

The private historical review also supplied a counterexample: an over-short
handoff can omit the knowledge needed to execute. This skill therefore minimizes
unnecessary work while retaining essential context and complete outcomes. Historical
examples explain design choices; they do not establish efficacy of this release.

## Evaluation and documentation follow-up, 2026-11-03

- Re-read the current First Principles Thinking author source above. Keep the
  outcome/constraint distinction; continue to omit mandatory analysis sections.
  The public README now explains the execution use case and direct installation
  without requiring a separate hosted product page.
- Adapt [Anthropic's skill-creator evaluation workflow](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md): paired executions with and without the skill,
  fixed acceptance criteria, recorded artifacts and honest timing/token evidence.
  Runs here use Codex, not Claude. Programmatic checks handle deterministic facts;
  the author reviews meaning and states that limitation. Do not interpret missing
  user feedback as satisfaction, or promote a passing demonstration into proof of
  reduced rework. No evaluation pipeline is installed as a runtime dependency.
