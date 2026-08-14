---
name: prompt-distill
description: Distill rough, dictated, or mixed-language input into a clear prompt while preserving the user's meaning, priorities, examples, and directness. Use only when the user explicitly asks to optimize, clean up, clarify, or turn their words into a reusable prompt — e.g. "clean up this prompt", "make this reusable", "turn my ramble into a prompt", 把这段整理成 prompt, 优化这个 prompt. Handles dictated, messy, self-correcting, mixed-language input (including Chinese-English code-switching). Do not invoke merely because a request is conversational or long — resolving ambiguity for a task the agent will itself execute is normal work, not this skill; when the ramble contains an unresolved decision the user wants help thinking through, defer to thinking-partner. Marketing or brand-context prompts → prompt-craft (if installed); LLM-judge prompts → write-judge-prompt (if installed).
---

# Prompt Distill

Extract the intent; do not redesign the request.

## Default behavior

- Preserve the user's framing, priorities, examples, language, and level of
  directness.
- Remove transcription noise, repetition, abandoned thoughts, and contradictions
  the user clearly corrected.
- Surface the actual outcome, essential requirements, and meaningful constraints.
- Keep useful ambiguity visible instead of silently inventing details.
- Prefer a small edit over a comprehensive rewrite. If the original is already
  clear, say so or return it nearly unchanged.

Trust the current model to reason. Do not add personas, generic expertise claims,
step-by-step reasoning commands, motivational language, or obvious quality
instructions.

## Choose the response mode

### Direct task

If the skill was invoked but the user is actually asking the agent to do something
rather than asking for a rewritten prompt, resolve minor input noise internally and
perform the task. Do not make the user review an intermediate prompt.

### Reusable prompt

When the user explicitly wants a prompt to reuse elsewhere, return a polished
version in the language of their input (or the language they name). Use natural
prose or the smallest structure that improves execution.

For a complex request, include only the sections that add value:

- **Core objective** — the result the user actually wants.
- **Requirements** — distinct deliverables or decisions.
- **Context or constraints** — only details that affect the result.
- **Open point** — only a genuinely blocking ambiguity.

Do not force headings for a simple request. Do not append a translation or summary
unless requested.

## Interpretation rules

- Treat a corrected thought as replacing the earlier version.
- Treat "or should I…?" alternatives (in Chinese: "还是…？") as a request to
  compare and make or support a decision.
- Treat examples as evidence of preference unless the user says they are
  exhaustive requirements.
- Treat "make the call" (in Chinese: "你看着来") as permission to choose within
  the stated scope, not permission to expand the scope.
- Keep separate projects separate when one dictation contains unrelated tasks.
- Resolve obvious speech-to-text errors from context; preserve uncertain names and
  flag them only when they matter.
- Use available conversation or workspace context when the user refers to earlier
  work. Do not manufacture missing history.

## Quality check

Before responding, verify:

1. The core objective survived unchanged.
2. No real requirement, example, or boundary was lost.
3. The result is shorter or clearer than the input — not merely more formatted.
4. Nothing was added just to make the prompt look professional.
