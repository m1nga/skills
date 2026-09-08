# Marketing Prompt Builder — Turn Rough Ideas into Brand-Ready AI Instructions

Turns rough marketing notes into a usable prompt that preserves product facts, audience and brand voice, with extra structure only when the task needs it.

## What it does

- Turns marketing notes and revisions into a reusable prompt that preserves product facts, audience, voice and constraints.
- Uses supplied product context first, then applicable project or personal brand files. Loads topic references only when useful.
- Keeps simple prompts short. Adds a detail mapping or deeper failure review when the task warrants it.
- Answers side questions and follows explicit requests to execute the prompt; drafting itself does not authorize external publication.
- Handles dictated and mixed-language input without turning tentative ideas into approved decisions.

## When it fires

- "Write me a prompt for a TikTok ad."
- "Turn these voice notes into a prompt for the launch thread."
- "I need a prompt that gets better ad copy out of the model."
- "Make this campaign brief AI-ready."
- 「帮我写个营销 prompt」
- 「把这段语音整理成投放 prompt」

It does not activate for general prompt polishing, system prompts, or coding prompts — those belong to prompt-distill. Writing the marketing copy itself is normal work, not this skill.

## Install

```
npx skills add m1nga/prompt-craft
```

Use it immediately with supplied product facts. Optionally copy `knowledge/user-context.example.md` to a project `user-context.md` or personal `~/.prompt-craft/user-context.md` for recurring brand work.

## Example: launch notes without invented proof

Authored demonstration; no campaign performance is claimed.

**Input:** “Use prompt-craft. Build a prompt for a short launch post for our offline
notes app. It exports Markdown. No customer numbers yet. Calm voice; invite people
to try it. No brand file.”

**Downstream prompt:**

```text
Write one short launch post for an offline notes app that exports Markdown.
Use a calm, direct voice and end with one invitation to try it.
Use only these supplied product facts; do not add customer counts, testimonials,
time savings, pricing, or a download URL. Ask for a verified URL if one is needed.
```

**Verification excerpt:** offline notes + Markdown preserved; no customer numbers
preserved as a claim boundary; calm voice and one invitation preserved. Generic
mode is disclosed. The prohibition on unsupported claims is added evidence hygiene.

**Recovery:** “Use the usual format” with no context file stays unresolved; the
prompt can propose a plain short post, labelled as an assumption, without inventing
a brand format or importing a fictional knowledge-base company.

## Works well with

- **prompt-distill** — general-purpose prompt cleanup without the marketing knowledge base. Non-marketing prompts get handed off there.
- **thinking-partner** — when your ramble contains an unresolved decision ("should this even be a video?"), think first, craft the prompt after.

## Design notes

Current agents can reason from clear goals and constraints. This skill supplies
marketing context, preserves revisions and separates facts from assumptions; it
should not force a long workshop around a short request. XML, extra advice, trace
tables and deep review are optional tools rather than mandatory output sections.

Project-specific context takes precedence over a personal fallback. Reference
examples are not customer evidence, and dated campaign facts require checking.
Private brand files remain outside the installed package and survive updates.

## Validation

The September 8, 2026 review used maintainer walkthroughs for a simple prompt,
missing context, dense revisions, a mid-task question, direct copywriting and stale
brand facts. These are instruction simulations, not human trials or measured
Astra performance. The skill structure and public product page are also validated.

The short authored example above remains a useful output shape. A future real
campaign or target-model comparison is needed to establish marketing performance.
