# TaskDock — Keep Agent Work Ready to Continue

Starting a new coding-agent session should not mean hunting for the latest draft.
When task files, decisions and handoffs are scattered, TaskDock puts the current
work in a portable folder with a stable identity. Its file organizer previews
moves and can undo its own recorded changes, with protection for later edits.

**TaskDock keeps the current result, the decisions behind it, and the next step together.**
Your agent can resume the task, find a moved folder, and reorganize its files with a
preview and an undo path.

![TaskDock: continue from current work, preserve history, and verify reversible organization](https://raw.githubusercontent.com/m1nga/taskdock/main/skills/taskdock/assets/workflow.svg)

## Install

```bash
npx skills add m1nga/taskdock
```

Claude Code users can install it as a plugin instead (same files, plugin update channel):

```bash
claude plugin marketplace add m1nga/taskdock
claude plugin install taskdock@taskdock
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
library; no account, network service or paid API. If `python3` is missing or blocked
(on macOS an unaccepted Xcode license blocks the system interpreter), the skill tries the
other interpreters on the machine and otherwise writes the control files by hand from
`references/control-files.md`; only the reorganization tools need the interpreter. It works with agents that can read
skills and run local Python. Filesystem acceptance checks run in the repository CI on Linux, macOS and Windows.
Windows shell checks target PowerShell; POSIX permission bits are tested only on POSIX systems.

## Resume an AI agent task from a sample handoff

Install TaskDock for Codex at project scope using the command above. For a
non-interactive install, add `--agent codex --yes`. From the same project folder,
run:

```bash
python3 .agents/skills/taskdock/scripts/demo.py --output taskdock-demo --domain release --handoff
```

On Windows, replace `python3` with `py -3` if you use the Python Launcher. If you installed
TaskDock somewhere else, use the path to `scripts/demo.py` in that installation.
The demo uses sample files. If `taskdock-demo` already exists, choose a fresh
name such as `taskdock-demo-2` and keep the earlier run.

1. Open `taskdock-demo/handoff.html` in a browser. The page contains the task ID,
   the folder path and a message you can paste into a new agent session.
2. In the page's README.md section, find **Current result**. Open
   `delivery/release-notes.txt` inside the sample folder. It starts with
   “Release 1.0: a sample delivery”.
3. Follow the next step in the page's STATE.md section. Compare that file with
   `runtime-copy.txt` and record the check in the sample's `STATE.md`.

The report is a snapshot. The sample folder holds the files and their latest
state. Review the page for task notes and local paths before sharing it.

```text
Before                           After
README → release-notes.txt       README → delivery/release-notes.txt
release-notes.txt                delivery/release-notes.txt
download-copy.txt                runtime-copy.txt  (needed)
runtime-copy.txt                  history/rejected.txt  (kept)
history/rejected.txt

Checked: entry repaired · runtime copy kept · history kept
Checked: undo refused the simulated collaborator edit and preserved all visible files
Checked: ordinary rollback restored every original visible file byte
```

The demo applies the change, edits the moved file as a collaborator would, and
shows a `rollback_conflict` receipt naming that file. It checks that the refused
undo touched no visible file. It then removes its own sample edit, verifies
byte-for-byte rollback, and reapplies a fresh plan so you can inspect the
organized result. The design and research variants use other sample files.

In a real workspace, preserve the later edit when undo reports a conflict.
Review the named paths and decide how to incorporate those changes before
replanning. The operation receipt is local filesystem evidence. Cross-session
time savings require a separate comparison.

## Create a handoff for your own task

```sh
python3 SKILL_DIR/scripts/handoff.py --path TASK_FOLDER --out handoff.html
```

Use a new filename for the page. It opens locally in a browser and includes the
task ID, selected folder, bounded records and a prompt for the next session.
Pending recovery is shown in the report and returns a nonzero exit. Verify the
live task files before continuing, and review private notes and paths before sharing.

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
python3 scripts/taskdock.py organize --path /path/to/task --spec moves.json   # plan + apply + check + report
python3 scripts/taskdock.py apply --path /path/to/task --operation RETURNED_ID
python3 scripts/taskdock.py rollback --path /path/to/task --operation RETURNED_ID
python3 scripts/taskdock.py recovery --path /path/to/copied-task --operation RETURNED_ID
```

The [organization guide](https://github.com/m1nga/taskdock/blob/main/skills/taskdock/references/organize.md)
contains small input examples, supported references, conflict behavior and recovery.
`organize` also returns `rollback_argv` for shell-free execution and labels the shell
used by the copyable `rollback` command. Errors after planning retain recovery details;
`resume` reports unfinished operations. Non-UTF-8 reference files stop planning before
work-file changes. Do not automatically retry or roll back over someone else's new work.

Planning saves its receipt and preimages under the task's private `.taskdock/` folder;
work files change only during apply. Keep this recovery folder in your private backup.
Include organization-related task notes in the same optional `notes` spec, so they undo
with the move rather than immediately conflicting with it. For a moved or copied task,
`recovery` generates checked arguments for that explicitly selected location; never
assume the original absolute-path command now targets the copy.

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

66 executable tests (including platform-specific cases) cover task identity, bounded recovery, reference repairs, identical
copy consolidation, retained runtime copies, changed sources, occupied destinations,
symlinks, partial operations, interrupted rollback, byte restoration and file mode bits.
The three demo contexts also execute apply and rollback. These are maintainer-run
filesystem checks, not independent user studies or measured productivity gains.

```bash
python3 -m unittest discover -s skills/taskdock/scripts -p 'test_*.py' -v
```

The standalone repository also ships an `evals/` suite for `claude plugin eval` (four
cases: resume a folder where the newest draft is not the approved one, set up a
multi-week task, answer a quick question without creating anything, reorganize with a
real undo path). It runs each case with and without TaskDock and reports the difference,
so the score shows what the skill adds rather than what the model already does:

```bash
claude plugin eval . --scaffold --allow-tools Bash Write Edit --no-publish
```

Measured on 2026-09-19 with `claude-sonnet-5` as the agent and `haiku` as the judge, two
arms per case (with TaskDock loaded, and a plain session):

| Case | With TaskDock | Without | Runs |
|---|---|---|---|
| resume-task-folder | 1.00 | 1.00 | 2 + 2 |
| new-long-task-workspace | 1.00 | 1.00 | 2 + 2 |
| tiny-question-no-workspace (must not fire) | 1.00 | 1.00 | 2 + 2 |
| organize-with-undo, before the `organize` command | 0.38 | 1.00 | 2 + 2 |
| organize-with-undo, after adding `organize` | 1.00 | 1.00 | 3 + 3 |

The first organize result was the useful one: the multi-step plan/apply route did the
moves and saved the rollback preimages but ran out of turns before reporting, so the user
never saw what moved or how to undo it. The one-call `organize` command fixed that, and
the reported ranges were 17 to 24 turns with TaskDock and 20 to 23 without.
Those overlapping ranges and three runs do not establish lower average cost or better
tail performance. The helper tests separately exercise actual recovery. On the outcome graders a current model already
handles these four scenarios without the skill; what TaskDock adds is the identity file,
the recorded state and the reversible operation receipts, which the graders deliberately
do not score. The three runs cost about USD 7 in total. Graders are documented in
`evals/README.md`. The resume fixture already gives both arms complete task records;
that case tests reading existing records, not the end-to-end value of creating and
maintaining them. A neutral two-stage pilot is specified in `evals/continuity/README.md`;
live model results for that pilot are not yet available.

[What's new](https://github.com/m1nga/taskdock/blob/main/skills/taskdock/CHANGELOG.md)
explains the update. For a Skills CLI installation, update just this skill with
`npx skills update taskdock`. Existing task UUIDs and control files remain valid;
installing the update does not automatically reorganize old projects.

## Author

Built by [Ming](https://github.com/m1nga). MIT licensed.

## September 19 follow-up: use selectively

A separate one-trial, three-condition Claude pilot found no continuation advantage on
its fixture: plain/short-agreement/TaskDock used 15/33/58 turns. Those are one observed
set, not general speed claims. The same report found TaskDock's conflict refusal safer
than the plain arm's unconditional undo, but its own follow-up note writes prevented
normal rollback. This release adds transaction-bound notes and explicit recovery-path
selection without weakening conflict guards. The prior trace is not a test of this fix.

The detailed maintainer report and its scoring limitations are in the source registry
under `ops/skill-quality/live-pilot/RESULTS-2026-09-19.md`; the follow-up review separates
incomplete trigger evidence from passes. No new authenticated Claude/Codex outcome or
routing result is claimed for this patch. Existing useful task notes are often enough;
use the organizer for a concrete need for previewed, conflict-checked recovery, not
merely because a task takes more than one chat.
