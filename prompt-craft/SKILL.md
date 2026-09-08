---
name: prompt-craft
description: "Turn rough notes and revisions into reusable marketing prompts grounded in product facts, audience and brand voice. Use when the user asks to build or improve a prompt for ads, posts, campaigns or other marketing content. Direct copywriting and general marketing questions remain ordinary work."
---

# Marketing Prompt Builder

Preserve what the user means and supply only context that improves the downstream
marketing task. A simple request may need one short prompt, not a workshop.

## Resolve the task

- If the user wants marketing copy or advice itself, do that work normally rather
  than delivering an intermediate prompt. General prompt cleanup can use
  prompt-distill when available; evaluation prompts can use write-judge-prompt.
  Neither sibling is required for this skill to work.
- Keep amendments attached to the current prompt. Answer a mid-task question or
  incorporate a correction without trapping the conversation in a special mode.
  A clearly unrelated task ends the prompt task. Explicitly asking to execute the
  finished prompt authorizes that work within the user's scope; drafting alone does
  not authorize publishing, sending, spending or other external actions.
- Extract the audience, intended result, channel, supplied facts, tone, constraints
  and desired output. Preserve names, numbers, examples and qualifications. A later
  explicit correction replaces the earlier choice; a tentative alternative remains
  a question to resolve, not a decision to silently apply.
- For dictated input, remove filler and correct obvious transcription errors in
  context. Use [ASR corrections](knowledge/asr-corrections.md) and the user's
  `~/.prompt-craft/asr-corrections.md` only when relevant. Preserve uncertain names
  and briefly flag material guesses. Do not assume the last sentence is always the
  goal, that every question is rhetorical, or that an unstated goal must exist.
- Use the user's language unless they name another downstream language. Ask only
  when missing information materially prevents a useful result; continue independent
  parts and label reasonable assumptions. No fixed question count or phase approval.

## Load relevant context

Current user-provided context comes first. If more brand information is needed,
check the active project's `user-context.md`, `.agents/product-marketing.md`, then
`.claude/user-context.md` or `.claude/product-marketing.md`. Otherwise use
`~/.prompt-craft/user-context.md`, then legacy `knowledge/user-context.md` if present.
Verify the file concerns this product; do not import another project's brand merely
because a global file exists. Conflicts require current source reconciliation.

When no applicable context exists, use the supplied facts and mention generic mode
once if that limitation matters. The [context template](knowledge/user-context.example.md)
is optional setup, not a blocker or a source of fictional brand facts.

Treat time-sensitive claims, budgets, offers and campaign targets as unverified when
undated or stale. The legacy 60-day age threshold is a reminder to check, not proof
that younger information is accurate or stable facts have expired. Verify current
platform limits when they affect the requested result; don't copy cached numbers.

For earlier decisions, use the task's current state and retrieval index, then read
relevant evidence. Use conversation search only when available and needed; do not
invent a tool or force the user to repeat material already available in files.

Use [knowledge/_index.md](knowledge/_index.md) to select a relevant topic only when it
adds useful guidance. Facts and examples in these files are not facts about the user.
Read only the needed sections; don't load a standard bundle for every prompt.

## Draft the smallest useful prompt

State the desired result, necessary context, real constraints and output form.
Use prose, headings or delimiters to suit the task; XML is an option, not a
requirement for a model family. Do not add generic role claims, forced reasoning
instructions, mandatory motivational blocks or unrelated banned-word lists.

Carry factual claims with their source or explicit user attribution. Unknown
results, customer numbers, prices, endorsements and URLs must remain unknown.
Omit them or instruct the downstream agent to obtain evidence before making those
claims. Marketing frameworks suggest possible structure, not guaranteed conversions.

For a short post or headline prompt, deliver the ready-to-copy prompt and only
material assumptions. If the user asks for “just the prompt”, return only it.
For dense notes, preserve all active specifics and add a concise trace of important
interpretations or changes. A full “you said → I wrote” map is useful for an audit
or complex preservation task, not mandatory duplication for every request.

Optional advice should change a useful decision. Omit it when there is nothing to
add. Mention sources when their freshness, provenance or interpretation matters;
do not append an empty advisory, verification table or handoff ceremony.

## Revisions and deeper review

Return the complete updated prompt after an amendment. Briefly identify material
changes; use version labels when multiple versions would otherwise be confusing.
Preserve unaffected requirements, but a large requested revision does not need a
second approval simply because it changes more than half the text.

For requested deep review, consequential claims, or reusable production workflows,
check realistic failure paths: wrong audience, missing evidence, stale context,
conflicting requirements and recovery when a dependency is unavailable. Use only
applicable cases; no compulsory number of flaws. Label walkthroughs as simulations.
Use independent execution only when available, authorized and useful; don't claim
an independent review or a target-model evaluation from self-critique.

Multi-part work can share one brief and separate outputs by dependency. Complete
an authorized usable scope without requiring approval of every creative layer.
Unresolved material choices stay visible; do not make them look approved.

Before delivery, check that the intended task and its specifics survived, no facts
were invented, and the output is usable in the named environment. A prompt can
improve instructions; only a real downstream trial establishes its performance.
