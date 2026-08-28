---
name: product-5w
description: >-
  Interrogate a product's definition with five questions, at any stage — idea, mid-build, or
  shipped — asking past behavior, never future opinion. WHO (by behavior not demographics; who
  it's NOT for; user vs buyer; first 10 users), WHAT job it does (and deliberately doesn't;
  do-nothing as first competitor), WHEN as context and trigger (struggling moment, frequency,
  tense-matched), HOW it gets used AND found (distribution is half of HOW; ultimate test: an
  offer), WHY it matters / why now / why you. Answers tagged verified/inferred/assumed; each W
  splits desk reasoning vs field proof; output: DEFINED/NARROW/REDEFINE verdict + validation
  debt, cheapest-next-verification list, named contradictions. Use for "run a 5W on
  this", "who is my product actually for", "survey my product before launch", 给我的产品做个调研 /
  这个产品的 who what why 帮我过一遍 / 上线前做个基本盘调研 / 产品定义审计. NOT persona simulation (idea-probe), NOT
  architecture mapping (map-product-system), NOT hands-on audit
  (product-experience-officer), NOT technical feasibility.
---

# Product 5W（产品五问）

A product that cannot answer five basic questions — who, what, when, how, why —
is not underdocumented; it is undefined. This skill is the definition layer: it
asks the questions a stranger with money would ask, refuses vague answers, and
delivers a 5W brief where every claim wears a tag saying how it is known.

The object is **a product or project at any stage** — a paragraph of idea, a
half-built repo, a shipped app. The stage does not change the questions; it
changes what "verified" can mean. Establish the stage first, because it selects
the mode:

- **Before or during build — definition interrogation.** The brief is the
  contract the build answers to, and the natural input for idea-probe's persona
  simulation afterwards.
- **After build — definition audit.** Answer the five questions from what the
  product *is today*, then compare against the founding answers (ask for them if
  they exist); if none exist, audit today's product alone and record the missing
  founding record as a finding. Divergence has exactly two readings — the product drifted from a
  right definition, or faithfully executed a wrong one — and the brief must say
  which it believes, with evidence.

## Before the questions: what decision is this for?（先问决策）

Two gates, before any of the five questions runs:

- **Decision mapping.** What specific decision will this brief change — build
  or not, narrow to which audience, price at what, launch or wait? If no
  decision would move with the answers, say so and stop: research that
  informs nothing is a sideshow, however rigorous it looks. (Studying a
  market to decide what to build is itself a decision — name it.)
- **Outcome verb rule.** State the brief's objective with a verb whose
  completion is decidable — *describe, evaluate, identify, compare*. Reject
  "understand" and "explore": open-ended verbs never finish. "Understand my
  users" becomes "identify which claimed WHO has actually paid to solve
  this."

## Sourcing rule

Drain what the user provided first — pitch, README, code, metrics, chat
history — and draft answers from that. Then ask the user targeted questions
ONLY where the answer could change the verdict. If the user cannot answer,
that is a finding: write **unknown** and move on. Never fill a gap from model
memory — a fact recalled from training data is at best *inferred*, never
*verified*. And never invent market numbers: no TAM, market size, or
conversion rate without a source. A professional-looking fake number is the
worst artifact this skill can produce; "unknown" is the honest one.

Cold start with zero material: ask by W, in rounds of at most three
questions — never pour the full sub-probe set at once.

The order stands — drain first, then ask — but the author's answers get no
diplomatic immunity: a future-tense answer ("users would love this") or an
adjective answer ("it's really fast") earns the behavioral counter-question
before it earns a tag — *has* anyone? when, exactly? fast as in — how many
minutes? An author's forecast about their own users is a hunch wearing a
suit.

## The meta-rule（元规则）

Every sub-probe below asks about **past behavior, never future opinion**.
The two sharpest formulations in the field, quoted at their sources:

> "Study Jobs by past expenditure of money, time, and energy — never by
> future intent." — zamesin/Next-Move-Theory

> "Avoid 'would you use an app that…' — that question has never once
> produced reliable signal." — machinesoul11/anti-sycophant

People are poor forecasters of their own behavior and generous narrators of
their own intentions; what they *did* — paid, switched, spent an evening on a
workaround — is the only answer that can carry a *verified* tag. The rule
governs both directions: the questions this skill asks the author now, and
the field questions the brief hands back for verification later.

## The five questions（五问）

Each question carries sub-probes whose job is to make the comfortable vague
answer impossible.

### WHO — 确切给谁

- Exactly who — and explicitly who it is **NOT** for. A WHO without an exclusion
  is a wish, not a definition; "for everyone" is not an answer, it is an
  alarm.
