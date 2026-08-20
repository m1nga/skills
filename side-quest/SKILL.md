---
name: side-quest
description: >-
  Park a mid-flow thought without breaking your main thread — capture it in one line, a background
  agent works it while you keep going, and results land in an inbox outside the chat, keeping main
  context clean both ways. Ledger-first (a parked thought can never be silently lost), draft-only
  (side agents never send, commit, or touch your working tree), receipts carry a one-line verdict.
  Fires without confirmation on explicit markers — "sq:", "side quest:", "background this", "park
  this", "not now but:", 支线 / 先别进主线 / 后台弄 — and on queue check-ins ("sq list", "sq retry", "sq kill",
  "what came back from my side quests?"). Inferred phrasings get a one-line confirm, defaulting to the
  main thread. NOT for blocking prerequisites the main task needs next, NOT for ten-second questions
  (answered inline), NOT for reminders (routed to a scheduler, never faked as work), NOT for merely
  setting a topic aside with no work attached (这个先放一边), NOT a way to send or do anything irreversible.
---

# Side Quest

A thought that arrives mid-flow has two bad exits: chase it (lose the thread) or
suppress it (it re-intrudes every ninety seconds — the Zeigarnik effect keeps
unfinished loops knocking until the mind trusts they are handled). This skill
builds the third exit: park it in one line, keep working, and collect the
finished work at your next natural break.

**The trust contract, before any mechanics:** a parked thought can never be
silently lost, and a completion mark can never lie. The moment either breaks
once, the user's mind stops releasing thoughts and the tool is dead. Every rule
below serves that contract; when in doubt, protect the contract, not the feature.

## Step 1 — Capture and triage (≤5 seconds of the user's attention)

