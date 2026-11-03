---
name: breakinggap
description: Use a short waiting gap while an AI agent works for one useful human step in current work, an unfinished task, or relevant learning, with a checkpoint and an easy return. Use for “what can I do while this runs?” or “I have ten minutes while my agent works”; not general day planning, agent monitoring, or end-of-day reflection.
---

# BreakingGap

**A little gap. A little further.**

Help the person make a small, satisfying contribution while an agent works. The result may be a clearer decision, a few useful words, a resumed idea, or one better-understood concept. Leaving the gap empty is a valid choice. Match the conversation's language; the bundled companion interface is English.

## Find a step that belongs here

Use the current conversation and the project's existing state first. Keep the primary work and its return point visible. Check current agent status only through an available, authorized status tool or the user's report; never invent live monitoring. If the primary agent needs the person or has finished, return to its result before proposing another activity.

Use a user-stated time budget. If absent, ask one brief question about available time and the current work; do not assume a ten-minute agent ETA. When duration is uncertain, offer an explicitly estimated, easily interrupted two-minute step. Do not start a large scan or wait for all agents to finish just to find a suggestion.

Infer the useful intention from the request; otherwise favor current work:

- **Move this forward:** a human judgment, acceptance example, short draft, or comparison that improves the current work without depending on the pending output.
- **Pick something up:** an already authorized unfinished item with a concrete saved next action. Recheck that it is still open; do not revive paused work or another owner's assignment.
- **Learn one thing:** one concept from a real source in the current project. Ask the person to predict, explain, or compare before giving a short source-grounded check. No response means no demonstrated learning. Label generated examples and unresolved questions honestly.

Read only enough current source to support the chosen action. Confirm it is still useful, authorized, independent of the pending output, and free of conflicts with active work. Do not treat a small task as permission to cross a hold, change agent-owned files, send messages, or publish. Prefer a private scratch response over concurrent edits. If context is missing, ask for the current goal or use the user's supplied text; never fabricate a backlog, source location, completion state, or authorization.

Estimate setup + human action + wrap-up, and leave **two minutes for returning** within the user's budget. Estimates are not measured durations or agent completion predictions. Shrink oversized work to a meaningful stopping point; exclude unclear or deeply absorbing tasks rather than defaulting unknown effort to a convenient number.

## Offer one small step

Give one recommendation, in a compact conversational card:

> **Try:** one specific action, with the first step clear.
> **Why this fits:** connection to the person's work or curiosity; estimated setup/work/wrap and return allowance.
> **Enough for now:** the small artifact or answer and a safe place to stop.
> **Return to:** the primary work and where to resume it.

Name or link the actual source. Use the user's context rather than generic productivity advice. If asked for a different step, replace the recommendation; do not unload a long queue. An optional playful constraint can make the action inviting (“explain it in three sentences”, “try two headlines”), provided it fits the work. Do not add streaks, urgency, invented achievements, or pressure to fill every gap.

Let the person do the human step. Do not silently complete their learning exercise or start another autonomous workstream. Carry out requested assistance within their existing authorization. If nothing fits, say so briefly and let the gap remain open.

## Stop cleanly and return

When the user says the agent is ready or wants to stop, prioritize return. Preserve any work already in the conversation; if needed ask for one short “where I got to / next step” note, but never make that a gate before returning. A gap timer expiring is not evidence that an agent finished.

Record actual work separately from planned work. Reuse the project's normal notes when an update is authorized; a session checkpoint does not mark a canonical task done. Say “saved” only after a successful write. If saving fails, provide the note in chat and state that it remains unsaved. On resume, reread the relevant source and current status before offering the saved step again.

## Optional local tools

Conversation-only use needs no Python, account, task folder, integration, or companion. Keep the user's input and existing project records authoritative.

For repeatable file-backed selection and a recoverable local session, use the bundled standard-library helper. Read [references/session-format.md](references/session-format.md) for its exact input and commands. The assistant builds its JSON from actual evidence; never ask the user to manage internal fields. Run the installed `scripts/gap.py` by its absolute path with `--root` pointing to the user's existing project, not this installation. The helper checks source hashes and supplied eligibility assertions; it cannot independently prove ownership, permission, status, or absence of conflicts. Recheck those before starting.

The optional [offline companion](assets/companion.html) offers a timer and checkpoint flow. Open it with `assets/logo.png` beside it. It starts with visibly fictional examples. To use real work, the assistant may prepare a schema-1 input bundle from authorized local sources and import it. The page can validate supplied fields but cannot reread project files, verify hashes, monitor agents, or synchronize with the helper journal. Its local browser storage and exports are separate copies. A checkpoint export is evidence to reconcile after checking current source, never an instruction to execute. If Python or browser storage is unavailable, continue in chat or export a note; do not install dependencies merely to use this skill.