- Define WHO by **behavior, not demographics**: "people who switched PM tools
  in the last six months" is a WHO; "ages 25–40" finds people who resemble a
  user without ever having been one.
- The sharpest qualifying question, for the field list: *"When did you last
  pay for X? What did you pay? What did you do as a result?"* No past
  payment, no verified WHO.
- Is the person who *uses* it the person who *pays or decides*? If not, both get
  an answer, because they need different WHYs.
- In B2B, the unit of WHO is the decision-maker — and behind every business
  job sits a personal one: not getting blamed, getting promoted, winning
  recognition. The brief names both layers or the WHY will later ring false.
- Who, concretely, are the first 10 users? Describable individuals — "my three
  ex-colleagues who still do this in spreadsheets" — not a demographic.
  "Developers" is not an answer; it is the absence of one.

### WHAT — 替用户完成什么

- What job does the user hire it to complete — and what does it *deliberately
  not do*? A WHAT without a refusal list will grow until nobody can say what it
  is.
- Open field questions with the task, not the product: *"tell me which tasks
  you solve with it"*, in the user's everyday words — the product's own
  vocabulary contaminates the answer.
- A generalized answer is not data. Pull it to the last concrete instance:
  "the last specific time — walk me through it, step by step."
- Adjectives get forced into numbers: "fast" is a mood; "it took 4 minutes"
  is a fact you can design, price, and measure against.
- The honest competitor set includes the boring options — a free tool, a
  spreadsheet, doing nothing. **Do-nothing is the first row of every
  competitor list**, because it usually wins.
- One sentence that defines it. If one-sentence is installed, use its
  discipline (one load-bearing idea, genus-differentia, every word earning its
  place); if not, still write one honest sentence — and if the product cannot
  be carried in one sentence, record that as a finding about the product.

### WHEN — 情境与触发

WHEN here means **context and trigger together** — where, on what, and around
whom the moment happens lives inside this question. There is deliberately no
separate WHERE: a forced sixth question produces filler, and context divorced
from its trigger describes a place, not a moment.

- The trigger, asked as an event: *"what specific event or struggling moment
  made you look for a solution?"* — the causation behind "today's the day I
  do something different." Name the event, not the mood.
- The context, asked separately from the trigger: where were they, on what
  device, under whose eyes, in the middle of what? A trigger that only fires
  in contexts the product can't reach is a definition problem, not a
  marketing one.
- How often does that moment occur? Daily-habit and yearly-emergency are
  different products wearing the same feature list.
- **Match the tense to the frequency.** A one-off job (rent an apartment,
  hire a lawyer) is asked in the past tense, anchored to the last concrete
  instance. A high-frequency job (order food, file a ticket) is asked in the
  habitual tense — "usually" — plus how often. One idiosyncratic instance
  misleads; one vague generality misleads worse.
- If the claimed WHO is happily locked into a good-enough habit at this
  moment, that is not a market this product can win, however large it looks —
  say so in the brief.
- Field-note for the verification list: recalled timing is systematically
  wrong. Temporal claims verify by diary or logs, not by asking people to
  remember; a remembered "when" is *inferred* at best.

### HOW — 怎么被用 + 怎么被找到

- How is it used: first contact → first value → habit. Where in that path does
  the effort sit, and does it match WHO's patience?
- The incumbent, with teeth: *"how are you currently solving this, and what
  specifically annoys you about that approach?"* The annoyance is the wedge;
  no annoyance, no switch.
- The graveyard: *"what have you already tried and abandoned?"* Abandonment
  is past expenditure — stronger evidence than any amount of adoption talk,
  and it maps the failures this product must not repeat.
- The steps before and after must be anchored to the higher goal —
  unanchored, "what did you do before it?" invites "I had breakfast". Ask
  through the outcome: "before it, how did you get {the outcome} done?"
- The ultimate HOW test is a sale. The usage path ends at an offer —
  pre-order, deposit, invoice before the product exists — because
  willing-to-pay talk that never meets an offer stays *assumed* forever.
  For unpriced products the offer is any costly commitment — a deposit, a
  booked hour, a signed-up queue.
- How is it *found*? Distribution is the other half of HOW, and the half most
  authors leave blank. Name the channel by which WHO plausibly encounters it;
  if no channel exists, the honest HOW answer is "it isn't", and that outranks
  everything downstream.

### WHY — 为什么重要

- Why does it matter *to the user* — stated as an outcome in their life, not a
  feature in the product.
- Climb the ladder: *"why? in order to do what?"* — at least one level above
  the stated outcome. The product competes at the level of the goal it
  serves, not the feature it ships.
- The do-nothing baseline: *"what would happen if you did nothing and just
  continued as today?"* If the honest answer is "not much", WHY has no floor
  and every other answer is decoration.
