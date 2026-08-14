# conclude-rounds

Recap the last N rounds of your current agent session — and refuse to let "I wrote the code" pass as "the code works".

## What it does

When a long back-and-forth gets hard to track, this skill re-reads the last N exchanges (default 4) and gives you a tight, honest recap: what you asked, what was actually done, and what's still open. Its one non-negotiable rule: every item is sorted into **done-and-verified**, **done-but-unproven**, or **merely proposed** — because an agent's confident claim and a passing test are not the same thing. It then mines those same rounds for up to 5 workflow insights, each tied to a concrete mechanism in the engine you're using (a hook, an instruction-file rule, a reusable prompt) with a one-line first step. If the rounds only support 2 real insights, you get 2.

It runs entirely in-context and is read-only: no files edited, no transcripts pulled from disk, no cross-session digest.

## When it fires

- "Recap the last few rounds"
- "What did we just do?"
- "Catch me up on this thread"
- "Wait — what actually got done vs just discussed?"
- "总结前面4轮"
- "这几轮做了啥？"

## Install

```
npx skills add m1nga/skills@conclude-rounds
```

## Example

> **You:** catch me up on the last 3 rounds
>
> **Agent:**
> **Bottom line:** auth middleware refactored and tested; rate-limiter written but never run; DB migration still awaiting your choice of strategy.
>
> - Round 1: you asked to refactor auth middleware → done, 14 tests pass (✅ verified)
> - Round 2: rate-limiter added to `api/limits.ts` → written, never executed (⚠️ unverified)
> - Round 3: two migration strategies proposed → waiting on you (💡 proposed)
>
> **Workflow insights:**
> 1. You manually re-ran the test suite after each edit (rounds 1–2) → a PostToolUse hook can do that automatically → first step: add a hook running `npm test` on Edit.
> 2. ...

## Works well with

- [`iteration-close`](../iteration-close/) — this skill closes a stretch of conversation; that one closes a whole product iteration.

## Design notes

This skill comes from a solo builder's recurring failure mode: after 20 rounds of agent-assisted work, the transcript said everything was done — and half of it wasn't. Code had been written but never run; decisions had been "agreed" that were actually still open. The three-state sort (verified / unproven / proposed) exists because the cost of a false "done" is a rebuild days later.

The insights section is deliberately strict: every insight must cite evidence from the rounds just recapped, name a mechanism you can actually configure, and end with a first step. Generic advice ("consider using subagents") is banned by the skill text itself, and it is told to deliver fewer than 5 rather than pad — and never to repeat an insight it already gave earlier in the session.

## Field-tested

Probed 7 scenarios across 5 personas · 4 fired correctly · 2 correctly stayed quiet · 1 flagged as a coin-flip (fix queued).

> **"wait, catch me up — what did we actually finish vs just talk about?"**
> → Fired. Recap sorted every item into verified / unproven / proposed — the rate-limiter that was written but never run stayed ⚠️, not ✅.

> **"recap what we did across yesterday's session and today"**
> → Correctly stayed quiet. Cross-session digests are explicitly out of scope; this skill only re-reads the conversation you're in.

> **"这个迭代做完了，总结一下"**
> → Correctly yielded to `iteration-close`. Closing a whole iteration is its sibling's job; this skill recaps a stretch of conversation, nothing more.

Probe method: [scenario-probe](../scenario-probe/)
