# Verify an efficiency change

Define the same end result and checks for both paths. Freeze scope, inputs, model and effort where comparable. Preserve required quality, acceptance criteria and source coverage. Record changed prerequisites, cache conditions and any unmatched comparison. Prefer a bounded real workflow before broad rollout.

Write the acceptance conditions before comparing outputs. Use the actual prior workflow, not an intentionally inflated baseline. Both paths must complete the requested substantive output, not merely select the same IDs. Record first-run setup separately from recurring execution; retain failed attempts and retries. A historical input replay is a real model run but not a fresh live collection scan.

| Measure | How to use it |
|---|---|
| Tool payload | Compare the actual bytes or rows exposed to the model. Preserve the original and show how relevant records can be recovered. |
| Actual model tokens | Use the provider's usage records for the selected run. Count each response once and include setup, coordination, retries and verification. |
| Cache and reasoning | For OpenAI usage fields that report cached input and reasoning as subsets, count input and output once. Show cached input, uncached input, reasoning and any separately exposed cache writes. Follow the endpoint's actual schema. |
| Cost and subscription | Use actual billed figures or a documented pricing calculation for the exact provider, model and cache categories. Subscription usage and reset times come from the official account meter. |
| Outcome and elapsed time | Record the final artifact, checks, rework and duration. Label the boundary if the run is still open or the user has not tried the result. |

On Codex, reuse an existing task-scoped usage export if available. Deduplicate per-response records and avoid adding an aggregate event to its underlying responses. A partial trace cannot establish the total cost. Read only relevant usage metadata from local logs and keep raw transcripts and credentials private.

Use comparable cache conditions or report both separately. Stable reusable prefix content can help where the provider supports caching. Avoid changing an active model, routing, reasoning level or speed merely to improve the number. Include the cost of summarizing and maintaining the new workflow.

Report smaller payloads as smaller payloads. Claim end-to-end savings only when measured for a comparable completed outcome. If error rates, rework or missing evidence rise, restore the relevant original context and narrow the optimization.

For a one-pair result, report the observed difference and cache conditions, not a stable expected percentage. Keep the paired execution boundary separate from the wider audit, debugging, skill authoring and release effort. Do not label the paired result as savings for the entire current conversation. If only an active-turn snapshot is available, state its cutoff and that later responses are excluded. Save the existing usage-export command for the next natural entry; do not create a polling job to close the ledger.

Sources: [OpenAI usage fields](https://developers.openai.com/api/docs/guides/agents-api/observability) and [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).
