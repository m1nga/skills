# Source comparisons

These are author sources inspected on 2026-11-07. They explain choices in this skill. The runtime uses local files and ordinary agent tools.

- [Ponytail](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md) checks what can be reused before new code and traces the places a change must reach. This skill applies that check to costly implementation and keeps full acceptance and recovery. It leaves out session modes and mandatory sign-offs.
- [Token Saviour](https://github.com/vagkaratzas/token-saviour/blob/8fe77b754c0a5e67eaf5ba5f374db95238d65b22/skills/token-saviour/SKILL.md) separates code reading, command output and generated text. This skill selects the actual bottleneck using tools already available in the project.
- [Context Optimization](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-optimization/SKILL.md) keeps bulky observations retrievable and measures the effect of changes. This skill uses scoped snapshots, versioned references and explicit evidence recovery.
- [Context Mode](https://github.com/mksglu/context-mode/blob/0491ccb9c798a95f3f8ee3124c9dcd57b72b8114/README.md) demonstrates a local full-output store with selective returns. The snapshot helper here returns changes from the existing task sources without needing a hook or database.
- [RTK](https://github.com/rtk-ai/rtk/blob/develop/README.md) documents output filtering, raw-output fallback and approximate token estimates. This skill uses native bounded output first and keeps measured bytes separate from actual provider tokens.
- [Caveman](https://github.com/JuliusBrussee/caveman/blob/c310c9d300df13a1dd9f5c086120ffd857a164a1/skills/caveman/SKILL.md) distinguishes compact prose from loss of technical meaning. The workflow here prioritizes repeated reads and redundant implementation, with concise normal-language reporting.
- [UI Morph](https://github.com/cutcodstudio/cutcod-ui-morph) and [Guizang product video workflow](https://github.com/op7418/guizang-product-video-skill/blob/main/SKILL.md) illustrate adapting a working source project and verifying actual inputs, a representative slice and final delivery. Check compatibility and licenses before reusing external code or assets.

Author benchmark numbers describe their respective setups. The skill's own validation reports its measured scope and units.

## Workflow follow-up, 2026-11-07

Current author sources were searched again and their actual skill bodies fetched for the incremental-research integration:

- **Adapt Ponytail:** retain the existing-component → platform → installed-dependency preference, affected-callers check and preservation of error handling. Add an observable reuse decision and a real entry-point result to the existing task record. Reject whole-session personality, ultra-mode pushback and compulsory response endings; they do not improve this research deliverable.
- **Adapt Context Optimization:** retain source recovery and outcome measurement. Add same-input/same-deliverable acceptance, one-time setup separation and remeasurement after material changes. Reject its fixed context percentages, promised reduction ranges, tolerated quality loss and automatic partitioning thresholds. This workflow requires the user's original acceptance checks and does not need a new runtime or agent to reduce a saved-library payload.

The update adds a specific RedBot/repeated-research route and explicit implicit-invocation metadata. It does not install Ponytail's hooks, change the model or claim that an instruction file enforces every running session.
