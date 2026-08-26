---
name: extend-first
description: >-
  Before building a new skill, agent, command, or automation, check whether an existing one already
  covers it. Runs BEFORE skill-authoring tools like skill-creator — verdict first, then build. Fires
  when the user asks to CREATE a new capability: "make me a skill for X", "build me an agent that
  does Y", 做一个 skill / 帮我建个 agent / 新写一个自动化. Inventories installed skills and the user's skill
  directories at description level, compares by core function (problem solved, input/output shape,
  judgment vs. execution — never name or keyword similarity), then gives a one-screen,
  evidence-quoted verdict: EXTEND (which skill, which section, what change), COMPOSE (two existing
  skills together, usage included), or BUILD NEW (no overlap confirmed, plus a drafted description
  boundary against the nearest neighbor). Overridable — "build it anyway" / 还是新建 ends the check. NOT
  for using an existing skill, NOT for non-skill product or project ideas (idea-probe's seat, if
  installed), skipped on "skip the check, just build" / 直接新建别查了.
---

# Extend First（先查书架）

A skill used once or twice gets forgotten; a library past a dozen skills is bigger
than its owner's memory of it. So the third "new skill" request for the same problem
does not feel like a repeat — it feels new. This skill is the librarian at the door:
before anything gets built, it checks the shelf, and it checks by what the books
*do*, not what they are called.

The gate is advisory, never a roadblock. It exists to make the overlap visible in
one screen; the user always holds the veto.

## Step 0 — Confirm the gate should run

Run only when the request is to **create** a skill, agent, or automation. Stand
down, without commentary, when:

- The request is to *use* a capability ("run the probe on this") — just route it.
- The idea is a product, site, or feature rather than a skill/agent — that
  belongs to idea-probe (if installed), which tests the idea itself, not overlap.
- The user pre-empts the check ("直接新建别查了" / "skip the check, just build") —
  respect it silently; do not sneak the inventory in anyway.

When the create request surfaces mid-way through another task that is still in
progress, do not derail it: confirm in one line first — 「现在查还是收尾后查?」
("check now, or after we wrap up?") — or park the request via side-quest (if
installed) and run the gate at the next natural stopping point.

## Step 1 — Inventory the shelf

Inventory the shelf of the requested kind: skill requests scan skills; agent
requests also scan the harness's agent definitions; automation requests also
scan hooks and scheduled tasks.

Gather, in order of cheapness:

1. **Installed skills** — the harness's skill listing, when one is exposed.
2. **The user's skill directories** — their skills repo and any local skill
   folders, including not-yet-installed drafts, scanned at the *description
   level*: frontmatter `name` + `description` only. Ask for the directory path
   once, on first use; on later runs reuse the answer instead of asking again.

Do not read bodies at this stage. Descriptions are the trigger surface and the
honest summary of what each skill claims; bodies are read later, and only for the
1–3 nearest candidates. If no inventory source is reachable, say so and ask for a
path — a verdict faked from an unseen shelf is worthless. A shelf that is
reachable and genuinely empty is the opposite: an instant one-line BUILD NEW, no
questions asked.

## Step 2 — Compare by core function, never by name

Name and keyword similarity is banned as evidence, in both directions: two skills
with unrelated names can be the same tool, and two skills sharing a word can be
strangers. Compare each candidate on three axes:

| Axis | Question |
|---|---|
| **Problem** | What user pain does it remove? Would the new request's pain vanish if this skill ran? |
| **Shape** | Input → output. What does it take in, what does it hand back? |
| **Nature** | Judgment (a verdict, a report, a ranking) or execution (it does work, produces artifacts)? |

Two skills overlap when they match on Problem and roughly on Shape. A Nature
mismatch usually means COMPOSE, not EXTEND: a judgment skill and an execution
skill about the same problem are a pipeline, not duplicates.

For the 1–3 nearest candidates only, open the body far enough to verify the
description isn't overclaiming — a description that promises the requested
capability while the body doesn't deliver it is a finding, not a match.

## Step 3 — The verdict（判决）

One screen, in the user's language, exactly one of three calls. Every claim about
an existing skill quotes that skill's description **verbatim** — the user must be
able to check the evidence without opening anything.

- **EXTEND** — name the skill, name the section, state the change: "add a mode
  to Step 2", "widen the description's trigger list with these phrases", "new
  table row". Specific enough to apply; an EXTEND verdict that says "just merge
  them somehow" is a non-verdict.
- **COMPOSE** — name the two existing skills whose combination covers the
  request, and give the combined usage: which fires first, what hands off to
  what, one example invocation. If composition needs glue beyond "run A, then
  B on A's output", it is not COMPOSE — reconsider.
- **BUILD NEW** — confirm no overlap on the axes above, then do the drive-by
  favor: draft the boundary clause — a NOT-sentence for the new skill's
  description and, when useful, a matching one for its nearest neighbor — so the
  two never collide at trigger time. The gate's last act is to prevent the
  *next* overlap.

**Tie-break rule:** when the verdict is genuinely uncertain, call BUILD NEW. A
wrong merge is more expensive than a duplicate — a duplicate wastes a directory;
a bad merge bloats a working skill's trigger surface and body until it misfires
for everyone, and unpicking it costs more than either skill did.

## The contract

- **Short.** The verdict fits one screen. The inventory happened; it is not
  recited. At most: verdict, evidence quotes, the concrete next step.
- **Evidenced.** Descriptions quoted verbatim, with the skill's name. No
  paraphrased overlap claims.
- **Vetoable.** "还是新建" / "I'd rather build new" ends the discussion in that
  same turn — proceed with the build, no relitigating, no "as I mentioned". The
  gate ran, the owner decided, that is the system working.

## Boundaries

- This skill decides *whether* to build, never builds. After a BUILD NEW verdict,
  the actual authoring belongs to the user's skill-writing workflow.
- It reports on existing skills; it never edits them. An EXTEND verdict is a
  proposal the owner applies.
- No manufactured overlap: if the shelf genuinely has nothing close, say so in
  one line and get out of the way. A gate that always finds something teaches
  the user to stop consulting it.
