# Skill Reuse Checker — Find What to Reuse Before Building a Duplicate

Before you build another agent skill, check the skills you already own and get
one evidence-based verdict: **EXTEND**, **COMPOSE**, or **BUILD NEW**.

## Quick answers

- **What problem does it solve?** It exposes forgotten overlap before duplicate
  agent skills are built with competing trigger surfaces.
- **What does it return?** Exactly one short verdict: extend one existing skill,
  compose two existing skills, or build a genuinely separate skill.
- **How does it compare candidates?** By the problem solved, input/output shape,
  and judgment-versus-execution nature — never by names or keyword similarity.
- **Does it create or edit skills?** No. It inventories and recommends; the
  actual authoring remains a separate, user-controlled step.
- **Can the check be overridden?** Yes. “Build it anyway” ends the gate in the
  same turn without relitigating the decision.

## The problem it actually solves

A skill you wrote and used twice is, six months later, indistinguishable from a
skill you never wrote. Libraries grow past what their owners remember, so the
same problem quietly gets solved twice — or a near-duplicate gets built with a
slightly different trigger surface, and now two skills raise their hand for the
same request. This gate runs at the moment of "make me a new skill for X": it
inventories what already exists, compares by what each skill *does* rather than
what it is called, and hands back a one-screen verdict.

## What it does

- Inventories installed skills and your skill directories at the description
  level — bodies are opened only for the nearest 1–3 candidates.
- Compares by core function on three axes: the problem solved, the input/output
  shape, and judgment-vs-execution. Name and keyword similarity is banned as
  evidence in both directions.
- Returns exactly one of three calls:
  - **EXTEND** — which skill, which section, what change.
  - **COMPOSE** — which two existing skills together, with the combined usage.
  - **BUILD NEW** — overlap ruled out, plus a drafted description boundary
    clause against the nearest neighbor, so the *next* collision is prevented
    too.
- Quotes the compared descriptions verbatim, so you can check the evidence
  without opening anything.
- Steps aside instantly when overridden: "build it anyway" ends the check, no
  relitigating.

## When it fires

- "Make me a skill that turns my meeting notes into action items."
- "I want a new skill for X."
- "Build me an agent that reviews my PRs for style."
- 「做一个 skill,帮我整理会议记录」
- 「帮我建个 agent 做数据清洗」

And when it doesn't: requests to *use* an existing skill just get routed;
product or feature ideas that aren't skills go to idea-probe; and "直接新建别查了" /
"skip the check" is respected silently — the inventory doesn't run behind your
back.

## Install

```bash
npx skills add m1nga/extend-first
```

## Example

> **You:** Make me a skill that summarizes long PDFs into a one-page brief.
>
> **Claude** scans the shelf and answers in one screen: "COMPOSE — you already
> own this in two pieces. `doc-digest` claims 'extract and condense the
> load-bearing content of long documents' and `brief-format` claims 'render any
> summary into a one-page decision brief'. Run doc-digest on the PDF, pipe its
> output through brief-format. If you'd still rather have a single command, say
> 'build it anyway' and I'll draft it — with a NOT-clause so it doesn't collide
> with doc-digest."

(Skill names in the example are illustrative.)

## Works well with

- [idea-probe](https://github.com/m1nga/idea-probe/) — the sibling gate for everything that *isn't* a
  skill: product, site, and feature ideas get persona wind-tunneling there. If
  your idea is a skill, extend-first checks the shelf first; if it survives as
  BUILD NEW and you want the concept itself tested, idea-probe is next.
- [scenario-probe](https://github.com/m1nga/scenario-probe/) — after a BUILD NEW verdict, the drafted
  boundary clause and the eventual description should be wind-tunneled before
  release. extend-first prevents overlap at birth; scenario-probe catches what
  slipped through.

## Design notes

Three observations shaped this skill:

- **One- and two-use skills are forgotten skills.** The gate exists because
  human memory of a library decays faster than the library grows — which also
  means the gate's value *increases* with every skill added. At five skills it
  is ceremony; at twenty-five it is the only thing standing between you and a
  shelf of near-duplicates.
- **A wrong merge costs more than a duplicate.** A duplicate wastes a
  directory. A bad merge bloats a working skill's trigger surface until it
  misfires for everyone, and unpicking it costs more than either skill did.
  That asymmetry is written into the verdict logic: uncertain calls go to
  BUILD NEW.
- **A gate that can't be overruled becomes a gate people route around.** The
  veto is one phrase and takes effect the same turn. The gate's job is to make
  overlap visible, not to win arguments — a check the user trusts to lose
  gracefully is a check they'll keep running.

## Field-tested

Before release, this skill went through an 8-scenario wind tunnel — 5 personas, 2 languages, including a fresh-install stranger with an empty shelf and head-to-head trigger collisions against 21 co-installed skills. Score: 3 clean passes, 5 degraded-risk findings, 0 harmful fires, 2 correct silences. Every finding below shipped as a fix before v1.

> **Messy dictation, Chinese (pass):** "那个,帮我搞个 skill 吧,就下载完自动把文件夹里乱七八糟的东西归归类那种" — the gate opened, compared by core function against the nearest neighbor, and returned a one-screen BUILD NEW with a drafted boundary clause. No ceremony, one screen, veto intact.

> **Correct silence:** "Probe this idea for a skill that auto-files my receipts" — three skills could have raised a hand here. extend-first stayed down: the verb is *probe*, not *create*, so the request belongs to idea-probe. A gate that fires on everything teaches you to stop consulting it.

> **Caught in the tunnel:** on "make me a skill…", the stock skill-creator claims the same sentence — and a model that jumps straight to authoring skips the duplicate check entirely, which is this skill's whole reason to exist. The description now states its position explicitly: *runs BEFORE skill-authoring tools — verdict first, then build.* The probe also caught the empty-shelf edge: a reachable-but-bare shelf is now an instant one-line BUILD NEW, never a nag for directory paths.

Probe method: [scenario-probe](https://github.com/m1nga/scenario-probe/)

## Author

Built and maintained by [Ming](https://github.com/m1nga). The design notes
above explain the real problem and tradeoffs that shaped this skill.
