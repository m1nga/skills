# Product Idea Stress Test — Find What Will Break Before You Build

**Wind-tunnel the idea before you build it — simulated by the users who are
least like you.**

## The problem it actually solves

Every idea gets tested before launch by exactly one user: its author. The
author discovers it instantly (they made it), reads the pitch correctly (they
wrote it), and is maximally motivated (it's theirs). All three advantages
vanish on contact with a real stranger — usually after the building is done and
the fixes are expensive. This skill moves that collision forward, to the moment
the idea is still one paragraph and changes cost nothing.

## What it does

- Derives 4–7 named personas from the audience the idea *claims* to serve,
  with forced diversity slots: age spread, income tiers, tech fluency, usage
  context and device, motivation strength. At least half the cast must be
  people the author would find unfamiliar.
- Runs each persona through an honest first-contact simulation: how they
  discover it → what they think it is at first glance (misreads recorded
  verbatim, before any explaining) → whether they start → where they first get
  stuck → whether they come back. A run is allowed to end at "she never finds
  out it exists."
- Ranks every surfaced problem by breadth (how many personas hit it) times
  fatality (do they leave when they hit it), with consensus escalation: a
  problem two personas hit independently is promoted a tier.
- Ships a fix per problem, a revised one-pager — the stronger version of the
  idea, honestly re-scoped — and a three-valued verdict: BUILD (to
  validation) / NARROW / RETHINK, always with its unverified-assumption debt
  line attached.
- Ends, mandatorily, with "what only real users can prove", and attaches a
  reality bridge to the deadliest findings: who to recruit (by behavior, not
  demographics), three past-tense questions, and a kill criterion stated
  before the test.

## When it fires

- "Probe this idea before I build it"
- "New idea — don't build anything yet, just probe it."
- "Quick probe: a subscription box for left-handed kitchen tools."
- "Simulate some users and test this concept."
- 「先别建,帮我推演一下」
- 「帮我模拟用户测测这个想法」
- 「新想法:xxx。先别建,推演一下」

And when it doesn't: a SKILL.md or system prompt goes to scenario-probe; a
product you can already click through goes to product-experience-officer; "is
this technically feasible" is a research question, not a persona simulation.

## Install

```bash
npx skills add m1nga/idea-probe
```

## Example

> **You:** New idea: a flashcard app for learning wine pairings. Don't build —
> probe it first.
>
> **Claude** casts six personas — a 24-year-old sommelier student on a cracked
> phone, a 51-year-old restaurant owner who delegates anything with an app
> store, a 33-year-old gifting it to her partner, among others — and runs first
> contact. The restaurant owner misreads the name as a wine *inventory* tool
> and leaves in eight seconds; three of six never encounter a plausible
> discovery channel; the gift recipient opens it once. The report ranks
> "no discovery path for the majority of the claimed audience" above every
> in-app issue, ships a one-pager re-scoped to sommelier students, and closes
> with what the simulation cannot prove: that students will pay, and that
> week-two retention exists.

## Works well with

The three probe seats, in build order:

1. **idea-probe** — before anything is built: the idea itself, tested against
   simulated first contact.
2. **[scenario-probe](https://github.com/m1nga/scenario-probe)** — once
   instruction text exists: a SKILL.md, a system prompt, a standing rule,
   tested against persona × scenario trigger simulation.
3. **[product-experience-officer](https://github.com/m1nga/product-experience-officer)**
   — once the product runs: experienced as a zero-context stranger, reported
   as an expert.

Same honesty contract across all three: a report with zero findings means the
auditor sat in the author's chair.

Also pairs with [extend-first](https://github.com/m1nga/extend-first) — if
the idea that survives the probe is a *skill*, that gate checks the shelf for
overlap before you write it.

## Design notes

Two rules carry most of this skill's value:

- **Misreads are perishable evidence.** The moment the correct reading of an
  idea is stated, the confusion cannot be re-experienced — so every persona's
  first-glance interpretation is recorded verbatim *before* any explanation,
  and interpreted only afterward. A probe that explains first has already
  destroyed its best data.
- **Forced diversity slots exist because authors simulate themselves.** Left
  alone, an idea's author casts users who share their age, income, patience,
  and phone. The slots (age spread, income tiers, tech fluency, context and
  device, motivation strength) make that impossible — because the biggest
  blind spot is always the people who are not like you. The cast rule is
  explicit: the author's lookalikes hold at most one seat.

And one honesty rule that outranks both: the report must end with what only
real users can prove. A persona simulation that gets mistaken for market
validation is worse than no simulation — so the boundary ships inside every
report, not in a footnote here.

### Benchmarked

After first release, this skill was benchmarked against the closest prior art
on GitHub:
[cookiy-ai/user-research-skill](https://github.com/cookiy-ai/user-research-skill),
[RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills),
[zamesin/Next-Move-Theory](https://github.com/zamesin/Next-Move-Theory),
[machinesoul11/anti-sycophant](https://github.com/machinesoul11/anti-sycophant),
and [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).
None of them wind-tunnels an unbuilt idea with simulated personas — the seat
had no incumbent — but several of their disciplines were plainly better than
ours, so we took them:

- From **zamesin/Next-Move-Theory**: the three-valued verdict that is never
  bare (a GO is always "GO — to validation"), the unverified-assumption debt
  line, and the kill criterion stated *before* the test so the result can't
  be rationalized after.
- From **machinesoul11/anti-sycophant**: past expenditure as the filter at
  the start-or-not station — a persona with no history of spending money,
  time, or effort on the problem holds a fake job, and their "I'd try it" is
  weighted near zero.
- From **alirezarezvani/claude-skills** (named-persona-adversarial-review):
  the zero-finding burden of proof, consensus escalation, and the
  homogeneity check — its integrity question "all NOTE-level? Then I'm
  narrating one perspective in different voices" became this skill's
  recast-and-rerun rule.
- From **cookiy-ai/user-research-skill**: recruiting by behavior, never
  demographics ("switched tools in the last 6 months", not "ages 25–40") —
  the shape of the reality bridge's "who to find" — and the pre-delivery
  checklist gate.

One criticism we took seriously instead of borrowing around:
machinesoul11/anti-sycophant refuses simulated users flatly — "a simulated
customer can only tell you what you already believe." As a critique of
simulation *presented as validation*, that is simply correct. Our answer is
structural, not rhetorical: every report ends with "what only real users can
prove", and the deadliest findings now carry a reality bridge — behavioral
recruiting, past-tense questions, a pre-stated kill criterion — that walks
the hypotheses into the real world. Simulation generates; only reality
validates. Simulation, never validation.

## Field-tested

This skill has passed two wind tunnels. Before first release: 9 scenarios, 5 personas, 2 languages — 1 harmful false-fire caught (a bare 「这个想法怎么样?」 summoning a full persona matrix against a strategy decision) and removed from the trigger surface before any real session paid for it. After the v2 rewrite (Step 0 pitch-labeling, run sizing, the reality bridge, the pre-delivery gate): an 11-scenario regression — all 3 original trigger phrases re-fired, all boundary silences held, 0 trigger regressions. The tunnel's two remaining catches were documentation drift and one sizing/gate wording conflict — both fixed before this page went up.

> **Narrow audience, dictated (pass):** 「先别写代码…给退休护士的记药 app,模拟几个用户跑跑」— fired on the verbatim phrases, and the diversity slots bent *inside* the niche exactly as written: age within the band, tech comfort, motivation — the slots never disappeared.

> **Correct silence, still holding after v2:** a bare 「这个想法怎么样?」about a business pivot — the phrase this skill's own first tunnel evicted — stayed silent through the rewrite. Regression is the point: a rewrite that re-awakens an old false-fire has failed even if everything new works.

> **A boundary, ruled:** 「给我的想法做个调研」— research-my-idea with no simulation language — routes to product-5w, not here. The two descriptions arbitrate it without a coin flip: 调研 belongs to the definition seat; this skill answers to 模拟 / 测测 / 推演.

Probe method: [scenario-probe](https://github.com/m1nga/scenario-probe)
