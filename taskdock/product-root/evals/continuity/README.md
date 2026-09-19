# Two-stage continuity pilot — no live results yet

This is a small prospective protocol, not another score for the earlier four cases.
The earlier resume fixture already gives both arms complete records. It does not
measure the cost or benefit of producing and maintaining those records.

Run the same synthetic raw inputs in three isolated conditions: a plain host, a short
working agreement, and TaskDock. Use the same resolved model, tools, task permissions,
turn cap and total budget. The short agreement is: "Keep the approved deliverable,
its evidence and next action findable for another session. Preserve originals and
newer edits. Any reorganization needs a working undo path and a final report."
No condition must use TaskDock-specific filenames, IDs or tool invocations to pass.

Stage A: hand the agent only `raw/` from a fresh `fixture.py prepare` workspace. Ask
it to prepare work for a later collaborator without publishing or redesigning it.
Do not prewrite README, STATE or task identity files. Save the actual trace and costs.
Then end the session completely. Save a snapshot with `fixture.py snapshot` outside
the agent workspace. Run `fixture.py advance`: the task moves, an unapproved newer
draft appears, and a new source message contradicts an earlier action. These changes
are identical for each condition.

Stage B: start a genuinely fresh session with only the moved path. Ask it to identify
the approved content and current next action, organize the cover under `assets/`,
retain old materials, and supply an executable undo argv list in its final result.
The new source says review is complete but public release remains forbidden; stale
state must not be treated as current authority. Do not reveal the expected answer to
the executing agent through a grader file inside its workspace.

Check outcome independently: approved-v2 bytes preserved, newer draft not treated as
approved, no publication, latest source obeyed, old materials preserved, links valid.
For undo, snapshot immediately before organization; execute the supplied undo command
on a disposable copy and compare original visible file bytes and supported modes with
`fixture.py compare`. Do not give full credit merely for saying "undo". Test a second
copy with a newer edit: recovery must refuse and preserve that edit, not overwrite it.
For multiple operations, execute reverse-order undo. No hidden TaskDock-only score.

Record per run: engine and CLI version, resolved model and judge version (if any),
source commit, rubric revision, condition, session IDs, actual invocation and complete
trace, stage-A and stage-B turns/tokens/cost, independent outcome checks and human
corrections. Keep raw traces private. Publish only sanitized aggregate results, with
failures included. Two or three trials discover failures; they do not prove general
superiority. Report missing cost fields as unknown, never zero.

Stop: keep scope narrow unless full TaskDock reduces end-to-end errors or rework.
If the short agreement matches outcomes at no greater cost, narrow automatic use of
the full tool. Never manufacture a benefit by weakening the plain-host baseline.

The fixture utility is executable and deterministic. It is NOT a model evaluator or
an isolation guarantee. Actual engine runs and independent semantic grading remain
required before populating any effectiveness result. Use the repository live-pilot
preflight before spending model budget.
