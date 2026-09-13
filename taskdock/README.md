# TaskDock — Keep Agent Work Ready to Continue

After several AI sessions, the work is scattered: a promising draft, a newer export,
an old handoff that still says “waiting,” and a folder nobody wants to move.

**TaskDock keeps the current result, the decisions behind it, and the next step together.**
Your agent can resume the task, find a moved folder, and reorganize its files with a
preview and an undo path.

![TaskDock: continue from current work, preserve history, and verify reversible organization](https://raw.githubusercontent.com/m1nga/taskdock/main/skills/taskdock/assets/workflow.svg)

## Install

```bash
npx skills add m1nga/taskdock
```

Then tell your agent:

> Use TaskDock to continue this project. Find the current deliverable and the decisions
> behind it, check what has changed, and leave a clear next step.

Or, when files have piled up:

> Organize this task around the version I am using. Preserve earlier decisions and
> original sources, repair affected links, and give me a way to undo the moves.

The agent prepares the records and commands. You do not need to tag every file,
change how you name your projects, or maintain a second task board.

Requires a local filesystem and Python 3.8+. The helper uses only the standard
library; no account, network service or paid API. It works with agents that can read
skills and run local Python. Filesystem tests in this release ran on macOS; Windows
and Linux behavior has not been independently platform-tested.

## See the result before using your own files

From the installed skill directory, run:

```bash
python3 scripts/demo.py --output /tmp/taskdock-demo
```

Choose a new output folder. The demo refuses to overwrite an existing one and uses
sample files. From another directory, use the absolute path to `scripts/demo.py`.

```text
Before                           After
README → cover.svg               README → assets/cover.svg
cover.svg                        assets/cover.svg
download-copy.txt                runtime-copy.txt  (needed)
runtime-copy.txt                  history/rejected.txt  (kept)
history/rejected.txt

Checked: entry repaired · runtime copy kept · history kept
Checked: rollback restored every original visible file byte
```

It performs the change, verifies rollback, and leaves an organized sample ready to
inspect. `--domain release` and `--domain research` exercise two more sample contexts.
The printed receipt includes the operation ID and verified results.

## What it does

| Moment | What TaskDock helps the agent do |
|---|---|
| Start or return | Locate the same task, read its current state and relevant evidence |
| Make a decision | Keep the choice, its source and the next action in the task record |
| Replace a result | Distinguish what is approved, what is used and what is still a proposal |
| Organize files | Preview moves and link repairs, preserve preimages, detect conflicting edits |
| Hand off | Leave one usable entry, the current outcome, history and a concrete next step |

A task starts with `TASK.json`, `README.md`, `STATE.md`, `PLAN.md`, and `AGENTS.md`.
A UUID identifies it after a move. Optional `INDEX.md` links to deeper evidence;
resume returns that index without loading everything it points to. Your existing
repository stays where it is. Small questions and tiny edits need no new folder.

## A few tools behind the workflow

Run these from the installed skill directory, or use the absolute script path:

```bash
python3 scripts/taskdock.py init --title "Launch review" --goal "Prepare a reviewed launch"
python3 scripts/taskdock.py locate --title "Launch review"
python3 scripts/taskdock.py resume --path /path/to/task
python3 scripts/taskdock.py check --path /path/to/task
```

For a folder moved beyond Desktop/Documents, add `--root /search/location` to
`locate`. Duplicate task IDs produce an ambiguity report instead of a guess.

When the work needs deeper organization:

```bash
python3 scripts/taskdock.py inventory --path /path/to/task
python3 scripts/taskdock.py record --path /path/to/task --spec artifacts.json
python3 scripts/taskdock.py reconcile --path /path/to/task
python3 scripts/taskdock.py plan --path /path/to/task --spec moves.json
python3 scripts/taskdock.py apply --path /path/to/task --operation RETURNED_ID
python3 scripts/taskdock.py rollback --path /path/to/task --operation RETURNED_ID
```

The [organization guide](https://github.com/m1nga/taskdock/blob/main/skills/taskdock/references/organize.md)
contains small input examples, supported references, conflict behavior and recovery.
Planning saves its receipt and preimages under the task's private `.taskdock/` folder;
work files change only during apply. Keep this recovery folder in your private backup.

## Why it exists

I built TaskDock because I was doing increasingly complex work with agents and kept
having to reconstruct earlier sessions. I wanted the work to remain somewhere I could
open, understand and carry forward.

The next problem came from using it: current materials and abandoned drafts accumulated
across folders, while old handoff notes still described a previous version. That led to
explicit artifact records and reversible organization. A file being used, approved or
published now has a different meaning. Identical content can still serve different purposes.

The demo is a reproducible illustration of those problems, using sample files.

## Who it's for

Use TaskDock when ongoing research, design, operations or engineering work needs a
durable task home and a reliable way to continue. [Planning with Files](https://github.com/OthmanAdi/planning-with-files)
is an adjacent option for file-based planning and host hooks;
[Skill Curator](https://github.com/cskwork/skill-curator) focuses on installed skill libraries.
TaskDock focuses on the task's deliverables, decisions, location and recovery.

It runs when your agent uses it. It is not a background cleaner, cloud sync service
or a replacement for backup. The organizer handles ordinary local files and common
relative Markdown/HTML/CSS references. Dynamic application paths, cloud permissions,
Office references and full archival metadata require separate tools. The agent still
has to understand the work; the scripts cannot approve a design or prove a deployment.

## Validation

36 executable tests cover task identity, bounded recovery, reference repairs, identical
copy consolidation, retained runtime copies, changed sources, occupied destinations,
symlinks, partial operations, interrupted rollback, byte restoration and file mode bits.
The three demo contexts also execute apply and rollback. These are maintainer-run
filesystem checks, not independent user studies or measured productivity gains.

```bash
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

[What's new](https://github.com/m1nga/taskdock/blob/main/skills/taskdock/CHANGELOG.md)
explains the update. For a Skills CLI installation, update just this skill with
`npx skills update taskdock`. Existing task UUIDs and control files remain valid;
installing the update does not automatically reorganize old projects.

## Author

Built by [Ming](https://github.com/m1nga). MIT licensed.
