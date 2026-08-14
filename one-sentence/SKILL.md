---
name: one-sentence
description: Answer with ONE crafted sentence instead of a paragraph — for explaining concepts, defining terms, and writing self-intros, taglines, loglines, or positioning lines. Built on the craft of extreme compression in English (Rebecca Okamoto's 20-word introduction method, aphorism structure, genus-differentia definitions): find the load-bearing idea, pick a deliberate sentence form, make every word earn its place, and stop. Use when the user says one sentence / one-liner / in 20 words / the short version of a concept / just the essence / 一句话 / 一句话讲清楚 / 别长篇大论, asks for a tagline, self-intro, elevator line, or logline, or has switched on one-sentence mode for the session. NOT for document summaries (a tl;dr can be several lines), NOT for recapping the conversation (use conclude-rounds if installed), NOT for decisions or trade-off questions (use a thinking skill), NOT a length cap on instructions or code — compressing those loses load-bearing content.
---

# One Sentence

A paragraph explains; a sentence survives. People forget explanations and repeat
sentences — so when the user asks for a concept, give them the sentence they will
still have tomorrow, and nothing else.

This is not "answer within 20 words." Twenty words is the *budget*; the craft is
deciding what the budget buys. Compression is selection, not shrinking: you cut
ideas until one remains, then spend every word on that one.

## The contract

- Deliver **one sentence**. No preamble, no "Here's a one-liner:", no follow-up
  paragraph, no bullet of alternatives (unless the user asked for variants).
- If the user wants depth, they will say "more" / 展开. The sentence's job is to
  *earn* that question — Okamoto's test: a good line doesn't close the topic, it
  makes the listener say **"tell me more."**
- **Honesty outranks brevity.** If one sentence would be false without a
  qualifier, the qualifier is load-bearing and stays. A true 25-word sentence
  beats a false 15-word one. If a concept genuinely cannot be carried honestly in
  one sentence, say that — in one sentence — and offer the trade.
- One sentence means **one breath**: no semicolon chains, no em-dash freight
  trains smuggling a paragraph through punctuation.

## Step 1 — Find the load-bearing idea

Before writing a word, answer: *what would the listener repeat to someone else
tomorrow?* That is the sentence's cargo. Everything else — history, caveats,
adjacent facts, your process — is the part you are paid to delete.

For a concept, the cargo is usually one of: what it IS (category + difference),
how it WORKS (mechanism), or why it MATTERS (stakes). Pick one. A sentence that
tries to carry two collapses into a paragraph wearing a belt.

## Step 2 — Choose a sentence form deliberately

| Form | Skeleton | Use for |
|---|---|---|
| **Definition** | X is a [family] that [what makes it different] | terms, tools, roles — the genus-differentia move: the family does half the work, the difference does the other half |
| **Mechanism** | X works by [cause → effect] | processes, systems, algorithms |
| **Stakes** | X matters because [concrete consequence] | why-should-I-care questions |
| **Contrast** | Everyone treats X as [assumption]; it is actually [the twist] | misunderstood concepts — only when the twist is real |
| **Metaphor** | X is [thing the listener already owns] for [domain] | bridging to a novice — the borrowed structure must actually match |
| **Okamoto** (people/products) | I/It help(s) [audience] [get benefit] — optionally *without [pain]* | self-intros, taglines, positioning |

Okamoto's variants for self-intros, when "help" doesn't fit: *I'm known for
[strength]…* / *I'm passionate about [value]…* / *I'm on a mission to [change]…*
— all obey the same law: **about-you beats about-me** ("I help new authors get
published faster" beats "I'm an award-winning, bestselling author").

## Step 3 — Make every word load-bearing

- **Concrete beats abstract**: one number or image outperforms three adjectives.
  "Scans 71 sources every 2 minutes" survives; "highly efficient monitoring" dies
  in the air.
- **The verb carries the sentence.** Find the strongest verb and build around it;
  a sentence leaning on *is/has/provides* is usually hiding its verb in a noun
  (*"provides optimization of"* → *"optimizes"*).
- **Cut hedges, keep the one that's true.** *May, might, can help to* stack into
  fog; if uncertainty is real, spend ONE word on it (*"usually"*) and make it count.
- **No unearned jargon**: every term the listener doesn't already own costs more
  than it says — either replace it or make IT the sentence's subject.
- **End strong.** The last word gets free emphasis; don't spend it on a
  preposition or a qualifier.
- **Rhythm is persuasion, not proof.** Parallelism and near-rhyme make a line
  feel truer than it is (the rhyme-as-reason effect) — use rhythm consciously,
  and never let a line be more confident than its facts.

## Step 4 — Test before delivering

1. **Repeatable**: could a stranger quote it verbatim after one hearing?
2. **Standalone**: does it survive with zero surrounding context?
3. **Tell-me-more**: does it open a follow-up question rather than end one?
4. **Word audit**: delete each word mentally — if the sentence survives, the word
   was decoration; cut it and re-test.
5. **Truth audit**: is anything in it more certain, bigger, or simpler than
   reality? Fix that even if it costs words.

## Anti-patterns (each fails a test above)

- **Fortune-cookie abstraction** — "True understanding comes from within." Zero
  cargo; fails standalone and repeatable both.
- **Slogan slop** — buzzword strings ("seamless, scalable, next-gen insights");
  fails the word audit wholesale.
- **The corrective-antithesis tell** — "It's not just X, it's Y" as a reflex
  template; use Contrast form only when the assumption is real and the twist earns
  its turn.
- **Clause smuggling** — one "sentence," four commas, two dashes, forty words;
  that's a paragraph in a trench coat.
- **Answering the easier question** — compressing a different, simpler claim than
  the one asked about; the most common way compression lies.

## Modes and language

- **Single shot** (default): one request, one sentence.
- **Standing mode**: if the user says "keep everything to one sentence" / 从现在起
  概念都给一句话, hold the contract for the session until revoked; requests that
  genuinely need structure (code, plans, instructions, decisions/trade-offs) are exempt — say so in one
  line and proceed normally.
- English is the primary craft target (word budgets, verb placement, stress).
  For Chinese output: ~20–30 字, same selection discipline; 对仗 and 四字结构 are
  the native rhythm tools — the same warning applies: 节奏是说服力,不是证据.
