# Privacy

TaskDock runs entirely on your machine.

- It makes no network requests, has no account, and sends no telemetry.
- It writes only inside the task folder you point it at: the control files
  (`TASK.json`, `README.md`, `STATE.md`, `PLAN.md`, `AGENTS.md`), optional
  `INDEX.md`, and a private `.taskdock/` folder holding artifact records,
  reorganization plans, progress journals and byte preimages used for rollback.
- The optional lookup index at `~/Desktop/🗂️ 任务索引/index.json` stores task
  titles, folder paths and timestamps so a moved folder can be found again. It
  never stores file contents.
- Nothing is uploaded, synchronized or backed up by TaskDock. Keep your own backup
  of task folders, including `.taskdock/`, if you need recovery beyond your disk.

The agent that calls TaskDock (Claude Code, Codex, ChatGPT or another host) has its
own privacy terms; those apply to the conversation, not to these local files. The
Skills CLI used for installation (`npx skills add`) may collect its own usage
statistics; TaskDock does not read or send them.
