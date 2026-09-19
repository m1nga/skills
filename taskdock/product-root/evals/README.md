# TaskDock eval suite

Four cases for `claude plugin eval`. Two arms run by default: with TaskDock loaded
and without it (a plain Claude Code session), so the score delta shows what the
skill adds rather than what the model already does.

```bash
claude plugin eval . --scaffold --allow-tools Bash Write Edit --runs 3 --no-publish
```

- `--scaffold` runs each case's `fixture.sh` (author-supplied bash) to build a
  sample task folder in the run's temporary directory. Read the scripts first.
- `--allow-tools` lets the agent run the TaskDock script and write files. Runs are
  confined to a temporary directory; cases always pass `--path` or a relative folder.
- Graders that only TaskDock can satisfy (`tool_used: Skill`, `.taskdock/` receipts,
  `TASK.json`) are marked `arm: with-only` or are excluded automatically; they are
  reported as indicators and do not inflate the delta. The scored graders judge the
  outcome a user would notice.

| Case | Checks |
|---|---|
| resume-task-folder | Resumes from STATE.md; treats the newest draft as unapproved; names the recorded next action |
| new-long-task-workspace | Sets up one entry point with identity, state and plan for a multi-week task |
| tiny-question-no-workspace | Answers a quick question without creating a folder or invoking the skill |
| organize-with-undo | Moves assets, repairs links, keeps history, and reports a real undo path |

Results land in `evals/results/` (ignored by git). Report the run's numbers and
model in the README when they are published; a passing suite here is a maintainer
check, not a user study.
