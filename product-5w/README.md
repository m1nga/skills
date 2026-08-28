# product-5w

**Five questions your product must answer — who, what, when, how, why — with
every answer tagged by how you actually know it.**

## The problem it actually solves

Ask a builder who their product is for and you get "developers." Ask what it
does and you get a feature list. Ask how users will find it and the room goes
quiet. These aren't research failures — they're definition failures, and they
are invisible to the author because the author's head autocompletes every
vague answer. This skill runs the interrogation a stranger with money would
run, and refuses the comfortable answers: not "developers" but the first 10
users by name; not the feature list but the job it completes and the jobs it
refuses; not "we'll do marketing" but the actual channel by which the actual
WHO plausibly encounters it.

It works at any stage. Before building, the brief is the contract the build
answers to. After shipping, it's an audit: do the founding answers still hold,
or did the product drift — or faithfully execute a wrong definition?

## What it does

- Asks the five questions with anti-vagueness sub-probes: WHO (defined by
  behavior, not demographics; who it's NOT for; user vs. buyer; the first 10
  users concretely), WHAT (the job and the deliberate refusals; adjectives
  forced into numbers; do-nothing as the first competitor), WHEN as context
  and trigger (the struggling moment, its frequency, tense matched to
  frequency), HOW (first contact to habit; what was tried and abandoned; the
  offer as the ultimate test; plus distribution — the half of HOW most
  authors leave blank), WHY (the ladder of "in order to do what", the
  do-nothing baseline, quantified stakes / why now / why you).
- Obeys one meta-rule throughout: every question asks about past behavior,
  never future opinion — including the author's own answers, which get the
  behavioral counter-question when they arrive in the future tense.
