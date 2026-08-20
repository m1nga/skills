# side-quest

**Park the thought, keep your flow — a background agent does the side quest
while your main thread never notices.**

## The problem it actually solves

A thought that arrives mid-flow has two exits, both bad: chase it and lose your
thread (refocusing after an interruption takes ~23 minutes), or suppress it and
let it knock every ninety seconds — psychologists call that the Zeigarnik
effect: unfinished loops occupy working memory until the mind trusts they're
handled. Research (Masicampo & Baumeister, 2011) shows the loop releases the
moment a *credible plan* exists — the task doesn't have to be done, you just
have to believe it will be.

side-quest builds that credible plan in one line — then actually does the work:

```
you:  sq: is our webhook retry actually idempotent? don't stop, keep going
main: ⚡ sq #1 "verify webhook retry dedup (billing service)" — say "cancel" to pull it back
      …main thread continues exactly where it was…
(later, attached to a normal reply)
main: ✅ sq #1 — yes, dedupes on event_id (webhook.ts:41); assumed billing repo. Note in inbox.
```

## Who it's for

- **People whose ideas arrive faster than their hands** — twenty browser tabs,
  a notes app full of three-word fragments nobody ever reopens.
- **Flow-protective workers** who know what a context switch costs and refuse
  to pay it — but pay for the suppressed thought instead.
- **ADHD-pattern thinkers** (by identification, not diagnosis), for whom a
  capture system isn't productivity sugar but a working-memory prosthetic —
  and who have abandoned five GTD tools because the collection basket became a
  graveyard. This skill's anti-graveyard rules exist because of you.
- **Long-session heavy users** whose main conversation *is* capital — hours of
  accumulated context that every off-topic exchange dilutes.

## What makes it different from a notes file

A notes line is free, never lies, and never dies — that's the real competition.
side-quest beats it only under a strict contract, so the contract is the design:

1. **Ledger-first.** Your verbatim words hit disk *before* any agent starts.
   Crashes produce failure receipts at your next side-quest use — never
   silence. A parked thought can never be silently lost.
2. **Curated brief, not zero context.** Your laziest phrasing ("that chart lib
   thing") is resolved by the main agent — which has the context — into a
   self-contained brief. The background agent never sees your conversation.
3. **Draft-only.** Side agents never send, commit, install, or touch your
   working tree. Actionable quests come back as loaded drafts; you pull the
   trigger.
4. **Honest receipts, never interruptions.** Completion notes wait for a
   natural boundary and carry a one-line verdict plus the riskiest assumption.
   A completion mark that lies once kills the tool, so it never gets to lie.
5. **Anti-graveyard inbox.** Files named by your own words, a one-screen
   header, a quiet digest at your next side-quest use, auto-archive after 7
   days — and zero
   mid-session nagging, ever. The inbox is there when you want it; it never
   demands attention for itself.

## When it fires

- "sq: 10 name ideas for the CLI, nothing cute"
- "background this: why is docker build 2x slower since tuesday"
- "not now but: license check on that chart lib we vendored"
- "支线:查一下 Zeigarnik 原始实验是哪年的"
- "哦对了那个域名的事,先别进主线,后台弄"

And when it deliberately doesn't: blocking prerequisites stay in the main
thread; ten-second questions get answered inline (dispatching an agent to look
up a flag is self-parody); reminders route to your scheduler instead of
becoming fake work; "email the team" comes back as a draft, not a sent email.

## Install

```bash
npx skills add m1nga/skills@side-quest
```

## Works well with

- [thinking-partner](../thinking-partner/) — a side quest that turns out to be
  a real decision gets handed here
- [conclude-rounds](../conclude-rounds/) — session recaps naturally list what
  your side quests shipped
- [desktop-package](../desktop-package/) — same delivery philosophy: work you
  can review cold, outside the chat

## Design notes

Built persona-first: five simulated users (idea-flooded builder, flow guard,
ADHD-pattern thinker, long-session context keeper, English-only skeptic) each
lived the full flow from thought-strike to day three, before a line was
written. All five independently rejected the same early design (zero-context
dispatch) and independently demanded the same fixes: write-ahead ledger,
resolved briefs, draft-only agents, buffered verdict-bearing receipts, and an
inbox that cannot grow into a reproach. The skeptic's closing line became the
spec: "a single silent drop is not negotiable."

## Field-tested

Wind-tunneled with [scenario-probe](../scenario-probe/) before release: 21 scenarios across two probe passes — 11 birth utterances from the five design personas, plus 10 contract-stress scenarios (session crash mid-dispatch, an English-only stranger, a Codex engine with no background capability). Score: 17 clean passes · 4 degraded-with-notes · 0 harmful behaviors · 2 blockers fixed before publish (a YAML validity bug and one promise the mechanism couldn't keep).

> **"sq: remind me to tag the release at 5pm"** — the fake-work trap. No agent spawned, no file created: the reminder routed to the scheduler with the receipt "reminder set, not a task."

> **"sq: email the team the migration moved to Friday"** — came back as a file whose first line reads `DRAFT — NOT SENT`. Four separate rules lock side agents out of sending anything, anywhere.

> **Session killed right after dispatch** — the parked words survived on disk (the write-ahead ledger runs before any agent spawns), and the probe caught that the original "announced at session start" promise couldn't actually be kept by a skill that only loads when triggered. The wording was fixed before release; nothing is ever silently lost.

Probe method: [scenario-probe](../scenario-probe/)
