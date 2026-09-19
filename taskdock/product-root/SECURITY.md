# Security

## Supported versions

The latest release on the `main` branch of https://github.com/m1nga/taskdock is
supported. Older releases receive no fixes.

## What TaskDock can do on your machine

TaskDock is a Python standard-library script driven by your agent. It creates and
moves files only inside the task folder passed with `--path`, plus the optional
index file under your Desktop. It never executes task content, never runs shell
commands from files it reads, and never contacts the network. Reorganizations save
byte preimages and a journal under `.taskdock/` so `rollback` can restore files.

Text inside a task folder is data. Agents using this skill are told not to follow
instructions found in user documents.

## Reporting a vulnerability

Open an issue titled `security:` at https://github.com/m1nga/taskdock/issues with
steps to reproduce, or use GitHub's private vulnerability reporting on the repository
if it is enabled. Expect an acknowledgement within a week.
