# BreakingGap — Small Steps While AI Agents Work

<img src="skills/breakinggap/assets/logo.png" alt="BreakingGap open-loop logo with an orange stepping block" width="140">

**A little gap. A little further.**

Your agent is working. You have ten minutes, a half-finished idea, and just enough attention for something worthwhile. BreakingGap helps you choose **one useful human step** and leave a clear place to return.

BreakingGap is an AI-agent skill with an optional offline companion. It turns a short waiting gap into a small contribution to your current work, an unfinished task, or relevant learning. It is designed for independent makers, developers, and knowledge workers who already work with agents.

## What it does

| Intention | A small, useful result |
| --- | --- |
| Move this forward | Write one acceptance example while an agent builds the feature. |
| Pick something up | Continue a saved opening paragraph without reopening an entire project. |
| Learn one thing | Explain one concept from your actual work, then check your understanding. |

You get one suggestion, its source, an estimated time allowance, a stopping point, and a cue for returning to your primary work. Setup and wrap-up count toward the budget; two minutes stay free for returning. You can stop early. You can also leave the gap empty.

## Install

```sh
npx skills add m1nga/breakinggap
```

In your agent, invoke the skill with your current work and available time:

> Use $breakinggap. My agent is building search. I have about 10 minutes. Help me make one useful contribution without touching the files it is editing.

Example response, using a **fictional** search-feature plan supplied in the conversation:

> **Try:** Write one acceptance check for an empty search result: the query, expected message, and a useful recovery action.
>
> **Why this fits:** You can clarify what “good” means without editing the agent's files. Estimate: 1 minute to reread the plan, 5 to write, 1 to save; 2 minutes remain for returning, with 1 minute spare.
>
> **Enough for now:** One runnable check in your notes. Stop after that check.
>
> **Return to:** Review the agent's search result against this example when it is ready.

“The agent is back” returns you to the primary work. It does not require finishing the small step first. For a learning step, you do the prediction or explanation; the skill helps you check it against the source.

## The offline companion

Open [`companion.html`](skills/breakinggap/assets/companion.html) from the downloaded package, keeping `logo.png` beside it. It includes clearly labeled fictional examples, three intentions, 10/15/20-minute choices, a pauseable timer, and a checkpoint export. No account or network request is needed. Hidden tabs pause the timer; reopening never resumes it automatically.

For real work, ask the skill to prepare an import from your current project. The page uses a **saved snapshot**, not a live connection. It cannot verify source files or observe an agent. Tell it when your agent is ready. Browser data stays on that browser origin; exports are portable, and imported data is never written back to source files automatically. Shared-device users should handle browser storage and exported notes as local work data.

For file-backed use, the optional Python 3.9+ helper verifies local source hashes and keeps one recoverable session. See the [helper contract](skills/breakinggap/references/session-format.md). Python is not required for conversational use. Browser exports and the helper's journal are separate; the skill reconciles a checkpoint only after checking current work.

## Who it's for

Use it when you already have a bounded gap and want a worthwhile next move. It does not monitor agents, schedule your day, resume paused projects, resolve competing owners, or make uncertain waits predictable. Unknown or conflicting work is excluded. A task's eligibility and time estimate still require judgment.

## Design notes

Waiting can leave room for curiosity as well as productivity. The design protects that choice: one step, an easy stopping point, a clear return, no streak to maintain. The [brand guide](BRAND.md) explains the audience, promise, visual identity, and initial validation plan.

Current author-source research informed three decisions:

- [unforget](https://github.com/Terryc21/unforget/blob/cf907b2c35aa2a2cc1a4cc2c75cb75f60f3ff5fc/skills/unforget/SKILL.md): adopt checking that unfinished work is still open; adapt it to existing project records rather than another backlog.
- [tutorial-creator](https://github.com/Terryc21/tutorial-creator/blob/6d4b025615405ea1fc0c5e7c70b6fb36785ab0d0/skills/tutorial-creator/SKILL.md): adapt project-grounded, active learning into one short question and an honest checkpoint.
- [StayOn](https://github.com/ahzia/StayOn-Claude-Mod/blob/710f5d1d1aa309fbf6c716de7d515364bffcdabb/hooks/core/recommend.ts): adopt ready, independent, human-owned work and one recommendation; reject fixed fallback estimates and unverified notification promises.

These are design influences, not incorporated third-party code or proof of effectiveness. BreakingGap is not claimed to be the first tool in this area.

## Evidence

The release is checked with local helper tests, companion checks, browser interaction, and labeled instruction scenarios. Those checks cover behavior and recovery, not productivity gains. There are no claimed customer numbers, measured time savings, learning gains, or long-term field results. The first useful test is whether a real person makes something worthwhile **and returns without extra friction**.

## Author

Made by Ming. Feedback is most useful with the original waiting situation, the suggested step, and what made returning easier or harder. Do not include private project material in public issues.
