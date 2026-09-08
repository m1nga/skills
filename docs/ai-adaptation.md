# How these skills evolve with AI

We review changes in model behavior, tool interfaces and real task results, then
adapt the parts that benefit the work. This is a maintenance approach, not a claim
that every skill has been benchmarked on every model or automatically updated after
every release.

## Verified changes — September 8, 2026

| Skill | What changed | Actual evidence |
|---|---|---|
| [TaskDock](https://github.com/m1nga/taskdock) | Resume includes an existing task topic index with bounded reads; linked documents stay unloaded until needed. | 16 executable filesystem tests, including index recovery, limits and symlink rejection. |
| [Marketing Prompt Builder](https://github.com/m1nga/prompt-craft) | Removed mandatory workshop formatting and mode restrictions; preserved product context, factual boundaries and revisions. | Six maintainer instruction walkthroughs plus structure checks. These were simulations, not independent user trials or measured model gains. |

[Review the source change](https://github.com/m1nga/skills/commit/946c34864bb455987cb483342c3a970bc8e69263)
and the content-bound review receipts in that commit. Both standalone packages
passed remote-source and direct-install discovery checks.

## Try a concrete result

- [Move a TaskDock folder and recover its identity](try-taskdock.md).
- [Reproduce a rejected agent turn budget](try-loop-budget-check.md).
- [Inspect a short marketing prompt example](https://github.com/m1nga/prompt-craft#example-launch-notes-without-invented-proof).

Future changes should explain the problem, the observed result, the verification
method and any remaining limitation. We preserve working behavior when a proposed
replacement has not demonstrated a benefit. Published code and simulations are
reported separately from real adoption and marketing outcomes.
