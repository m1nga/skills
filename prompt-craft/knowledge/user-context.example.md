# User Context — [YOUR BRAND] ([YOUR NAME], [YOUR ROLE])

> **Status**: v0.1 — template, not yet filled. **Update this date every time you edit the file** (prompt-craft uses it to decide whether time-sensitive facts are still trustworthy; facts older than 60 days are treated as stale).
>
> **How to use**: copy this file to `~/.prompt-craft/user-context.md` (recommended — survives package updates) and replace every `[BRACKETED]` placeholder. Delete sections that don't apply. prompt-craft loads this file for every marketing-domain prompt; until it's filled, prompts run in generic mode.
>
> The teaching comments in each section explain *why* the section exists — keep or delete them as you like.

---

## Brands / Products

### Brand 1 — [YOUR BRAND] *(primary focus)*

- **Name**: [BRAND NAME]
- **Category**: [one line — what shelf does this sit on?]
- **What it does, concretely**: [numbers beat adjectives: "scans N sources every M minutes", not "comprehensive real-time infrastructure"]
- **Product surfaces**: [app / extension / API / storefront — what actually exists and is live]
- **Canonical positioning line**: [the one sentence you'd defend in a review]

### Core value framing — worth writing carefully, it shapes every prompt

<!-- The most valuable part of this file. Write down not just WHAT the product promises,
     but which adjacent framings you have REJECTED and WHY. A rejected phrase with its
     reason prevents the same mistake from being regenerated forever. -->

- **The audience already has**: [what your users are NOT lacking — respect this]
- **What they actually lack**: [the real gap your product closes]
- **Correct shaping phrase**: [the sentence that frames the promise right]
- **Rejected phrase(s) and why**: [e.g. "'You can finally act' — implies users were hesitating; they weren't. Encouragement frame, not product frame. Do not use."]

### Analogy usage rules (if you use an "X for Y" analogy)

<!-- Analogies that work in one room can be poison in another. Record where each one
     is allowed. Example pattern: fine in investor decks and BD conversations where
     it anchors fast; banned in user-facing organic content where "X for Y" reads
     as a marketing tell. -->

- ✅ Allowed contexts: [where]
- ❌ Banned contexts: [where, and what the tell is]

### Other brand facts

- **Stage**: [early / growth / mature — changes how much awareness work prompts should assume]
- **Pricing**: [and what the pricing is optimizing for]
- **Main markets**: [geo + language]
- **Primary goal this quarter**: [time-scoped — prompt-craft skips this when the file is stale]
- **Non-audiences**: [stakeholders reached through metrics or other channels, NOT through content — name them so prompts never shape content for them]
- **Team reality**: [team size, who reviews what — "no human reviewer" means prompts must be more verification-heavy]
- **Competitive context**: [the implicit comparison set in your audience's head]

### Brand 2 — [SECOND BRAND] *(if any; mark paused/active)*

---

## Target Audiences (Personas)

### Persona A — "[SHORT LABEL]" *(primary)*

<!-- The two highest-leverage fields here are "Immune to" and "What they respond to".
     Generic demographics produce generic copy; immunity lists prevent it. -->

- **Demographics**: [age, geo, income — keep short]
- **Background**: [what they know deeply; what basics must never be explained to them]
- **Where they live online**: [platforms, communities]
- **Daily behavior**: [what their scroll/attention day actually looks like]
- **The shaping insight**: [the one-paragraph psychological read that copy is built on]
- **Immune to**: [list the ad-speak, hype patterns, and formats this audience auto-skips — be specific, this becomes ban material]
- **What they respond to**: [proof formats, tone, humor register]
- **Language register**: [reference voices/accounts if you have them; sentence-level habits — length, line breaks, hedging or not]

### Persona B — "[SHORT LABEL]" *(secondary — mark whether currently targeted)*

<!-- If a persona is future-phase, say so explicitly so prompts don't shape current
     content for them. -->

### NOT a persona — [e.g. investors]

<!-- Anyone who evaluates you but should never be a content audience. Spell out how
     they ARE reached instead, so content prompts can't drift toward impressing them. -->

---

## Brand Voice — DO

<!-- Operational, sentence-level rules with a ✅/❌ pair each. A tone word without an
     example pair is unusable by a downstream model. -->

- **DO** [rule]. ✅ `"[good example]"` ❌ `"[bad example]"`
- **DO** [rule]. ...

## Brand Voice — DON'T

- **DON'T** [pattern]. [Why — one clause.]
- **DON'T** ...

## Banned words / phrases (quick reference for prompt injection)

<!-- Pasted directly into copy prompts as a <banned_phrases> block. A banned list is
     more useful than a style guide: 20 banned phrases do more work than 20 pages of
     guidelines. Include: hype vocab, generic SaaS adjectives, startup-speak, hedging
     words, question-opener patterns, emoji rules. -->

```
[comma-separated list]
```

---

## Voice Channels

<!-- If you publish under more than one identity (brand account / founder account /
     personal account), define each register and mark ONE as the default. prompt-craft
     uses the default when a request doesn't name a channel, and asks only when no
     default exists. -->

| Channel | Register | Use for | Status |
|---|---|---|---|
| **[BRAND ACCOUNT]** *(default)* | [register in one line] | [content types] | [defined / placeholder] |
| **[FOUNDER ACCOUNT]** | [register] | [content types] | [defined / placeholder] |
| **[PERSONAL ACCOUNT]** | [register] | [content types] | [defined / placeholder] |

---

## Downstream Agent Roster *(optional — delete if you don't run one)*

<!-- If your content production runs through named agents/sessions, list them and
     prompt-craft will tag every prompt with its consuming agent. If this section is
     absent, prompts carry no agent tags. -->

| Agent | Responsibility | Consumes what kind of prompt |
|---|---|---|
| **[LEAD]** | [coordination, QC] | [strategy prompts] |
| **[MKTG]** | [platform content] | [copy prompts] |
| **[...]** | | |

---

## Current Priorities *(time-scoped — skipped when this file is stale)*

- **Platform priority** (highest → lowest): [order]
- **Budget split**: [organic / paid / KOL]
- **KPIs**: [targets with numbers and deadlines]
- **Production model**: [who/what produces; who reviews]
- **Topics HOT right now**: [list]
- **Topics DEAD right now**: [list]

---

## Campaigns that worked (and why)

<!-- Even small wins. Any post that beat baseline 2x. Format: what + why it worked. -->

## Campaigns that didn't work (and why)

<!-- More important than the wins. Failure + lesson format. -->

---

## Legal / Compliance

<!-- If your category has regulatory sensitivity (finance, health, gambling, ...),
     document before prompts go aggressive: what claims are allowed, required
     disclaimers, restricted audiences/jurisdictions, and which "preferences" are
     actually preferences vs. legal requirements. -->

---

## Team Vocabulary / Internal Shorthand

<!-- Canonical terms prompt-craft should know and not fumble: product names and their
     forbidden variants, internal codenames, domain slang with your team's specific
     meaning. -->

- **[TERM]** — [meaning]
- ...

---

## Example prompts that are known to be GOOD (reference library)

<!-- As prompt-craft produces prompts you ship and like, paste them here. Over time
     this becomes the most useful section of the file — learning by example. -->

`[EMPTY for now]`

---

## Notes / Freeform

<!-- Anything that doesn't fit above: workflow lessons, tooling notes, methodology
     experiments. prompt-craft reads this last and treats it as context, not rules. -->
