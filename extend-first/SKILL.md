---
name: extend-first
description: "Check for reusable skills, agents, or automations before creating a new capability. Recommend extending, combining, or building; skip for ordinary tasks and explicit requests to bypass the check."
---

# Extend First

Avoid building a duplicate capability. This check supports creation; it does not
add a separate approval stage to already-authorized work.

## Inspect the nearest existing capabilities

Use the available catalog and the user's known source registry. Read names and
descriptions first, then inspect the few candidates that may actually cover the
request. Inspect agent definitions or scheduled tasks only for those kinds of work.
Do not ask for a directory already present in session or repository context.

Compare the problem solved, input and output, and whether the capability judges
or executes. Similar names are a search aid, not proof of functional overlap.
Distinguish reusable behavior from incidental shared words.

## Recommend and proceed

- **EXTEND:** identify the existing capability and the exact behavior to add.
- **COMPOSE:** identify the handoff between existing capabilities and how to use it.
- **BUILD NEW:** explain the uncovered need and its boundary against the nearest match.

Give a short evidence-backed recommendation; quote only the description fragment
needed to establish overlap. If the catalog is unavailable, state that limitation
and inspect reachable sources rather than pretending a complete search.
When overlap is uncertain, prefer a small reversible prototype or a separate narrow
capability over merging unrelated purposes.

Continue the creation or update the user authorized using the appropriate authoring
workflow. Do not ask for a second approval of a routine reuse choice. Respect an
explicit "build it anyway" or "skip the check" immediately.

This skill does not activate for using a capability, an ordinary project task,
or a product idea that does not propose a new agent capability.