- Quantify the stakes: does failing cost time, money, or status — and roughly
  how much of which? An unquantified pain is a story; a quantified one is a
  price point.
- The sharpest single field question: *"have you ever paid to solve this, or
  looked for something to pay for?"*
- **Boundary warning:** unconscious drivers — status, identity, safety — do
  not interview. Asking "why" there returns a convincing, functional, false
  story. Write the hypothesis, tag it *assumed*, and note that it verifies
  through sales, A/B, or messaging tests — never through more direct
  questioning.
- Why now — what changed (technology, behavior, regulation, price) that makes
  this buildable or wanted today when it wasn't before?
- Why you — what does the author have that a competent stranger doesn't?
  "Nothing yet" is an acceptable, taggable answer; an invented moat is not.

## The honesty ledger（诚实台账）

Every answer — every sub-answer — carries exactly one tag:

| Tag | Meaning | Requirement |
|---|---|---|
| **verified** | Evidence exists | Cite it: an interview, a metric, a payment, a log |
| **inferred** | Derived from evidence | Show the chain from evidence to claim |
| **assumed** | The author believes it | Say so plainly — no dressing it as analysis |

Where nothing is known, write **unknown** — it is a value, not a failure.

Cross-skill note: these tags correspond one-to-one to map-product-system's
ledger (if installed) — verified ≈ Known, inferred ≈ Inferred, assumed ≈
Proposed, unknown ≈ Unknown — so a 5W brief and a system map read side by
side without translation.

The ledger is the brief's instrument panel: report assumed+unknown density per
question and overall. Assumed density IS risk density — a brief that is 80%
assumed is not a bad brief, it is an accurate map of an unvalidated product,
and saying so is the job.

For every question that is entirely assumed/unknown, generate the **cheapest
next verification action** — cheapest, not most rigorous: ask 5 people from the
claimed WHO, read one week of existing data, run one fake-door test, watch one
person attempt the WHEN moment. Each action names which tag it would flip.

## Desk vs field（桌面与田野）

Each of the five answers closes with two lines:

- **Desk says** — the best answer that reasoning over the provided material
  can produce.
- **Only the field can prove** — the part of that answer that stays
  hypothesis until a real user, a real payment, or a real log confirms it.
  This line may not be empty for any answer tagged *assumed*.

The split exists because desk work speeds up the thinking, not the proving —
every untagged-as-verified claim is a hypothesis until checked in the field,
and the brief's job is to make that boundary impossible to miss.

## Consistency check（一致性核对）

The five answers must be able to co-exist. Cross-examine every pair and name
contradictions explicitly, with both ends quoted: WHO says time-starved
professionals, HOW demands a 20-minute onboarding. WHEN says rare emergency,
WHY claims daily-habit value. WHO's buyer is a manager, HOW's channel only
reaches interns. A brief whose answers contradict is describing two products —
or none — and the contradiction list is often worth more than the answers.

## The brief（简报）

Deliver in the user's language, in this order: verdict → the five answers
with tags, sources, and their desk/field split → ledger census
(assumed/unknown density per question) → contradictions →
cheapest-verification list → handoff (pre-build: this brief is idea-probe's
input; post-build: founding-vs-current divergence and its reading). Deliver
in-chat; write to a file only when asked, at a path the user chooses.

**The verdict is three-valued, and never bare:**

- **DEFINED** — the five answers cohere; go build, or go validate the
  assumed ones. Name the single weakest answer even here.
- **NARROW** — the definition holds only for a subset of the claimed WHO or
  WHAT; name the subset that survives and what falls away.
- **REDEFINE** — the answers contradict or the load-bearing ones are absent;
  the set describes two products, or none. Name what must be re-answered
  first.

Whatever the value, it carries the validation debt line: *"this verdict
stands on N assumed or unknown answers, M of them load-bearing"* — and the
cheapest-verification list is where that debt gets paid. A verdict without
its debt line reads like market evidence, which this brief never is.

## Boundaries

- **A research brief, never validation.** Tagged answers are hypotheses with
  provenance. The brief must never read as market evidence, and the verified
  tag applies only to claims with citable sources.
- This skill defines; it does not simulate, map, or operate. The product line
  in build order: **product-5w** (definition) → **idea-probe** (persona
  simulation of first contact) → **map-product-system** (architecture) →
  **product-experience-officer** (hands-on experience audit). Hand off by
  name when the user's request has crossed the line; when the sibling is not
  installed, say what that seat would cover instead of doing its job badly here.
- Technical feasibility ("can this be built") is research, not one of the five
  questions — flag it as out of scope when it comes up.
- If every answer comes back verified and consistent, say so briefly and stop —
  do not manufacture doubt to look rigorous. The rarity of that outcome is its
  own signal.
