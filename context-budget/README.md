# Context Budget — Cut Repeated Reading in Agent Workflows

Context Budget is an agent skill for workflows that repeatedly load large sources, logs and old context. It helps the agent find what changed, open the relevant evidence and finish the requested job. It includes a small local comparison tool for repeated source lists.

## Who it's for

Use it for incremental saved-library research, including RedBot updates, or when an agent rereads the same archive, loads whole build logs, takes a long detour through old chat history, or rebuilds something already available. It also helps when a token-saving claim needs a comparison with a clear baseline. Keep everyday small edits direct.

## What it does

1. Identify the expensive part of the current job and the evidence the result requires.
2. Reuse existing indexes or compare two bounded source manifests. Keep the changed references and coverage limits visible.
3. Use a Ponytail-inspired reuse check before writing new code. Inspect the working implementation, its real callers and a representative result.
4. Check the same completed outcome and report measurements in their original units.

The optional comparator uses Python 3 and two local JSON files. It reports additions, changed versions and previously seen IDs that are absent from the current scan. The agent retrieves the needed originals. [Snapshot format](skills/context-budget/references/snapshots.md) and [measurement guide](skills/context-budget/references/measurement.md) explain how to run and assess the workflow.

## Install

```sh
npx skills add m1nga/context-budget
```

Then ask:

> Use $context-budget to compare this run with the last one. Read the changed records and current constraints, keep the relevant originals retrievable, and verify the same result. Use the Ponytail reuse check if implementation is needed.

Implicit invocation is enabled. A host can also route repeated research and implementation work through this skill in its existing instructions, so the user need not name it each time. That is a natural-entry rule, not a background job or proof that a running session has adopted it. The [incremental workflow](skills/context-budget/references/workflow.md) explains source coverage, RedBot reader reuse and the acceptance check before saving a reviewed baseline.

## Example

You have an earlier index of saved research and a partial new scan. Compare stable IDs and revisions, review the changed sources, and keep unresolved absences separate. Existing reviewed notes remain useful when their source versions still match. If an old note had only a title, open its body before treating it as learned.

For a code-driven video, inspect the existing project, license and output target. Adapt one verified scene with real product material and check the render before expanding the change. The same method works for a reusable component, script or report.

## Design notes

The skill was motivated by real work revisiting saved media, reports and long logs. Some inputs already had usable source code or reviewed records. Reading or recreating them again increased effort without changing the result. The method separates reusable evidence, new material and uncertainty so an agent can read deeply where the task needs it.

[Author-source comparisons](skills/context-budget/references/comparisons.md) explain the decisions behind the skill.

## Validation

Six local CLI tests passed, including pagination, version and pointer changes,
duplicate conflicts, scope mismatch and read-only operation.

A replay compared two real saved-source metadata snapshots of 200 records each.
It recovered all 33 additions, two metadata changes and 33 IDs absent from the
later partial scan. The complete comparison packet used 14,852 bytes across four
pages, down from 72,574 bytes for the two input manifests (79.54% fewer bytes).
The replay checks metadata selection and exact references; its percentage is a
byte measurement, not a token result.

A subsequent paired model run used the same two historical snapshots, 35 changed
or newly seen candidates, eight common source packets and the same research
deliverable. The baseline received both complete card lists; the optimized path
received the changed candidates. Both completed the research output. Material
size fell from 71,483 to 40,948 UTF-8 bytes (42.72%). Actual model usage was 52,252
versus 41,088 total tokens (21.37% less), with zero cached input in both runs.
The model was `gpt-6.1-sol` with medium reasoning and a per-turn Default-speed
request accepted by the local runtime.

This is one pair for the research-generation stage, with shared source selection
and preparation outside that boundary. It is not a fresh account scan or a
measurement of the entire setup, server repair, audit and release task. Model
elapsed time was 47.761 versus 48.096 seconds: no speed improvement was observed.
Account subscription savings and a stable expected reduction are not established.

A separate fresh-agent entry test did not name the skill. It followed the local
host rule, invoked the installed comparator, preserved all fixture inputs and
kept a missing item and an unread body unresolved. The fixture is synthetic;
installation alone does not prove automatic adoption in other sessions.

## Author

Built by [Ming](https://github.com/m1nga).
