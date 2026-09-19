---
name: day-close
description: "Turn the day or week into a short handwritten closing note: real progress, unfinished work with a place to resume, and questions to leave for later. Use for bedtime work reflection, 今日收笔, 睡前总结, or a weekly wrap-up intended for personal journaling."
---

# 今日收笔

Help the user finish their day by seeing what happened and putting open work into words they can copy by hand. Deliver the note in the conversation. The user writes it on paper; an exported report or dashboard is not the primary result. Adapt the same practice to a week when requested.

## Scope and evidence

- Default to the current conversation. When the user asks about their other tasks or requests a cross-task review, inspect the available task list and relevant recent messages read-only. Do not imply access to all apps, private thoughts, or a complete life record.
- Resolve “today” and “this week” in the user's timezone. This week means the current calendar week, Monday through today unless the user specifies otherwise; it is not silently the last seven days. State the date range briefly. Separate older background from progress within that range.
- Task titles and active/idle/completed flags do not establish outcome. Read relevant messages; use the returned title verbatim if naming a task, but group the note by actual work. An active task with unavailable current messages is “still processing; latest result unavailable,” not a guessed milestone.
- Retrieve compact user messages and final replies first. Filter out reasoning, raw tool dumps and images before surfacing results. Read older turns or a specific artifact only when a material claim needs it. Do not run a fresh technical audit of every project for a bedtime note.
- Distinguish a produced artifact, a reported check, user acceptance, public release and real user impact. A draft is progress but not approval; an agent finishing a turn is not the project finishing. Follow the user's latest correction over an older completion claim.
- If only a limited record is available, give a useful bounded note and one short scope statement. Invite missing input only when necessary before writing; do not invent completion, feelings, personal events, adoption or growth.

## Write for a pen

Synthesize related work rather than replaying the chat. Keep sentences short, concrete and natural in the user's language. A useful starting size is roughly 200–350 Chinese characters for a day or 400–700 for a week, adjusted to the amount of real work and the user's preference.

Use these four movements when they fit, without forcing empty sections:

1. **完成与推进** — What now exists, what changed, or what the user decided. Clarifying a direction or rejecting an unsuitable path can count as progress if supported by the record.
2. **还没完成** — The few consequential open items: where each stopped and its smallest resumption point, if known. Distinguish ongoing work, waiting on someone, and consciously deferred work. Do not convert all unfinished items into tomorrow's commitments.
3. **留着再想** — One or two unresolved questions already important to the user. Write them down without launching the debate, expanding the scope or asking the user to solve them tonight.
4. **收笔** — A simple closing sentence that gives the entry an end, grounded in what was recorded. No invented emotion, forced gratitude, motivational praise or promise of better sleep.

First-person wording is useful for copying factual statements, but do not put unspoken beliefs or feelings in the user's mouth. Leave personal reflection space rather than manufacturing an answer. Avoid tables, nested lists, technical logs, long URLs and references within the copyable note. When provenance is useful, put a compact scope/evidence pointer before the note or in an optional private companion file.

Finish after the closing sentence. Do not append “would you like me to…”, further suggestions, a new task, or a question that reopens work. If the user wants an interactive journaling session, ask one gentle question at a time, then produce the final copyable note once there is enough material.

## Boundaries

This is a reflective read-only workflow. It does not resume other tasks, change their status, schedule monitoring, publish writing or send messages. A request to review tasks authorizes reading, not managing them. Do not create a new task folder for each daily use unless requested or an existing records workflow calls for saving it. Personal recap evidence must never be bundled into the public skill package.
