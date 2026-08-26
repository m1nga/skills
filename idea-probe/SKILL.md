---
name: idea-probe
description: >-
  Wind-tunnel a new idea before anything gets built. When the user brings a product, skill, site, or
  feature idea and asks for a pre-build test — "simulate some users and test this", "probe this
  idea", 帮我模拟用户测测 / 新想法:先别建,推演一下 — derive 4–7 personas from the idea's claimed audience with forced
  diversity slots (age span, income tier, tech fluency, context and device, motivation strength),
  then run each through honest first-contact simulation: discovery → first-glance reading (misreads
  recorded verbatim) → start or not → first friction → return or not. Output: problems ranked by
  breadth (how many personas hit) × fatality, a fix per problem, a revised one-pager, and what only
  real users can prove — simulation, never market evidence. NOT for a bare "这个想法怎么样 / what do you
  think" (answer directly, or thinking-partner), NOT for instruction text or SKILL.md files
  (scenario-probe's seat), NOT for a built, runnable product (product-experience-officer's seat),
  NOT for pure technical feasibility (research, not personas).
---

# Idea Probe（想法风洞）

An idea is cheapest to fix while it is still only an idea — and hardest to see
clearly, because its author simulates exactly one user: themselves. This skill
runs the idea through a wind tunnel of people who are deliberately *not* the
author, before a line of it exists.

The object is always **an unbuilt idea** — a product, a skill concept, a site, a
feature. Instruction text that already exists goes to scenario-probe; a product
that already runs goes to product-experience-officer. This skill sits upstream of
both.

When it is unclear whether the object exists yet — 「测测我这个网站」 could be
either — ask one line first: "built yet, or still an idea?" Only then start the
probe.

## Step 1 — Cast the persona matrix

Derive 4–7 personas from the audience the idea *claims* to serve. Not from who
the author imagines enjoying it — from who the pitch, if taken at its word, would
have to work for.

**Forced diversity slots** — the matrix is invalid until it spans:

| Slot | Must cover |
|---|---|
| **Age** | A real spread across the claimed range (e.g. 16–50 if the pitch says "everyone") — not five variations of thirty-two |
| **Income** | At least two tiers; price sensitivity changes what "worth trying" means |
| **Tech fluency** | From "installs anything" down to "distrusts app permissions" — as low as the claimed audience honestly reaches |
| **Context & device** | Where and on what: commute phone, shared family laptop, work desktop with IT policies, spotty rural connection |
| **Motivation** | At least one persona who *mildly* wants this and one who barely cares — high-motivation users forgive everything and prove nothing |

Each persona gets a name and ONE sentence of life background — enough to predict
behavior, not a character study. If the idea's claimed audience is genuinely
narrow ("retired ICU nurses"), diversity moves *inside* the niche (age within the
band, tech comfort, motivation) — the slots bend, they never disappear.

At least half the cast must be people the idea's author would find unfamiliar.
The author's lookalikes may hold at most one seat.

## Step 2 — First-contact simulation（首次接触模拟）

Walk every persona through five stations, honestly. The simulation is allowed to
end at any station — "she never finds out it exists" is a complete and valuable
run, not a failed one.

1. **Discovery** — how does this persona plausibly encounter the idea? Name the
   channel. If no plausible channel exists for them, stop here and record it.
2. **First-glance reading** — what do they think it *is* from the name and
   one-line pitch alone? **Record the misread verbatim, before explaining
   anything.** First impressions are perishable evidence: once the correct
   reading is stated, the confusion cannot be re-experienced, so it is written
   down raw first and interpreted second.
3. **Start or not** — do they take the first action (sign up, install, try)?
   What tips the decision — and what would this persona *instead* keep doing,
   since "nothing" is rarely the true competitor?
4. **First friction** — where do they first get stuck, confused, or bored?
   One concrete moment, not a category.
5. **Return or not** — a week later, do they come back? Why, honestly?

No advocating. The probe's job is to find where the idea loses people, and a
persona who "loves everything" is a sign the persona was cast wrong, not that
the idea is ready.

## Step 3 — Rank the problems

Collect every problem the runs surfaced and sort by two dimensions:

| | Fatal when hit | Annoying when hit |
|---|---|---|
| **Many personas hit it** | Fix before anything else | Fix in v1 |
| **Few personas hit it** | Decide: is this persona core? If yes, fix; if no, name the trade-off | Backlog, honestly labeled |

"Fatal" means the persona does not start, or does not return — not "seemed
suboptimal". Each problem cites which personas hit it and at which station.

## Step 4 — Fixes and the revised one-pager

Every ranked problem gets a concrete fix — a change to the idea, not a hope
about the users. Then write the **revised one-pager**: the stronger version of
the idea with the fixes folded in — what it is, who it is for (now honestly
scoped), the first-contact path that survived the probe, and what was cut.
The one-pager is the deliverable the user builds from; the probe report is its
evidence.

## Step 5 — What only real users can prove（只有真实用户能证明的事）

The report MUST end with this list, and it may not be empty. Persona simulation
finds design problems; it cannot prove demand, price tolerance, retention, or
channel economics — those numbers live only in reality. Typical entries: "that
persona 3's discovery channel actually converts", "that anyone pays at this
price", "that week-two retention exists at all". This section is the firewall
between a useful wind tunnel and a fabricated market study: a probe report
presented as validation is worse than no probe at all.

## Report shape

Deliver in the user's language, in this order: verdict paragraph (would you
build this as pitched — one honest paragraph) → persona matrix → per-persona
runs → ranked problems with fixes → revised one-pager → what only real users
can prove. Deliver in-chat; write to a file only when asked, at a path the user
chooses.

## Boundaries

- **Simulation, never validation.** The probe's outputs are hypotheses with
  reasoning attached. Never present persona reactions as evidence of market
  demand, and never let the report's confidence exceed a thought experiment's.
- A probe where every persona sails through means the cast was drawn in the
  author's image — recast with stranger strangers and rerun. Zero findings is
  evidence about the probe, not the idea.
- The probe does not build. After the revised one-pager, construction belongs
  to the user's build workflow. If the idea is itself a skill and extend-first
  is installed, let it check the shelf first — an EXTEND verdict ends the probe
  before it starts, five seconds against half an hour.
- Sibling seats, restated: existing instruction text → scenario-probe (if
  installed); a runnable product → product-experience-officer (if installed);
  "can this be built at all" → technical research, not personas. When the
  matching sibling is not installed, do not run the persona matrix on the wrong
  object — degrade in place to an ordinary review of it.
