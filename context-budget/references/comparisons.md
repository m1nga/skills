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
