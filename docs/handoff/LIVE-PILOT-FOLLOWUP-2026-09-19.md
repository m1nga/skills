# Live-pilot follow-up — 2026-09-19

## What helps Ming now

The Mac executor reports day-close is independently preserved and TaskDock updated to
8da9227. No Mac files are changed by this follow-up. Ordinary questions, clear small
changes and already-readable project handoffs should remain ordinary host work. The
pilot did not demonstrate that full TaskDock improves those jobs. Keep its organizer
for a concrete need for preview, recoverable changes and refusal to overwrite new work.

The pilot's 15/33/58 turns (plain/agreement/TaskDock) and list-equivalent estimates are
one observed trial, not a universal performance ranking or amounts charged. Raw traces
remain on the local host; this reviewer inspected the published sanitized report and
reproduced code contracts independently, not the private live conversations.

## Evidence corrections, without silently rescoring the original report

Read the original [report](../../ops/skill-quality/live-pilot/RESULTS-2026-09-19.md).
Its detailed trigger table contains SIX completed passes, ONE routing failure and ONE
incomplete recap case. The summary's "7 correct" cannot establish recap success: a
no-write check passed, but recap quality was not exercised. A future recap case needs
an actual seeded conversation, not a first-message empty session.

The no-continuity-advantage observation is not proof of no safety value. The report also
says plain-host undo was unconditional, agreement undo refused with exit 0, and TaskDock
correctly preserved a newer edit and returned nonzero. Keep that safety difference
separate from success-path convenience and cost. Do not increase automatic trigger
frequency merely to make a tool-used indicator pass. The TaskDock trigger description
is unchanged here; use explicit selection when deliberately testing its safety tools.

Blob mode 0600 is private storage, not the original work-file mode. The existing engine
writes the mode stored in the plan when restoring. Existing and new mode-roundtrip
tests pass; no chmod broadening or blob-copy workaround is justified by the report.
An absolute-path command intentionally targets its original task. Its portability
limitation is real, but copying a folder must not silently retarget that command.

## Narrow implementation

- Optional `notes` records organization-related control-file text and expected input
  hashes in the SAME operation as moves and link repairs. Preview remains non-mutating.
  Full exact rollback restores the notes too. Changes made afterwards are still newer
  work and still stop rollback; no control files are exempted from guards.
- Read-only `recovery --path SELECTED_COPY --operation ID` validates task identity and
  preimages and generates arguments for the explicitly selected task path. A copy test
  must include recovery data; the compatible installed script must still be available.
- The prospective rubric distinguishes immutable approved source evidence, a working
  reading copy with documented link edits, local links, copy portability and safe refusal.
  This does not retroactively change any of the first pilot's scores.

Local acceptance: 63 tests collected, OK with one Windows-only skip, including 11 new
regressions. The input source fingerprint matched the published reviewed 2026.9.20
fingerprint before changes. Actual cloud matrix/publication evidence is recorded in the
follow-up PR and Actions; this document alone is not proof of those later steps.

## Still requires the local executor

After this fix is published, update only TaskDock through its existing installation
method, preserving local changes; do not update the full source checkout or day-close
again. Run the note/undo regression locally and one small explicitly selected TaskDock
organization including its normal notes; report whether the delivered undo actually
works with no bespoke script. No broad new 28-session run is requested by this patch.
The prior 18 model sessions do not test this new implementation.

Codex is blocked in the reported command-line environment. Not finding `codex` does not
prove that the desktop app or account is absent. Check documented executable locations
and the current PATH before proposing installation. Installing a CLI does not itself
purchase a subscription. Ask Ming once before adding the missing runtime; prefer the
existing ChatGPT subscription login, do not introduce API-key billing or paid credits,
and stop if entitlement or no-extra-spend conditions cannot be verified. Official
reference: https://developers.openai.com/codex/auth/ . No credential belongs in GitHub.

One local-only authorization/login step cannot be performed by this GitHub-connected
chat. The task is not finished merely because instructions were written; keep Codex
and the fresh live follow-up marked blocked/not_run until their runs actually exist.
