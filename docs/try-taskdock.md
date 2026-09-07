# Move a task folder and recover its next action

TaskDock is for builders who keep research, decisions and deliverables outside a
single code repository. A task has a stable ID, current state and a plan. Renaming
the folder does not erase that identity.

## Try the filesystem behavior

Clone this source collection into a location you choose, then run the demonstration:

```bash
git clone https://github.com/m1nga/skills.git ming-skills
cd ming-skills
python3 examples/taskdock-relocation.py
```

The script creates a fictional task and a private index inside a temporary folder
in the current directory. It writes a next action, moves the folder, locates the
original UUID, verifies that the brief is unchanged, and checks duplicate handling.
Only the demonstration's temporary folder is removed afterward.

Expected output, verified on September 7, 2026:

```text
PASS: renamed folder found with the same task UUID.
PASS: existing brief preserved byte for byte.
Resume: Next action: confirm the target customer.
PASS: two copies are reported as ambiguous; no copy silently selected.
Demo complete. Its temporary task and private index were removed.
```

This is a real filesystem check with fictional content. It does not demonstrate an
autonomous agent remembering something, cross-device synchronization, or measured
time savings. Finding the moved folder depends on searching the right root.

## Use it for your own task

```bash
npx skills add m1nga/taskdock
```

Ask your agent: “Use TaskDock to organize this task. Record the current decision,
what remains unverified, and the next action. Keep the code in its existing repo.”

For an ordinary code-only project, a small plan in the repository may be enough.
[Planning with Files](https://github.com/OthmanAdi/planning-with-files) provides a
broader planning workflow with documented hook integrations. TaskDock's focus is a
portable Desktop task folder, UUID lookup and explicit duplicate handling. This is
a difference in scope, not a claim that it outperforms the alternative.

## Tell us what happened

[Report a reproducible result](https://github.com/m1nga/taskdock/issues/new) with
your agent, operating system, command, expected result and actual result. Use a
fictional example and remove private paths or content. A failure is useful feedback.
If it helps a real task, you can star [TaskDock](https://github.com/m1nga/taskdock).
