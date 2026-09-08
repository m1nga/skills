# TaskDock — Keep Complex Tasks Organized and Ready to Resume

TaskDock is an agent skill that plans and maintains a portable Desktop workspace for ongoing work. Your goal, decisions, current state, evidence, and results stay together so a fresh session can continue without reconstructing the entire chat.

**任务坞：让每个复杂任务都有自己的桌面工作位置。**

## What it does

- Creates a task folder with a stable UUID, a human-readable entry point, current state, and a working plan.
- Plans categories from the actual work and adds folders when they have a use.
- Updates decisions, verification, and next actions as the task changes.
- Finds renamed or relocated task folders within specified search roots and repairs stale index entries.
- Detects conflicting copies and broken common Markdown links instead of silently guessing.
- Returns an existing topic index during resume, so the agent can choose relevant evidence without loading the entire task history.

## When it fires

Use it for multi-step research, a launch, a design project, or continuing work that needs a durable record. Say:

> 用 TaskDock 给这个任务建桌面工作文件夹，规划怎么做，并在过程中维护进度。

> 找回昨天的任务文件夹，按它的状态继续做。

> 这个任务目录乱了，按工作逻辑重新整理并修好引用。

Simple answers and tiny edits do not need a workspace unless you ask for one.

## Install

```bash
npx skills add m1nga/taskdock
```

Then ask your agent: `Use $taskdock to organize this task and keep it ready to resume.`
Requires Python 3.8 or later; no paid API is used by the filesystem helper. A skill
installation may need a fresh session for automatic discovery.

Commands below run from the installed skill directory. From another directory, use
the absolute path to its `scripts/taskdock.py`. Add `--language en` at initialization
for English task notes; Chinese is the CLI default.

## How the folder works

`TASK.json` identifies the task. `README.md` explains what the folder handles. `STATE.md` tracks current facts, decisions, verified progress, and the next action. `PLAN.md` explains dependencies and why files are grouped that way. `AGENTS.md` lets an agent entering the folder find these records.

For a larger task, an optional `INDEX.md` maps questions to source and decision files.
`resume` returns this index when present, bounded like the control records, without
reading its linked files. The agent selects relevant details and reconciles current
state before acting. Simple tasks do not need an index.

The task ID survives a move. Internal relative links survive a whole-folder move. The Desktop task index is a replaceable location hint, not the only copy of your work. A missing index can be rebuilt from task folders.

```bash
python3 scripts/taskdock.py init --title "Launch review" --goal "Ship a reviewed launch plan"
python3 scripts/taskdock.py locate --title "Launch review"
python3 scripts/taskdock.py check --path "/path/to/task-folder"
python3 scripts/taskdock.py resume --path "/path/to/task-folder"
```

Use `locate --id <task-id> --root <search-directory>` for a task moved outside the default Desktop/Documents search. A folder copied twice keeps the same ID; the tool reports ambiguity so the intended working copy can be selected explicitly.

## Design notes

A folder becomes useful when it carries the reason for the work and the next decision, not merely a transcript. TaskDock starts small and expands its structure as deliverables and dependencies become real. It keeps existing repositories authoritative and task evidence separate from public packages.

It does not run while the agent is idle, guarantee discovery anywhere on a disk, move unrelated files, or replace backups. Scheduled work still requires an actual automation. The link check covers common inline Markdown links, not arbitrary HTML or Office document references.

## What we learned from similar skills

[Planning with Files](https://github.com/OthmanAdi/planning-with-files) informed the
explicit recovery check and single-owner rule for shared state. TaskDock adapts those
ideas to portable Desktop tasks and keeps updates tied to meaningful changes instead
of a fixed tool-call counter. It does not copy another engine's hook support or claim
that a plain skill installation enables background execution.

## Validation

Sixteen executable tests cover moved folders, stale or missing indexes, duplicate identities, existing-file preservation, broken-link repair, bounded search, control-file symlinks, corrupt metadata, same-name task isolation, and bounded topic-index recovery without loading linked documents.

```bash
python3 scripts/test_taskdock.py -v
```

The tests establish filesystem behavior, not the quality of every future task plan.

## Author

Built by Ming. MIT licensed.
