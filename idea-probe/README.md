# idea-probe

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
  fatality (do they leave when they hit it).
- Ships a fix per problem and a revised one-pager — the stronger version of
  the idea, honestly re-scoped.
- Ends, mandatorily, with "what only real users can prove": the explicit
  boundary between this simulation and actual market evidence.

## When it fires

- "What do you think of this idea?"
- "New idea — don't build anything yet, just probe it."
- "Simulate some users and test this concept."
- 「这个想法怎么样?」
- 「帮我模拟用户测测这个想法」
- 「新想法:xxx。先别建,推演一下」

And when it doesn't: a SKILL.md or system prompt goes to scenario-probe; a
product you can already click through goes to product-experience-officer; "is
this technically feasible" is a research question, not a persona simulation.

## Install

```bash
npx skills add m1nga/skills@idea-probe
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

1. **[idea-probe](../idea-probe/)** — before anything is built: the idea
   itself, tested against simulated first contact.
2. **[scenario-probe](../scenario-probe/)** — once instruction text exists: a
   SKILL.md, a system prompt, a standing rule, tested against persona ×
   scenario trigger simulation.
3. **[product-experience-officer](../product-experience-officer/)** — once the
   product runs: experienced as a zero-context stranger, reported as an expert.

Same honesty contract across all three: a report with zero findings means the
auditor sat in the author's chair.

Also pairs with [extend-first](../extend-first/) — if the idea that survives
the probe is a *skill*, that gate checks the shelf for overlap before you
write it.

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

## Field-tested

Before release, this skill went through a 9-scenario wind tunnel — 5 personas, 2 languages, a stranger who installed nothing else, and boundary sentences fired point-blank at its three sibling skills. Score: 5 clean passes, 3 degraded-risk findings, 1 harmful false-fire — caught in simulation, fixed in the description before any real session paid for it. 3 correct silences.

> **Voice-note Chinese, no trigger phrase at all (pass):** "就是我早上想到一个东西啊,呃,给楼下咖啡店做个小程序让熟客提前点单,你帮我看看靠不靠谱,别急着写代码" — no verbatim keyword matched, and the probe still fired on semantics: an unbuilt idea plus an explicit don't-build-yet. The five-station simulation ran end to end, including a persona who honestly never discovers the product.

> **Correct silence:** "Here's my SKILL.md draft — what do you think?" — contains a phrase that once sat in this skill's own trigger list, yet the NOT-clause held: existing instruction text is scenario-probe's seat. The probe routed instead of firing.

> **The false-fire the tunnel caught:** a bare "这个想法怎么样?" about a business pivot — no audience, nothing to build — would have summoned a full persona matrix against a strategy decision: a confident, complete, wrong-instrument report. The casual-opinion phrases were removed from the trigger surface; a bare "what do you think" now gets a direct answer (or thinking-partner), and this skill fires only when a pre-build test is actually asked for.

Probe method: [scenario-probe](../scenario-probe/)
