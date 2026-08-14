# one-sentence

**Ask about a concept, get one sentence a stranger could repeat tomorrow.**

## What it does

Most explanations die because they were paragraphs. This skill answers with a
single crafted sentence — built on the craft of extreme compression in English:
Rebecca Okamoto's 20-word introduction method (TED), genus-differentia
definitions, and aphorism structure. Twenty words is the budget; the skill's job
is deciding what the budget buys. It selects one load-bearing idea, picks a
sentence form on purpose (definition, mechanism, stakes, contrast, metaphor, or
Okamoto's "I help X get Y"), spends every word on specifics, and stops.

It also holds an honesty line most compression advice skips: if one sentence
would be false without a qualifier, the qualifier stays. A true 25-word sentence
beats a false 15-word one.

## When it fires

- "Give me the one-sentence version of event sourcing."
- "Introduce me in 20 words for this panel."
- "What's a good logline for this product?"
- "一句话讲清楚什么是 RAG。"
- "From now on, keep concept answers to one sentence." (standing mode)

It stays quiet for document summaries, decisions, and instructions — compressing
those loses load-bearing content, and it says so in one line.

## Install

```bash
npx skills add ming4uk/skills@one-sentence
```

## Example

> **You:** one sentence — what is a scenario probe?
>
> **Claude:** A wind-tunnel test for instruction text: it simulates real users
> against your skill's trigger surface before real sessions pay for the misfires.

No preamble, no follow-up paragraph. Say "more" when you want the depth back.

## Works well with

- [scenario-probe](../scenario-probe/) — probe reports need one-line verdicts
- [prompt-distill](../prompt-distill/) — distill the prompt, then compress the pitch
- [product-experience-officer](../product-experience-officer/) — its 判词 (opening verdict) is a one-sentence discipline

## Design notes

The reference points are public craft: Okamoto's about-you formula ("I help new
authors get published faster" beats "I'm a bestselling author"), the
genus-differentia move that makes dictionary definitions work, and the
rhyme-as-reason caveat — rhythm makes a line feel truer than it is, so the skill
treats rhythm as persuasion, never as proof. The delivery contract (one sentence,
no scaffolding, "tell me more" earned rather than assumed) is the point: the
skill exists because models default to paragraphs and humans remember sentences.
