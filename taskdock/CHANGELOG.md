# Changes

## 2026-09-19 — Claude Code plugin, Python-free fallback, measurable evals

- New `organize` command: plan, apply, structure check and a ready-to-paste report with
  the rollback command in one call. Added after the eval showed the multi-step route ran
  out of turns before reporting; `plan` / `apply` remain for previewed changes.
- The trigger description now names the real job: one portable folder that a later
  session, another agent (Claude Code, Codex, ChatGPT) or another machine can resume,
  find after a move and reorganize reversibly. Chinese trigger phrases and an explicit
  "not for" clause were added; hosts now cover generic "continuing work" natively.
- `python3` unavailable is no longer a dead end: the skill tries the other interpreters
  on the machine, then writes control files by hand from `references/control-files.md`.
  Found on the maintainer's own Mac, where an unaccepted Xcode license blocks `/usr/bin/python3`.
- Installable as a Claude Code plugin: `claude plugin marketplace add m1nga/taskdock`,
  then `claude plugin install taskdock@taskdock`. The Skills CLI path is unchanged.
- `evals/` suite for `claude plugin eval` with a with/without ablation (four cases).
- `PRIVACY.md`, `SECURITY.md` and a pinned, read-only scanner workflow for the HOL registry.
- No change to task identity, control files, commands or recovery data. Existing folders
  keep working; nothing is reorganized by installing the update.


## 2026-09-13 — Current work and reversible organization

TaskDock now helps maintain the relationship between the current result, its decisions
and its files, in addition to creating and finding portable task folders.

- `record` / `reconcile`: distinguish explicit approval from actual use, detect changed
  or missing artifacts, and preserve replacement relationships.
- `inventory` / `plan`: inspect content identities and common relative references;
  preview individual moves, identical-copy merges and required link repairs.
- `apply` / `rollback`: retain original bytes, journal progress, resume after an
  interruption and refuse to overwrite conflicting new work.
- A runnable sample with design, release and research contexts proves its own undo path.
- Existing UUIDs, control files and commands remain compatible. New generated task
  notes default to English; working records can follow the user's language.

Recovery data remains local in `.taskdock/`. The organizer is for ordinary local files,
not cloud storage or complete archival metadata. No automatic cleanup or background
service is installed. Windows locking is implemented but not tested on Windows in this release.
