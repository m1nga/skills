# grilling

An interview protocol that refuses to start building until your plan survives questioning — one question at a time, each arriving with a recommended answer, ending in a plan that states what you are NOT doing.

## What it does

`grilling` runs three phases: GRILL, PLAN, EXECUTE. The grill phase walks the design tree of your plan, asking exactly one question per turn and always attaching its own recommended answer — you confirm or redirect instead of facing a blank decision. Every few questions it injects a perspective from outside your frame. Before planning, it restates your problem in one sentence you didn't use; if the real problem differs from the stated one, that's where it surfaces. The locked plan includes explicit non-goals, checkpoints, and drift triggers, and execution waits for your explicit "go".

## When it fires

- "Grill me on this plan before we build it."
- "Poke holes in this design — I don't trust it yet."
- "Interview me until this feature is fully scoped."
- "Ask me everything you need before writing any code."
- 「开工前把我问透。」
- 「拷问一下这个方案。」

It deliberately does not fire on "just do it" / "you decide" / 「你看着办」 — those authorize execution, not an interview. For light feedback on a plan, or open-ended thinking with no build attached, use `thinking-partner` instead.

## Install

```
npx skills add m1nga/skills@grilling
```

## Example

> **You:** Grill me on this: I want to add offline sync to my notes app.
>
> **Claude:** Q1 — When the same note is edited offline on two devices, what wins? **My recommendation:** last-writer-wins per field — your notes are single-user, and field-level merging covers most collisions without a CRDT. Confirm or redirect?
>
> **You:** Confirmed.
>
> **Claude:** Q2 — ...

Eight questions later you get a plan whose "What we are NOT doing" section reads: no CRDT, no multi-user sharing, no conflict-resolution UI in v1.

At any point, say "just decide" (or 「别问了」) and it collapses every remaining question into its own recommended answer and hands you the full plan anyway.

## Works well with

- `thinking-partner` — for the stage before you have a build: deciding what is worth building at all. `grilling` takes over once there's a concrete thing to scope.

## Want a `/grill-me` alias?

`/grilling` is directly invokable — an alias adds nothing functionally. If you prefer typing `/grill-me`, create a skill directory named `grill-me` next to your other skills with this exact 7-line SKILL.md:

```markdown
---
name: grill-me
description: Alias for /grilling — run a relentless plan interview. Requires the grilling skill to be installed.
disable-model-invocation: true
---

Run a `/grilling` session.
```

`disable-model-invocation: true` keeps the alias off the model's trigger surface, so only you can invoke it by name — semantic triggering lives entirely in `grilling`. (The key is Claude Code-specific; engines that don't recognize it ignore the line harmlessly.)

## Design notes

This skill comes out of a solo builder's post-mortems, where the recurring failure was never bad code — it was building the wrong thing confidently. The opinions baked in:

- **One question at a time, always with a recommendation.** A wall of questions gets skimmed; a bare question hands the decision back with no anchor. A recommendation you can veto is the fastest honest path through a design tree.
- **"What we are NOT doing" is mandatory, not optional.** Scope creep doesn't announce itself; the only working defense is a list of tempting-but-excluded items agreed on before the first line of code.
- **Drift triggers are named in advance.** "We've gone off-scope" is easy to wave away mid-flow — unless the plan itself already says what off-scope looks like.
- **The exit valve is part of the protocol.** Willingness to be grilled is a mood, not a contract. The moment you say "just decide", the interview folds into recommendations and you still get the full plan structure — the protocol never punishes you for wanting out.

## Field-tested

Probed 7 scenarios across 6 personas · 4 fired correctly · 2 correctly stayed quiet · 1 edge flagged for a description patch.

> **"开工前把我问透,这个切片方案"** → Fired. One question per turn, each arriving with a recommended answer to veto — and「别问了」collapses the rest into recommendations without losing the plan.

> **"方案就按你说的来吧,你看着办,直接开工"** → Stayed quiet. Delegation grants execution, not an interview — the exclusion this clause was written for, verified working.

> **"Ask me everything you need before writing code — a CLI to dedupe my photo library."** (stranger, only this skill installed) → Full walkthrough with no dead ends: interview → one-sentence reframe → locked plan whose "What we are NOT doing" section exists before the first line of code.

Probe method: [scenario-probe](../scenario-probe/)
