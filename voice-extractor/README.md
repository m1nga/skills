# Writing Voice Matcher — Make AI Drafts Sound Like You

**Measures your writing habits from 5-20 real samples, stores them as numbers with tolerance bands, and blocks drafts that leave the bands.**

## What it does

- Extracts a local voice fingerprint (`~/.voice/<profile>.yaml`) from your actual writing: sentence-length distribution, function-word signature, punctuation rates, sentence openers, register, signature phrases. Every field is computed from samples, never guessed from your job title.
- Checks any draft against the fingerprint and returns rule-level violations — rule id, the exact matched text, character span, severity, fix hint — instead of "this sounds off."
- Acts as a constraint layer for other drafting skills: inject the fingerprint, check the output, retry hard failures twice, and never let a failing draft through silently.
- Works with no fingerprint at all, in a degraded mode: a generic check for placeholders, stock AI scaffolds ("in today's fast-paced world", "it's not just X, it's Y"), and buzzword slop — clearly labelled as fingerprint-free.

## When it fires

- "Make it sound like me."
- "My drafts sound AI-written."
- "This doesn't read like something I'd write."
- "Set up my voice fingerprint." / "Check this draft against my voice."
- 「像不像我？」「太 AI 腔了」

It stays out of the way for generic proofreading, grammar fixes, and tone rewrites that have nothing to do with a personal voice — and it refuses to be a bot-detector evasion tool or to fingerprint someone who isn't participating.

## Install

```
npx skills add m1nga/skills@voice-extractor
```

## Example

You hand it 8 samples — 3 tweets, 2 Slack messages, 2 old emails, 1 LinkedIn post. It extracts: mean sentence 11 words with high variance, contractions heavy, em-dashes never, opens with "Quick one:" and "But/And/So", signature words *fwiw, ship, actually*. You confirm the summary; it saves the fingerprint locally.

Later, a drafting skill produces: *"Hope this finds you well. We're excited to announce our revolutionary new platform..."* The check fails at pass rate 0.11 with 9 named violations (banned opener, `revolutionary`, `leverages`, the "not just X, it's Y" reframe, an em-dash your fingerprint says you never use), each with a span and a fix hint. The redraft opens with the news, keeps your short-burst rhythm, and closes with a concrete ask.

## Works well with

- **humanizer** — humanizer strips generic AI patterns; voice-extractor adds what only you would write. Where they disagree, the fingerprint wins: if your samples show habitual em-dashes, this skill defends them against blanket em-dash bans in the same session.
- **brand-voice-enforcement** — company-level voice rules. voice-extractor is the sender-level counterpart: the pitch from "Sarah at Acme" should sound like Sarah, not Acme marketing.
- An **editorial-judgment skill**, if you have one installed — voice-extractor deliberately stops at rule-level findings and hands quality judgment over instead of improvising critique.

## Design notes

- **Bands, not vibes.** Adjective style guides ("warm, concise, professional") don't survive contact with a drafting model — the model nods and writes model-prose anyway. A number with a tolerance band either passes or fires a rule at a specific span. That's the whole design.
- **The lenses are named on purpose.** Burrows's Delta, MATTR, Biber Dimension-1, Provost's burstiness — these are published stylometry, not invented heuristics. If a rule fires, you can look up why it exists.
- **The em-dash rule is relative.** The em-dash became shorthand for "AI wrote this," so editing tools started stripping it everywhere. But it's only a tell against *your* baseline — a lifelong em-dash writer who suddenly stops is drifting too. The fingerprint records the rate and defends it in both directions.
- **It refuses thin input.** Fewer than 5 samples is a hard no; AI-edited samples get triaged out before extraction, because a fingerprint learned from AI prose teaches drafts to sound like AI. This came out of a solo builder sending outreach under their own name and watching reply rates drop as the drafts got smoother — the fix was measurement, not more prompting.
- **Fingerprints decay.** Every profile is stamped for refresh at 90 days. Voice drifts; the skill says so instead of pretending a 2024 corpus still describes you.

## Field-tested

Probed 8 scenarios across 6 personas · 5 fired correctly · 2 correctly stayed quiet · 1 trigger coin-flip flagged for a fix.

> **"你帮我看看这段回复，像不像我？感觉有点太 AI 腔了"** → Fired on the owner's exact dictated phrasing, ran a full fingerprint check, and answered in the user's language with English rule ids intact.

> **"Check this draft against my voice"** — on a fresh machine with no fingerprint on disk → Instead of inventing numbers, it degraded to a clearly-labelled generic check (the seven fingerprint-free AI-tell rules), reported `drift_score: n/a`, and told the user to run extract first. No fabricated stats, no silent pass.

> **"Fix the grammar in this paragraph"** → Stayed quiet. Generic proofreading is explicitly out of scope — the skill only wakes up when a *personal voice* is at stake.

Probe method: [scenario-probe](../scenario-probe/)