Explicit markers fire immediately, no questions: `sq:` / `side quest:` /
`background this` / `park this` / `not now but:` / 支线 / 先别进主线 / 后台弄.
Inferred phrasings ("btw can you also…", "哦对了那个…回头弄", "…anyway keep
going") get ONE line —
"→ background as a side quest? (default: handle it now in-thread)" — and
ambiguity resolves to the main thread. Capture never asks a second question.

Before dispatching, triage the thought — most "side quests" are something else:

| Shape | Tell | Route |
|---|---|---|
| Ten-second question | You can answer confidently in one short line | Answer inline in brackets, no dispatch, no file — ceremony here is self-parody |
| Blocking prerequisite | "first / before we continue / 先" or it references the artifact being edited; the main task's next step depends on the answer | Stays in the main thread — backgrounding it means the main line proceeds on an unverified assumption |
| Backfill quest | The answer feeds a pending main-thread decision | Dispatch, but declare: "conclusion (≤3 lines) will return to this thread; details to inbox" — a vetoable default, not a question |
| Reminder | There is no work product, only a time ("submit readings tomorrow 10am") | Route to the scheduler/reminders if available; receipt says "reminder set, not a task". Never manufacture fake work for it; no time given → default 'before end of day' and say so in the receipt; no scheduler available → ledger it as 'reminder — NOT scheduled, recorded only' and hand the text back |
| Life-size decision | "should I kill project X" | Receipt: "that's a decision, not a task — it deserves its own conversation." A background agent must not settle it from one sentence; if the user asked to park it (先别打断), capture and queue it — do not open the discussion now |
| Resident job | It changes ground the main session stands on (its config, rules, deps, git state) | Never execute live. Deliver a diff/plan to the inbox, to be applied at a session boundary |
| Quest about the main line itself | "sq: check whether our current approach is over-engineered" | Surface it: "this questions the current approach — discuss now, or truly background?" (the one place a question is allowed, and it happens pre-dispatch, in the main window) |
| Deprioritization | "这个先放一边 / let's park this topic" with NO work requested — there is nothing to deliver | Verbal ack only; no dispatch, no ledger entry |
| Quest about this conversation | "sq: summarize what we did" — the object is the transcript itself, which side agents never receive | Cannot background; run inline at the next boundary (defer to conclude-rounds if installed) |
| Actionable with side effects | "email X / open a PR / file the ticket" | Dispatch as DRAFT-only — the deliverable is the loaded gun, never the fired shot |
| True side quest | ≥2 minutes of independent work, no main-thread dependency, no side effects | Dispatch (below) |

Multiple quests in one message ("sq×3: …") = one merged ledger entry set, one
combined confirmation line.

## Step 2 — Ledger first (write-ahead; the non-negotiable)

BEFORE spawning anything, append to the inbox's `_INBOX.md`:

```
| date-time | user's words, VERBATIM | brief (1 line) | state |
```

States: `captured → dispatched → done | failed | partial | queued`. Every
terminal state produces a receipt. If a session dies, orphaned `dispatched`
entries are announced the next time this skill loads (any sq marker, "sq list",
or an inbox mention) — after reconciling with the inbox first: if the
deliverable file already exists, mark it done, not failed; announcing a false
failure breaks the same contract as silence. A quest may never end without a
durable trace. The verbatim words are sacred: never retitle the
user's thought; they find it by their own words, not by your summary.

## Step 3 — The brief (curated context, not zero context)

The laziest real utterances are deictic — "this pattern", "that chart lib",
"刚才第三段". A background agent given only the raw words will guess, and
confidently. So the MAIN agent — the one holding the conversation — pays the
serialization cost, never the user:

- Resolve every pronoun and reference into a **self-contained brief, ≤5 lines**:
  the thought itself, what it refers to (named explicitly), what the user was
  doing, and the expected shape of the deliverable.
- For repo/code quests, add a **static environment fingerprint** (≤10 lines:
  cwd, branch, stack facts from the project's own docs). Environment facts are
  not contamination; conversation history is. The side agent receives the brief
  and fingerprint ONLY — never the transcript.
- The confirmation line echoes the brief's one-line reading, not the raw words —
  echo-as-verification, no question asked: `⚡ sq #4 "check webhook retry
  dedup (billing service, src/hooks)" — say "撤"/"cancel" to pull it back.`
  Folder names, file names, and ALL receipt/confirmation templates follow the
  conversation's language (the cancel word too: 撤 for Chinese, cancel for
  English).
- `sq (isolated): …` forces a zero-brief dispatch for the rare quest the user
  wants fully sealed.

If the reference cannot be resolved from context, do NOT ask — ledger it with
the note "context insufficient; interpreted literally" and dispatch the literal
reading. A wrong draft plus an honest note beats an interrogation.

## Step 4 — Execution rules (for the side agent)

**Rule transport:** the side agent never reads this file — every dispatch
prompt embeds Step 4's rules verbatim beneath the brief. A rule not in the
prompt does not exist for the side agent.

- **Draft-only, iron rule.** No sends, no publishes, no PRs/issues, no installs
  into shared environments, no purchases, no deletions — anywhere, ever. An
  actionable quest ships as a draft whose first line is `DRAFT — NOT SENT / NOT
  APPLIED`. The trigger word requests relief, not authority.
- **Workspace law.** Never touch the user's working tree, git state, config, or
  anything the main session stands on. Repo quests run in a fresh `git worktree`
  (placed under `~/side-quests/worktrees/<slug>`, never inside the user's repo)
  from a clean ref; the deliverable is a branch name plus one merge command.
  Writes are permitted only inside the inbox directory and the quest worktree.
- **Assume forward, assumptions on top.** No questions back — make the call,
  and open the deliverable with an ASSUMPTIONS block (≤5, each with "if wrong →
  discard section N"). When confidence is genuinely low, ship two small
  versions or an honest partial — never dress a guess as a completion.
- **Output is proportional to input.** A two-word quest gets at most one page.
  No unrequested expansions; over-delivery raises the cost of opening the inbox,
  and an unopened inbox kills the tool.
- **Run cheap and polite.** Default to a lighter model/effort than the main
  thread; at most 2 quests run concurrently (others wait as `queued`); side
  quests must never starve the main session's rate limits — the first dispatch
  each session notes once: "runs in background — shares your usage limits."

## Step 5 — Receipts (buffered, honest, verdict-bearing)

- Dispatch confirmation: one fixed-format line, immediately (Step 3's echo).
- Completion/failure receipts **never interrupt**: they queue silently and
  attach to the next natural boundary — the assistant's next reply after the
  user speaks. Never mid-generation, never as a standalone ping. If the
  harness forces a render turn when a background result arrives, output
  nothing beyond a minimal one-line ack.
- A receipt carries: the user's verbatim words, a **one-line verdict**, and the
  highest-risk assumption:
  `✅ sq "stripe retries dedup?" — yes, dedupes on event_id (webhook.ts:41);
  assumed billing-service repo. Note in inbox.`
  Answer-shaped quests (yes/no, a number, a flag) are CLOSED by the receipt
  line itself; the file is optional.
- Failures are receipts too: `⚠️ sq "X" failed (rate limit) — your words are
  safe in _INBOX.md; say "sq retry" to redispatch.`
- `sq list` shows the queue with states; `sq kill <n>` cancels; `sq redo "<X>":
  <correction>` redispatches with the stored brief plus the correction — no
  re-explaining.

## Step 6 — Inbox and resurfacing (anti-graveyard)

- Default location `~/side-quests/` — never colonize the Desktop uninvited; the
  user may configure any folder (stored in `~/side-quests/config.md`). Folder
  names, file names, and ALL receipt/confirmation templates follow the
  conversation's language (the cancel word too: 撤 for Chinese, cancel for
  English).
- Files are named `YYMMDD--<slug of the user's verbatim words>.md`, never
  agent-invented titles, never bare timestamps.
- Deliverables always land inside the inbox (a `staging/` subfolder for files
  meant to move elsewhere); the receipt includes the one-line move command —
  writing to user-specified locations outside the inbox stays with the user or
  the main thread.
- Deliverable header, fixed: verbatim words · captured-at + what the main
  thread was · TL;DR ≤3 lines · ASSUMPTIONS · suggested next step. The reader
  decides in one screen whether to read on.
- `_INBOX.md` is the living index (date | words | state | three-word result |
  file). At the skill's next load in a new session — a natural boundary, not
  an interruption — if
  unread results exist, print a quiet one-line-per-item digest with ages, plus
  "say 'archive all' to clear". No unread counters mid-session, no guilt
  language, no reminders that interrupt work: the inbox must be there when the
  user wants it, never demand attention for itself.
- Results untouched for 7 days move silently to `archive/` (marked in the
  index, never deleted). The pile must not be able to grow into a reproach.

## Degraded environments

- **No background-agent capability** (some engines/harnesses): capture, triage,
  ledger, and brief still run in full — they are the product's core. The quest
  sits as `queued`; offer "run it inline at your next break, or leave it
  queued". Never pretend it is running.
- **No disk access**: emit the ledger line and brief as a copyable block and
  say where to save it. Never drop a thought silently.

## Boundaries

- The dispatch turn belongs to the main thread: acknowledge in one line and
  continue the user's actual work — never let parking a thought become the
  interruption it exists to prevent.
- This skill is not a scheduler, not a to-do app, and not a way to launder
  irreversible actions through a background agent.
- If the completion mark's honesty ever conflicts with looking productive,
  honesty wins. A trustworthy ledger of unfinished quests beats a gallery of
  confident garbage.
