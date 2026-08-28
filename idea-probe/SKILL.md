---
name: idea-probe
description: >-
  Wind-tunnel a new idea before anything gets built. When the user brings a product, skill, site, or
  feature idea and asks for a pre-build test — "simulate some users and test this", "probe this
  idea", 帮我模拟用户测测 / 新想法:先别建,推演一下 — derive 4–7 personas from the idea's claimed audience with forced
  diversity slots, then run each through honest first-contact simulation: discovery → first-glance
  reading (misreads recorded verbatim) → start or not → first friction → return or not. Output:
  BUILD/NARROW/RETHINK verdict with assumption debt, problems ranked by breadth × fatality, a fix
  each, a revised one-pager, and a reality bridge: real-user tests with kill criteria for the
  deadliest findings — simulation generates hypotheses, never market evidence. NOT for a bare
  "这个想法怎么样 / what do you think" (answer directly, or thinking-partner), NOT for instruction text or SKILL.md files
  (scenario-probe's seat), NOT for a runnable product (product-experience-officer's seat), NOT
  for technical feasibility (research, not personas).
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

## Step 0 — The pitch is testimony, not fact（用户输入即假设）

Before casting anyone, tag what the pitch itself claims. Its audience, price,
and channel are the author's statements, not the probe's ground truth — each
gets one label: **hunch** (the author believes it), **observation** (the
author has seen it, uncited), or **data** (a source exists). The probe runs on
the claims as stated, but the report carries a section — "risks in what you
told me" — naming the claims the whole probe leans on and how thin their
labels are. A wind tunnel that inherits the pitch's assumptions unlabeled is
just the author's head with extra seats.

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

**Size the run to the summons.** A quiet trigger — the idea arrived in passing,
the trigger phrases merely matched — gets a quick probe: 3 personas, the
stations compressed, the report cut to the verdict, top problems, and the
gate's mandatory lines — compressed, not skipped. An explicit invocation
("run idea-probe on this", "full probe") gets the full 4–7 matrix. The
diversity slots bind in both sizes; only the seat count and report length
change. Don't dump a full wind tunnel on someone who mentioned an idea over
coffee; don't hand a one-liner to someone who asked for the works.

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
   since "nothing" is rarely the true competitor? **Anchor the decision in
   past behavior:** what did this persona actually do the last time this need
   arose, and what did they spend on it — money, time, effort? A persona with
   no past expenditure on the problem is holding a fake job; their "I'd try
   it" is written down and weighted near zero.
4. **First friction** — where do they first get stuck, confused, or bored?
   One concrete moment, not a category.
5. **Return or not** — a week later, do they come back? Why, honestly?

No advocating. The probe's job is to find where the idea loses people, and a
persona who "loves everything" is a sign the persona was cast wrong, not that
the idea is ready. Two anti-performance rules make that structural instead of
a vibe:

- **Zero-friction burden of proof.** A persona who sails through all five
  stations must come with three concrete facts from their one-sentence life
  background that explain the smooth pass — the commute that fits the use
  moment, the tool they already pay for that this replaces, the motivation
  slot they occupy. If the three facts can't be produced, the run is invalid:
  rerun it, honestly.
- **Homogeneity detection.** If every persona stalls — or passes — at the
  same station in near-identical words, that is one perspective narrated in
  different voices, not several people. Swap at least two personas for
  stranger ones and rerun before reporting anything.

## Step 3 — Rank the problems

Collect every problem the runs surfaced and sort by two dimensions:

| | Fatal when hit | Annoying when hit |
|---|---|---|
| **Many personas hit it** | Fix before anything else | Fix in v1 |
| **Few personas hit it** | Decide: is this persona core? If yes, fix; if no, name the trade-off | Backlog, honestly labeled |

"Fatal" means the persona does not start, or does not return — not "seemed
suboptimal". Each problem cites which personas hit it and at which station.

**Consensus escalation, as an explicit rule:** when two or more personas hit
the same problem at the same station *in their own distinct words*, the
problem is promoted one severity tier — written as a promotion, not felt as
one. (Identical words is not consensus; it is the homogeneity failure above,
and triggers a recast instead.)

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

### The reality bridge（真实验证桥）

The list alone is not enough. For the one or two most fatal ranked problems,
attach an executable real-human test:

- **Who to find** — defined by behavior, never demographics: "people who paid
  for X in the last six months", "people who switched tools this year". Not
  "ages 25–40"; a demographic finds people who resemble the user, behavior
  finds people who *are* one — and name one reachable channel — a subreddit,
  a group chat, a queue they stand in.
- **Three past-tense questions** — about what they actually did and spent,
  mom-test style: "When did this last happen to you? What did you do about
  it? What did that cost you — money, time, workaround?" Never "would you
  use…" — future-tense intent questions produce no reliable signal.
- **A kill criterion, stated before the test** — "if fewer than X of N people
  have this behavior, the assumption is dead and the fix is NARROW or
  RETHINK." Setting the threshold up front is what stops the result from
  being rationalized after.

Recruit where the behavior lives — the forum, community, or thread where
they paid or complained. N stays small: five is enough to hit a kill
criterion.

The bridge is the honest answer to the strongest critique of simulated
users — that a simulated customer can only tell you what you already believe.
True, and accepted: simulation *generates* the hypotheses; the bridge walks
them into reality. A probe without its bridge is a thought experiment that
stops at the interesting part.

## Report shape

Deliver in the user's language, in this order: verdict → persona matrix →
per-persona runs → ranked problems with fixes → risks in what you told me
(Step 0's labels, cashed in) → revised one-pager → what only real users can
prove, with the reality bridge. Deliver in-chat; write to a file only when
asked, at a path the user chooses.

**The verdict is three-valued, and never bare:**

- **BUILD** — build it as re-scoped, *to validation, not to launch*: the
  next step is the reality bridge, not the roadmap.
- **NARROW** — the idea survives only for a subset of the claimed audience;
  name the subset and what gets cut.
- **RETHINK** — the probe broke something load-bearing (no discovery path,
  no real job, a fatal misread of the core); name it before any building.

Whatever the value, it carries a debt line: *"this verdict stands on N
unverified assumptions, M of them fatal — listed in the bridge."* A verdict
without its debt line reads like market evidence, which it never is.

**End with a rerun invitation:** name the one or two changes that would most
alter the outcome — "re-position as X and the misreads likely vanish",
"narrow to Y and the discovery problem dissolves" — and offer to rerun the
tunnel on the revised idea. A wind tunnel is for iterating, not for filing.

**When writing to a file, deliver three layers:** a one-page answer first
(verdict with debt line, top problems, the revised one-pager), the ranked
detail second, per-persona runs as an appendix. Nobody should read fifteen
pages to find the verdict.

## Pre-delivery gate

All boxes, or the report does not ship — in a quick probe each box compresses
to a line, but none is skipped (checked internally, never printed as a
checklist in the report):

- [ ] Matrix spans all five diversity slots; author-lookalikes hold ≤ 1 seat
- [ ] Pitch claims labeled hunch / observation / data (Step 0)
- [ ] Every first-glance misread recorded verbatim, before any explaining
- [ ] Every zero-friction run carries its three-fact burden of proof
- [ ] No homogeneity: no two personas stall or pass in the same words
- [ ] Station-3 decisions anchored in past behavior; "would try" downweighted
- [ ] Verdict is BUILD / NARROW / RETHINK and carries its debt line
- [ ] The 1–2 most fatal problems carry a reality bridge with kill criterion
- [ ] "What only real users can prove" is non-empty
- [ ] Nothing in the report claims to be market evidence

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
