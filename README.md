# ming-skills

**Agent skills for people who ship alone.** Twenty-one skills for Claude Code and
Codex, distilled from a solo builder's real workflow — including the rebuilds
that went wrong. Every skill is its own product: one directory, one page, one
install command.

```bash
npx skills add m1nga/skills@<skill-name>
```

Each skill was wind-tunnel tested before release: simulated against six user
personas (from "dictated 2 a.m. voice note" to "stranger who installed only this
one skill") across 140+ scenarios, hunting trigger misfires, sibling collisions,
and silent failures. The tool that does that testing is in the box
([scenario-probe](scenario-probe/)) — this repo is its first customer.

All skills answer in **your language** (English and Chinese trigger phrases
ship in every description), and every skill carries an `agents/openai.yaml`
interface for Codex.

---

## 🎯 Protect the flow

| Skill | One line |
|---|---|
| [side-quest](side-quest/) | Park a mid-flow thought in one line — a background agent works it, results land outside the chat, and a parked thought can never be silently lost |

## 🧠 Think before you build

| Skill | One line |
|---|---|
| [thinking-partner](thinking-partner/) | A judgment partner that keeps 2–4 live interpretations open and only converges when the evidence earns it |
| [grilling](grilling/) | A relentless one-question-at-a-time interview that ends in a locked, scoped plan — every question arrives with a recommended answer |
| [one-sentence](one-sentence/) | Ask about a concept, get one sentence a stranger could repeat tomorrow — 20 words is the budget, selection is the craft |

## 🔁 Close the loop

| Skill | One line |
|---|---|
| [conclude-rounds](conclude-rounds/) | Recap the last N rounds with done/claimed/proposed sorted honestly, plus up to five evidence-based workflow insights |
| [iteration-close](iteration-close/) | End an iteration the safe-but-ruthless way: distill decisions, delete superseded files (with your explicit yes), prove a cold reader could take over |
| [experience-pack](experience-pack/) | A two-layer memory: a dated project ledger, and a boundary test that decides which lessons may travel to other projects — experience inherits, decisions die |
| [diagnose-project-rebuild](diagnose-project-rebuild/) | For inherited, chaotic, or five-times-rebuilt projects: diagnose the limiting condition first — rebuild is one treatment, not the default |

## 📦 Build the product

| Skill | One line |
|---|---|
| [map-product-system](map-product-system/) | Turn a rough idea or a live codebase into an end-to-end system map with every claim labeled Known / Inferred / Proposed / Unknown |
| [loop-system-architect](loop-system-architect/) | Turn a repeated task into a closed control loop — persistent state, independent verification, recovery, and a lint that checks your contract |
| [product-experience-officer](product-experience-officer/) | Experiences your product as a zero-context stranger, then reports as an expert — confusion is captured before it evaporates |

## 📏 Test and evaluate

| Skill | One line |
|---|---|
| [idea-probe](idea-probe/) | Wind-tunnel an unbuilt idea: simulate first contact across a forced-diversity persona matrix, rank the problems, ship a stronger one-pager |
| [scenario-probe](scenario-probe/) | Wind-tunnel any skill, prompt, or standing rule: persona × scenario simulation that finds misfires before real sessions pay for them |
| [extend-first](extend-first/) | Before building a new skill, a librarian's gate checks what you already own — verdict: extend, compose, or genuinely build new |
| [write-judge-prompt](write-judge-prompt/) | Design a binary LLM judge for one failure mode — after checking a code-based check couldn't do it cheaper |
| [validate-evaluator](validate-evaluator/) | Calibrate that judge against human labels (TPR/TNR, bias correction) — and never let the model grade its own homework |

## ✍️ Write like yourself

| Skill | One line |
|---|---|
| [voice-extractor](voice-extractor/) | Measures your writing voice into a numeric fingerprint (function words, burstiness, punctuation rates) and gates drafts against the bands |
| [prompt-distill](prompt-distill/) | One-shot prompt cleanup that preserves your intent instead of redesigning your request — small edits over grand rewrites |
| [prompt-craft](prompt-craft/) | A marketing prompt workshop: turns content ideas into structured prompts enriched with YOUR brand context (bring your own `user-context.md`) |

## ☕ Everyday

| Skill | One line |
|---|---|
| [desktop-package](desktop-package/) | Packages a work session into one reviewable desktop folder with a start-here file — verified with five integrity checks before it says "done" |
| [coffee-brewing](coffee-brewing/) | Espresso and pour-over dial-in that trusts shot numbers over taste adjectives, remembers every bean you've dialed, and adapts to your gear |

---

## Design principles

1. **Triggers are the product.** A skill that fires on the wrong request — or
   sleeps through your phrasing — fails before its body loads. Every description
   here carries natural-language trigger examples, explicit exclusions, and
   deferral clauses to sibling skills.
2. **No silent failures.** Missing data files degrade loudly, deletions require
   an explicit yes, and no skill invents numbers to satisfy an output format.
3. **Opinionated bodies, honest claims.** The methodology in each skill comes
   from real incidents (a five-rebuild contamination saga taught most of it).
   Where a skill's advice is a judgment call, it says so.
4. **Your data stays outside the package.** Skills write user data to your home
   directory, never into their own folder — updates should never eat your history.

## License

MIT. Third-party skills this collection pairs well with (a humanizer, headline
libraries, marketing psychology references) are linked from individual skill
pages and installed from their original authors — not vendored here.
