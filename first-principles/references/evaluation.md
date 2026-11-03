# Executed comparison — 2026-11-03

## Result

This test did not demonstrate an incremental reduction in rework from loading the
skill. Both configurations met the defined acceptance criteria on their first
delivery. This is a small, bounded result, not evidence that the skill never helps.

| Reconstructed task | Criteria | Without skill: repair rounds | With skill: repair rounds |
|---|---:|---:|---:|
| Repair a download while retaining current and historical entry points | 4 | 0 | 0 |
| Apply a zero-new-budget decision to source and generated briefing | 5 | 0 | 0 |
| Prepare a usable migration handoff while preserving pauses, owners and unknown-write reconciliation | 6 | 0 | 0 |

All 15 criteria passed in each configuration. There were six actual model
executions, three per configuration, with no corrective execution required.

## Method

- Frozen skill content: SHA256 `4f614a50a7cadfe8031be5551398e97b7c89a8bd83845f6549fff084a7d62455`.
- Fresh, isolated Codex CLI executions were explicitly configured with
  `gpt-6.1-sol`, `medium` reasoning and `default` service tier.
- Each pair received the same task and fixture. Optional skill discovery and
  inherited project documents were excluded from both controlled contexts; the
  treatment received the installed skill snapshot. Both had the same local tools.
- Acceptance criteria were written before running. Checks included real HTTP
  downloads and ZIP contents, preserved historical hashes, source-to-render
  regeneration, ownership and schedule preservation, exact versions and receipts.
- The primary outcome was additional correction rounds required after initial
  delivery. Up to two repairs were planned for failures; none were needed.
- Deterministic checks were followed by the maintainer's reading of the artifacts.
  This substantive review was not independent or blinded.

## Limits and costs

Only three author-selected historical failure families were reconstructed. They
were known when the skill was designed, not an unseen holdout. This test does not
measure long-term user satisfaction or live-business rework. Both baselines passing
creates a ceiling effect: the sample does not establish an advantage.

All runs encountered connection retries before falling back to HTTP. Timing is
therefore confounded by transport behavior. Reported token counts include cached
input and differ by execution path; they are not subscription usage percentages.
The evaluation coordinator's preparation and analysis are outside those executor
counts. No end-to-end cost or speed improvement is claimed.

The private task record retains the pre-run protocol, fixtures, execution events,
output snapshots and individual grades. The public package includes the method and
bounded conclusion, without private conversation history or local-machine paths.
