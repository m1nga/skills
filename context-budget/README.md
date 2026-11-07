# Context Budget — Cut Repeated Reading in Agent Workflows

Context Budget is an agent skill for workflows that repeatedly load large sources, logs and old context. It helps the agent find what changed, open the relevant evidence and finish the requested job. It includes a small local comparison tool for repeated source lists.

## Who it's for

Use it when an agent rereads the same archive, loads whole build logs, takes a long detour through old chat history, or rebuilds something already available. It also helps when a token-saving claim needs a comparison with a clear baseline. Keep everyday small edits direct.

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
The replay checks metadata selection and exact references. End-to-end model
usage, rework and subscription savings remain unmeasured.

## Author

Built by [Ming](https://github.com/m1nga).
