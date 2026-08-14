# thinking-partner

Routes ambiguous requests to the question actually being decided — and refuses to fake convergence when the evidence isn't there.

## What it does

- Detects when the real deliverable is judgment rather than output, and switches into structured thinking without being asked.
- Separates what you said, what the evidence shows, what it infers, and what is still unknown — so you can disagree with a specific claim instead of a vibe.
- Keeps two to four live interpretations with the test that would distinguish them, instead of forcing one answer to feel finished.
- When convergence is earned, gives one recommendation, its main trade-off, and why the alternatives lost; when it isn't, names the next learning step.
- Handles dictated, messy, mixed-language input — corrections and decisions arriving in one stream.

## When it fires

- "Help me think this through."
- "I'm torn between X and Y."
- "Am I even asking the right question?"
- "What am I missing here?"
- 「你帮我想想」
- 「我在纠结要不要…」

No magic words — it triggers on meaning. It stays out of the way for research, building, review, and status work, and applies only to the unresolved fork in mixed requests.

## Install

```
npx skills add m1nga/skills@thinking-partner
```

## Example

> **User:** I'm torn between rewriting the sync module or patching it again. Help me think this through.

The skill separates the open decision (rewrite vs. patch) from the stated constraints (no downtime, solo maintainer), names what makes each path plausible, and identifies the distinguishing test — "how often has a patch here caused a regression in the last three months?" — before recommending. If that record isn't available, the verdict is "not yet decidable, go get that one number," not a side picked to sound decisive.

## Works well with

- **grilling** — this skill frames the decision; grilling interrogates the resulting build plan step-by-step.
- **prompt-distill** — once thinking converges, distill the outcome into a reusable prompt.

## Design notes

Written by a solo builder after real incidents where an assistant "found" a deeper need that wasn't there and the work went confidently sideways. That produced the two hard rules: accurate surface understanding before depth (an eloquent sentence is not evidence of an underlying need), and convergence must be earned (a recommendation without a distinguishing test is a guess in a suit).

Perspectives are selected, not enumerated — a viewpoint only enters when its disagreement would change the verdict, and the skill must say what that viewpoint has no authority to decide. Low-risk reversible defaults are decided by the agent; only identity, values, irreversible commitments, and material external consequences go back to the user. The skill deliberately does not stop work: once the fork is resolved, it continues into whatever was already authorized.

## Field-tested

Probed 6 scenarios across 5 personas · 4 fired correctly · 2 correctly stayed quiet.

> **"这个项目我现在有两个方向嘛……呃不对,是先把底座锁死再切,你帮我想想,我有点纠结"** → Fired. Untangled the dictated self-correction (later wording overrides earlier), kept both paths alive, and named the one test that would settle them — no fake convergence.

> **"帮我想想办法把这个 CSV 转成 JSON"** → Stayed quiet. "想想" alone isn't a thinking request when the deliverable is a file — the execution exclusion held, and even on a misfire the body routes straight to "build it, no thinking prelude."

> **"方案我大概想好了,帮我想想还有没有漏洞,然后我们开工"** → Deferred to grilling. This skill frames the decision; interrogating a committed build plan is explicitly someone else's seat.

Probe method: [scenario-probe](../scenario-probe/)
