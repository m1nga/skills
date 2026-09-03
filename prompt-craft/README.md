# Marketing Prompt Builder — Turn Rough Ideas into Brand-Ready AI Instructions

Turns "write me a prompt for a TikTok ad" into a prompt that carries your brand voice, platform constraints, and banned-word list — with a line-by-line map showing where every detail you said ended up.

## What it does

- Transforms rough ideas, dictated voice notes, and revision feedback into structured, copy-paste-ready prompts for marketing work: social posts, ad copy, video scripts, campaign briefs, brand-voice definitions.
- Grounds every prompt in your brand context file (voice rules, personas, banned phrases) plus a marketing knowledge base: platform specs, headline/hook/CTA patterns, funnel logic, and 25 known ways marketing prompts fail.
- Preserves every concrete detail you gave — numbers, names, constraints — and proves it with a "you said → I wrote" mapping in every delivery.
- Adds a 1-3 line advisory: format, platform, or structural choices you didn't ask about but should know about.
- Treats follow-ups as amendments (v1 → v2 → v3), never restarts. A DEEP mode adds failure-mode analysis and an adversarial review pass for high-stakes prompts.
- Handles dictated, messy, mixed-language input, including Chinese-English code-switching, with a correction dictionary you can extend.

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
npx skills add m1nga/skills@prompt-craft
```

Then copy `knowledge/user-context.example.md` to `~/.prompt-craft/user-context.md` and fill in your brand. Until you do, it runs in generic mode and tells you so.

## Example

**Input (dictated):** "ok tweet about the arb we caught this morning, the 6 cent gap, um it was 71 on one venue 65 on the other, don't explain the math just show it, you know the format"

**Output:** a structured prompt containing the exact numbers (71¢ / 65¢, both venues named), your brand's banned-phrase block, the platform's receipt-format conventions, an execution-discipline block — and a verification summary mapping "don't explain the math" to the injected rule "give raw numbers, let the reader compute the implication," flagging "you know the format" as resolved from your context file's reference library.

## Works well with

- **prompt-distill** — general-purpose prompt cleanup without the marketing knowledge base. Non-marketing prompts get handed off there.
- **thinking-partner** — when your ramble contains an unresolved decision ("should this even be a video?"), think first, craft the prompt after.

## Design notes

Built by a solo builder running content production through AI agents with no human reviewer at any step — which is why the output format is verification-heavy: an execution-discipline block in every prompt, a mandatory "you said → I wrote / I added / I guessed" accounting in every delivery. When nobody proofreads downstream, the prompt has to carry its own checks.

Two deliberate asymmetries. Input handling defaults to preservation over invention: when in doubt, every specific you said survives into the prompt, because dropping a number is a worse failure than keeping a redundant one. And the skill is split into an engine (this package: methodology + generic marketing knowledge) and a brand payload (your private context file, which lives outside the package and survives updates). Brand context also carries a staleness date — a 90-day-old sprint goal silently injected into fresh copy is a bug, so time-scoped facts expire after 60 days.

## Field-tested

Probed 9 scenarios across 7 personas · 5 fired correctly · 2 correctly stayed quiet · 1 clean mode exit · 1 sibling boundary flagged.

> **"Write me a prompt for a TikTok ad for our sleep app"** (fresh install, no brand file) → fired, ran in generic mode with a one-line setup notice — no dead end, no invented brand facts.
>
> **"Write a TikTok ad script for our sleep app."** → stayed quiet. You asked for the copy, not a prompt; that's normal work, and this skill knows the difference.
>
> **Brand context file dated 5 months ago** → stable facts (voice, banned words) still injected; stale sprint KPIs and "hot topics" skipped, with a one-line notice to refresh — a 90-day-old goal never leaks into fresh copy.
>
> **"先别优化了,帮我看下这个报错"** (mid-session pivot) → exited workshop mode immediately and just helped. No format ceremony, no mode trap.

Probe method: [scenario-probe](../scenario-probe/)
