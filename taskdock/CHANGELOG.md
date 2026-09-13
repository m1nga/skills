# Changes

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