- Tags every answer **verified** (evidence, cited) / **inferred** (chain shown)
  / **assumed** (author's belief, said plainly) — and reports assumed density
  per question, because assumed density is risk density.
- Writes **unknown** where nothing is known. Never invents a market number: no
  TAM, no conversion rate, no "industry reports suggest" without a source.
- Turns all-assumed questions into a cheapest-next-verification list: ask 5
  people, read one week of data, one fake-door test — each action named with
  the tag it would flip.
- Cross-examines the five answers and names contradictions with both ends
  quoted: WHO says time-starved professionals, HOW demands 20-minute
  onboarding.
- Splits every answer into "desk says" vs "only the field can prove", and
  closes with a three-valued verdict — DEFINED / NARROW / REDEFINE — that is
  never bare: it always carries its validation debt line ("this verdict
  stands on N assumed answers, M load-bearing").

## When it fires

- "Run a 5W on this."
- "Who is this actually for?"
- "Survey my product before launch — just the basics."
- 「给我的产品做个调研」
- 「这个产品的 who what why 帮我过一遍」
- 「上线前帮我做个基本盘调研」

And when it doesn't: simulating users' first contact is
[idea-probe](https://github.com/m1nga/idea-probe)'s seat; mapping architecture
is [map-product-system](https://github.com/m1nga/map-product-system)'s;
actually operating the product as a stranger is
[product-experience-officer](https://github.com/m1nga/product-experience-officer)'s;
"can this be built" is technical research, not one of the five questions.

## Install

```bash
npx skills add m1nga/product-5w
```

## Example

> **You:** 上线前帮我做个基本盘调研 — it's a CLI that turns meeting recordings
> into task lists.
>
> **Claude** drains the README and pitch, then asks only the questions that
> change the verdict. The brief comes back: WHO is tagged assumed ("remote
> engineering managers" — zero interviews); WHEN is the strongest answer
> (verified: the author's own Monday ritual, weekly); HOW's distribution half
> is **unknown** — no named channel reaches a single manager. One contradiction
> is called out: WHO says managers who won't install dev tools, HOW requires a
> terminal. The verdict: the product is defined enough to build but not to
> launch, and the cheapest next action is five interviews from the claimed
> WHO — which would flip three assumed tags at once.

## Works well with

The product line, in build order:

1. **product-5w** — definition: can the product answer who/what/when/how/why?
2. [idea-probe](https://github.com/m1nga/idea-probe) — simulation: the 5W
   brief is its natural input; personas cast from a tagged WHO are honest
   personas.
3. [map-product-system](https://github.com/m1nga/map-product-system) —
   architecture: how the defined product hangs together end to end.
4. [product-experience-officer](https://github.com/m1nga/product-experience-officer)
   — experience: the built product, walked by a zero-context stranger.

Also pairs with [one-sentence](https://github.com/m1nga/one-sentence) — WHAT's
one-line definition borrows its compression discipline when installed.

## Design notes

- **The tags are the product.** Anyone can list five questions; the value is
  that every answer declares its provenance. A 5W brief that is 80% assumed is
  not a failed brief — it is an accurate map of an unvalidated product, which
  is exactly what its author needs to see. The skill's hardest rule follows
  from this: no invented market numbers, ever. A professional-looking fake TAM
  is worse than "unknown" because it ends the search that "unknown" starts.
- **Distribution lives inside HOW.** Most 5W-style frameworks treat "how" as
  usage mechanics. Here HOW is split — how it's used *and* how it's found —
  because an unfindable product's real HOW answer is "it isn't", and that
  answer outranks everything downstream of it.
- **The consistency check exists because answers lie in pairs.** Each answer
  can be individually plausible while the set describes no coherent product.
  Cross-examining pairs (WHO×HOW, WHEN×WHY, buyer×channel) catches what
  reviewing answers one at a time cannot.

### Benchmarked

This skill's second pass was built against the closest prior art on GitHub:
[cookiy-ai/user-research-skill](https://github.com/cookiy-ai/user-research-skill),
[RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills),
[zamesin/Next-Move-Theory](https://github.com/zamesin/Next-Move-Theory),
[machinesoul11/anti-sycophant](https://github.com/machinesoul11/anti-sycophant),
and [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).
The five-question frame and the provenance tags are this skill's own; the
field-grade phrasings inside the sub-probes are openly taken from people who
tested them on real users:

- **The meta-rule** is the ecosystem's strongest consensus, quoted at its
  sources: "Study Jobs by past expenditure of money, time, and energy — never
  by future intent" (zamesin/Next-Move-Theory); "Avoid 'would you use an app
  that…' — that question has never once produced reliable signal"
  (machinesoul11/anti-sycophant).
- **Decision mapping and the outcome verb rule** come from
  cookiy-ai/user-research-skill, as does behavioral recruiting ("switched
  project management tools in the last 6 months", not "ages 25–40").
- **The struggling-moment question and the do-nothing baseline** come from
  RefoundAI/lenny-skills — Bob Moesta's "today's the day" causation, "what
  would happen if you did nothing?", and the pre-product invoice test that
  became HOW's offer probe.
- **The tense discipline** (past tense for one-off jobs, habitual for
  frequent ones), the adjective-to-number push ("fast" → "it took 4
  minutes"), the higher-goal anchoring warning (unanchored "what did you do
  before it?" invites "I had breakfast"), and the unconscious-motive boundary
  (direct "why" returns "a convincing, functional, false story") all come
  from zamesin/Next-Move-Theory — as does the caveat behind the desk/field
  split: "this speeds up the thinking, not the proving."
- **The stakes quantifier and WHY's sharpest question** ("have you ever paid
  to solve this, or looked for something to pay for?") come from
  machinesoul11/anti-sycophant.

What was *not* taken: simulated users (idea-probe's seat, with its own
firewall), market sizing (no invented numbers is this skill's hardest rule),
and interview logistics (recruiting screeners and session scripts belong to a
research tool, not a definition brief).

## Field-tested

Before release, this skill went through a 13-scenario wind tunnel — 6 personas, 2 languages, a bare fresh install, a host crowded with a product-management plugin, and boundary sentences fired point-blank at its three sibling skills. Score: 8 clean passes, 4 degraded-risk findings, 1 harmful false-fire — caught in simulation, fixed in the description before any real session paid for it. 3 correct silences.

> **The false-fire the tunnel caught:** a user pastes a *competitor's* landing page and asks, in passing, "who is this actually for?" The old trigger phrase matched verbatim — and would have launched a five-question interrogation about a product the user doesn't own, opening with "when did you last pay for this?" aimed at someone who can't answer. The phrase now reads "who is **my product** actually for": the audit fires on your product, and a casual question about someone else's gets a casual answer.

> **The meta-rule under fire (pass):** mid-interrogation, the author answers "users will love it because it's way faster." The body doesn't just forbid accepting this — it scripts the counter-questions verbatim: *has* anyone? when, exactly? faster as in — how many minutes? paid for it, ever? The claim entered the brief tagged **assumed**, with the cheapest test that would flip it.

> **Correct silence:** 「帮我模拟几个用户测测我的产品」 — product-adjacent, research-flavored, and exactly one word away from this skill's own Chinese trigger. The NOT-clause held: simulating users is idea-probe's seat, and the skill routed instead of firing.

Probe method: [scenario-probe](https://github.com/m1nga/scenario-probe)
