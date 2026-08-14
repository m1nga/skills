---
name: grilling
description: Interview the user relentlessly about a plan or build, then produce a locked, scoped plan before any execution. Trigger when the user explicitly asks to be questioned or stress-tested — "grill me on this plan", "poke holes in this before I build it", "interview me until this is fully scoped", "ask me everything you need before writing code", "don't let me start until the plan is tight"; Chinese triggers — 拷问我 / 盘问这个方案 / 开工前把我问透 / 先问清楚再动手. Also trigger for an explicit build the user wants scoped through questioning before execution — only when they show willingness to answer questions. Do NOT trigger on delegation or authorization phrases ("just do it", "you decide", "你看着办") — those grant execution, not an interview. For lightweight feedback on a plan, or open-ended thinking with no concrete build to scope, yield to the thinking-partner skill. NOT for mock interviews or quiz practice ('grill me on React questions').
---

Run a relentless interview that ENDS in a locked, scoped plan. Three phases. Do not skip ahead to building.

Conduct the whole session in the language the user is using (Chinese in, Chinese out). This skill handles dictated, messy, mixed-language input — never ask the user to clean up their phrasing; extract the plan from whatever form it arrives in.

## P1 — GRILL

Interview the user relentlessly about every aspect of the plan until you reach shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

- Ask **one question at a time**, waiting for the answer before the next. Asking multiple at once is bewildering.
- For **every question, give YOUR recommended answer** + a one-line rationale. The user confirms or redirects — never hand the decision back blank.
- If a question can be answered by exploring the codebase (or searching the web, when the task turns on external facts), do that instead of asking. In an environment without file or web access, say so and ask the user instead.
- **Every 3–4 questions, inject one perspective from OUTSIDE the current frame** — a lens, an opposite assumption, or a cross-domain analogy the user did not bring. Widen the frame; do not change their direction.
- **Exit valve:** if the user says "just decide" / "stop asking" / "别问了", collapse all remaining branches into your recommended answers and jump straight to P2.

## P1.5 — REFRAME

Before planning, restate the problem in ONE fresh sentence the user did not use. If the real problem underneath is different from the stated one, say so now.

## P2 — PLAN

Produce a plan with these exact sections:

- **Goal** — one sentence, locked.
- **Decisions locked** — what the grill settled.
- **Decisions open** — what's still unresolved, and why.
- **What we are NOT doing** — mandatory scope control. List the tempting-but-excluded explicitly.
- **Steps** — each independently completable in one sitting.
- **Checkpoints** — where the user reviews before you continue.
- **Branches** — forks where the plan changes based on what we find.
- **Drift triggers** — the specific signals that mean we've gone off-scope.

If the user wants the plan saved, write it to a location they name — never inside this skill's directory. If writing to disk is not possible, output the full plan as copyable text instead.

## P3 — EXECUTE

Wait for the user's explicit "go". Pause at every checkpoint. Flag drift the moment a drift trigger fires — never silently push through it.
