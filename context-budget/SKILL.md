---
name: context-budget
description: "Reduce token use in agent workflows by selecting source changes, bounding tool output and reusing working implementations. Use for token costs, context bloat, repeated large reads, delta-first review, 省 token / 上下文消耗, or an explicit request to apply the Ponytail reuse check."
---

# Context Budget

Reach the requested result with less irrelevant context and less repeat work. Preserve the evidence, scope, permissions and checks that make the result usable.

## Choose the expensive step

Start from the current goal, the existing result and the smallest evidence needed for the next decision. Identify whether the cost comes from reading sources, tool output, repeated history, implementation and rework, or the response. Make one targeted change first. Small requests usually need direct work.

- **Repeated sources:** use an existing index, Git diff or stable IDs and versions. Compare the whole agreed scope with code. Send counts, changed references and exceptions to the model, then read the necessary original material. Keep a separate record of what was actually reviewed. Check an unversioned source when its freshness matters. A previously seen ID is not evidence that its contents were read or accepted.
- **Large tools and logs:** select relevant fields, files and line ranges before loading the output. Preserve failure status and enough surrounding evidence to explain it. Keep original output retrievable. Expand the read when a missing definition, changed authority, hidden error or unclear boundary could change the decision.
- **Long handoffs:** carry current intent, active constraints, source versions, unresolved decisions and the exact next step from the authoritative task record. Reuse existing memory and owner records. Split work only when authorized and when the added context and coordination pay for themselves.
- **Long responses:** give the result and decision-relevant evidence first. Retain exact identifiers, reasoning needed for a decision, and material uncertainty.

When there is no suitable built-in comparison for two local record snapshots, use [snapshot comparison](references/snapshots.md). Its helper reports a bounded delta with recoverable source references. An item missing from a partial scan remains unresolved.

## Ponytail reuse check

Before writing or rebuilding, find the existing implementation and read the actual entry point, affected callers and the required output. Reuse a compatible working component, source project or platform feature when it saves adaptation and maintenance. Check the source version, license and fit when adapting external material. Prove one representative slice with real inputs before expanding. If reuse makes the full job harder, change the smallest part that reaches the outcome.

When requested, show the observed reuse decision and the check that passed through the real entry point. Preserve required behavior, accessibility, failure recovery, data and security checks. Apply the check to the current task.

## Measure when it matters

For a usage claim, a costly workflow or a comparison, read [measurement](references/measurement.md). Compare equivalent completed tasks. Report measured payload size, actual tokens, wall time and official subscription usage as separate quantities. Keep cache reuse and extra setup, verification and retries in view. Keep provider and account settings under their existing authority.

A short excerpt is sufficient only when it supports the decision. Use the original for exact quotations, new or contested evidence, approvals and release verification. Deliver the requested result and the relevant evidence once the necessary checks pass.
