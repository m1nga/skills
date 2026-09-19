#!/usr/bin/env bash
set -euo pipefail
root="./task"
mkdir -p "$root/old" "$root/notes"
svg='<svg xmlns="http://www.w3.org/2000/svg" width="80" height="40"><rect width="80" height="40" fill="#c8b6ff"/><text x="8" y="26" font-size="14">cover v2</text></svg>'
printf '%s\n' "$svg" > "$root/cover.svg"
printf '%s\n' "$svg" > "$root/cover copy.svg"
printf '<svg xmlns="http://www.w3.org/2000/svg" width="80" height="40"><rect width="80" height="40" fill="#ddd"/><text x="8" y="26" font-size="14">cover v1</text></svg>\n' > "$root/old/cover-v1.svg"
cat > "$root/README.md" <<'MD'
# Brand one-pager

This folder handles: Produce the approved brand one-pager for the website team

Task ID: `a3b7c1d2-4e5f-4a6b-8c7d-9e0f1a2b3c4d`

## Resume here

Read [current state](STATE.md) and [the plan](PLAN.md). [TASK.json](TASK.json) identifies this task across folder moves.

Cover image: ![cover](cover.svg)

Approved text: [final-v2.md](final-v2.md)
MD
cat > "$root/STATE.md" <<'MD'
# Current state

## Goal

Produce the approved brand one-pager for the website team

## Verified progress

- `final-v2.md` approved by Ming on 2026-09-11. Approved version.
- `final-v3-draft.md` is an unreviewed experiment; not approved.
- `cover.svg` is the image the website team uses. `cover copy.svg` is an accidental duplicate download.
- `old/cover-v1.svg` is the rejected first cover, kept for the record.

## Next action

Hand the approved one-pager (`final-v2.md` + `cover.svg`) to the website team.
MD
cat > "$root/PLAN.md" <<'MD'
# Task plan

## Outcome and scope

One approved one-pager and its cover image, ready for the website team.

## File organization

Keep the approved result easy to find; keep rejected versions in history; do not lose the cover the website team already uses.
MD
cat > "$root/AGENTS.md" <<'MD'
# This task workspace

This folder handles Brand one-pager. Read README.md, STATE.md and PLAN.md to resume.
TASK.json identifies the task across folder moves. Keep internal links relative.
MD
cat > "$root/final-v2.md" <<'MD'
# Brand one-pager (v2, approved)

We make small tools that respect your time.

![cover](cover.svg)
MD
cat > "$root/final-v3-draft.md" <<'MD'
# Brand one-pager (v3 draft)

Small tools. Big respect for your time.
MD
cat > "$root/notes/review-notes.md" <<'MD'
Ming, 2026-09-11: v2 approved. Keep the purple cover. v1 cover rejected (too grey).
MD
cat > "$root/TASK.json" <<'JSON'
{
  "schema": "taskdock/v1",
  "id": "a3b7c1d2-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
  "title": "Brand one-pager",
  "goal": "Produce the approved brand one-pager for the website team",
  "created_at": "2026-09-09T08:00:00+00:00",
  "files": {"readme": "README.md", "state": "STATE.md", "plan": "PLAN.md"}
}
JSON
echo "fixture ready: $root"
