# experience-pack

Your project's lessons survive a rebuild. Its decisions don't — and this skill knows the difference.

## What it does

Keeps a dated `EXPERIENCE.md` ledger in each project (what happened, what we
did, what it cost — written the same day, as a gate on "done", not a diary).
Then, on request, runs each entry through a five-part boundary test —
substitution, mechanism-vs-choice, re-derivation, sunk-cost, verifiability —
to decide what is portable experience and what is a dead decision. Portable
lessons travel to other projects with provenance tags; everything else stays
put or dies. It also ships a reference pack of pre-distilled lessons from a
project that was rebuilt five times because old context kept leaking back in.

## When it fires

- "Let's do a post-mortem on this project."
- "Write down what we learned before we forget it."
- "Record this incident so we don't repeat it."
- "What lessons from the last project apply here?"
- 「把这次的教训沉淀下来」
- 「给这个项目建个经验文件」

It does not fire on "review this conversation" (that's `conclude-rounds`) and
it refuses to become a decision register — decisions live in the project's own
truth files.

## Install

```
npx skills add m1nga/skills@experience-pack
```

## Example

> **User:** that migration ate the whole afternoon because staging pointed at
> the old bucket. write it down.
>
> **Agent:** Confirms the project root (won't drop a ledger on your Desktop),
> appends a dated entry — what happened, the response, the cost (4 hours),
> marked `Portable? not yet` — and reminds you the fix isn't "done" until the
> entry exists. Weeks later, "distill the ledger" turns it into one noun-free
> line: *"Verify every environment's external endpoints against the current
> truth file before a migration; stale endpoints fail silently."* The bucket
> name dies; the lesson travels.

## Works well with

- [`diagnose-project-rebuild`](../diagnose-project-rebuild/) — when a project
  direction is replaced, that skill takes exactly one input from history:
  this skill's portable layer.
- `iteration-close` — owns the closure ritual; runs this skill's distillation
  pass inside it.
- `conclude-rounds` — conversation-level review; this skill is project-level.

## Design notes

The two-layer split exists because of a specific, repeated failure: a solo
builder rebuilt the same product five times, and every restart the abandoned
strategy leaked back in — through summaries, archive maps, and "lessons" with
prospect lists still attached. The fix that finally held was a hard rule,
**experience inherits, decisions die**, enforced by a written test instead of
judgment in the moment. Ambiguous items die by default (the ledger keeps them
recoverable), because every optimistic "this one's probably fine" was how
contamination got back in. The binding rules — recording as a gate on done,
declared bootstrap imports, a mandatory backup channel for gitignored ledgers
— each trace to an incident an adopter project actually hit.

## Field-tested

Probed 8 scenarios across 5 personas · 6 fired correctly · 1 correctly stayed quiet · 1 logged as a follow-up note.

> **"复盘一下刚才这几轮对话" ("recap the last few rounds of this chat")** → stays quiet. Conversation recaps belong to `conclude-rounds`; this skill only claims post-mortems that outlive the conversation.

> **"That refactor ate two days — write down what we learned before we forget."** → fires. Appends a dated ledger entry — what happened, the response, the cost — with a `Portable?` flag for the next distillation pass.

> **"记录经验" (dictated from the Desktop, no project open)** → fires, then refuses to drop an `EXPERIENCE.md` on your Desktop — it asks which project the lesson belongs to, and if no project can be established it hands you the formatted entry instead of silently losing it.

Probe method: [scenario-probe](../scenario-probe/)
