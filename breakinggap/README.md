# BreakingGap — Three-Minute Reflection While AI Works

<img src="skills/breakinggap/assets/wordmark.svg" alt="BreakingGap" width="460">

**Stay sharp. Feel refreshed.**

Your agent is working. Your hand is reaching for your phone. Try a three-minute thinking break: one unexpected question, a little room to think, and a fresh angle to take back to your work. You don’t need to know what to ask.

## What it does

BreakingGap is an Agent Skill for a short, context-aware reflection inside your existing AI conversation. It helps independent makers step outside the immediate delivery, then choose whether an insight should stay a thought or become a focused conversation.

1. **Start where you are.** “How do you feel right now?” Answer Restless, Foggy, Stuck, Curious, Not sure, or use your own words. Skip it if you already know what you want.
2. **Try a fresh angle.** One light question grounded in the context available. Ask for more when you want a wider choice. Original motivation, an unexpected comparison, another perspective or a sourced old idea can all be starting points.
3. **Give the person room.** Think for about three minutes, pick any question, reply whenever ready. No countdown, obligation to answer everything, or automatic reminder.
4. **Put the thought in context.** Show a short synthesis of the person's words, relevant known project state and an open question. Keep interpretations separate from facts.
5. **Continue only if wanted.** Offer a focused new chat when useful. Create it only with the person's agreement and a supported host tool; otherwise provide a copy-ready starter. Keeping only the inspiration is a complete outcome.

A perspective can be wrong. The skill does not diagnose why you are stuck or treat every technical problem as a mindset issue. It can also offer a genuinely unrelated question, accept a rejected premise, or end as soon as your agent returns.

## Who it's for

Independent developers and makers who work with AI agents, move between uncertain waits and concentrated work, and want room to reconsider a purpose, assumption or choice. It is especially relevant when the next implementation step is clear but the broader question is still interesting.

It is not a task planner, therapist, automatic agent monitor or universal memory system. Installation does not expose all your chats or create a new-chat tool. Revisiting an idea requires a real source; a missing progress note is not proof you never started it.

## Install

```sh
npx skills add m1nga/breakinggap
```

Select your supported agent. Start immediately with one line:

**Codex**

> Use $breakinggap. Start a thinking break.

**Claude Code**

> /breakinggap Start a thinking break.

The skill opens with **“How do you feel right now?”** If you already say “I feel stuck” or “surprise me”, it skips that check and offers a question. In supported skill pickers, the default prompt provides this start entry. Installing the files itself does not open a conversation.

Natural language such as “I have a gap” can also match; automatic selection depends on the host. The portable `SKILL.md` needs no API key or additional service. See [Codex skills](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills](https://code.claude.com/docs/en/skills) for host setup. Local Codex installation has been checked. Claude Code format compatibility is documented; its runtime and new-chat behavior have not been tested.

## From a thought to a useful next conversation

An **illustrative, fictional** exchange:

> **You:** The agent is fixing my movie site's recommendation API. I have a gap and feel caught in the details.
>
> **BreakingGap:** While the API issue is being handled, here are a few angles:
> 1. What did you hope someone would feel after watching a film they found here?
> 2. If the recommendation API worked perfectly tomorrow, what would you still be unsure about?
> 3. Could someone coming back less often ever mean this was working well?
>
> Take about three minutes. Choose any one; a fragment or a different thought is enough.
>
> **You:** I wanted people to scroll less and really watch something. Now I'm designing around daily visits. I'm not sure those are the same thing.
>
> **BreakingGap:** Your original aim was deeper viewing; daily return has become another design goal. The API is still being fixed, so this thought does not explain that technical problem. A separate question has emerged: what would tell you the product is helping someone find a film worth watching?
>
> Want me to open a focused chat around that question, with this context, or leave it as a thought for now?

If you agree and the host supports it, the skill passes the relevant context and the question to a new chat. It does not treat the reflection as permission to change the product. If creation is unavailable, it gives you the prepared prompt and says the chat has not been opened. You can stop at any point.

## What about an automatic five-minute invitation?

This package does not watch agent progress or open windows in the background. No update for five minutes is not proof that a person is idle. A future host integration would need a real waiting signal, an explicit preference, an activity check, and at most one invitation per waiting period. It should never steal focus or repeatedly reopen a dismissed chat.

Codex supports lifecycle hooks, but a background hook finishing does not itself start a new turn. That is not an end-to-end idle invitation mechanism. See [Codex hooks](https://learn.chatgpt.com/docs/hooks). This proposed integration is not included or activated by installation.

## Why use a skill when AI can already do this?

Ordinary AI can ask reflective questions. BreakingGap packages a repeatable experience: offer an easy start, notice the actual situation, choose a fresh question, wait, respond to the person's meaning, then make a possible next conversation easy without forcing action.

The intended value is lower effort to enter that kind of reflection. It is not additional intelligence or guaranteed insight. A previous small same-model exercise produced enjoyable replies with and without the skill; it did not establish superiority. Real preference and sustained usefulness remain to be tested.

## Try the offline walkthrough

Open [companion.html](skills/breakinggap/assets/companion.html) from a downloaded copy of the repository. Try three waiting moments: about to scroll, still waiting, or losing the thread. Choose how you feel and press **Refresh me** for one prewritten question. The mood changes both the example opening and the starter you can take into your AI. All examples are fictional.

The page runs no model, reads no chat history, starts no timer and cannot open a new chat. Newly entered text stays only in the current tab. Previous v1 browser data is left untouched and can be exported from the same origin when available.

The text-only Br/Ga wordmark and dark green visual direction remain. See [the brand guide](BRAND.md).

## Design notes

The product began with ten-to-twenty-minute gaps between agent results. The first task-and-timer version missed part of the creator's intent. The next revision introduced playful dialogue. This revision makes the experience more explicit: open reflection for about three minutes, then a contextual synthesis and an optional focused chat. A useful break may leave only a new perspective.

Current author-source research informed the actual behavior:

- [Socratic Learning Coach](https://github.com/Shuboya1030/socratic-learning-coach/blob/cebfc0b479fd6983e54aef331d3c2a85f6dda821/SKILL.md): adapt the transition from a person's own reflection to a faithful synthesis. Preserve their wording and uncertainty. Reject its mandatory one-question tutoring loop, repeated probing of incomplete answers and full knowledge-document format; this break offers a few optional perspectives and accepts fragments.
- [Requirements Interview](https://github.com/SuperCorks/agent-skills/blob/498c6d75b3c4f95e072a14e80b15b23f43ec6a58/requirements-interview/SKILL.md): adopt context-first synthesis, source attribution and the distinction between observed state, inference and a decision. Carry those distinctions into the optional next chat. Reject restricting every question to an implementation decision; a philosophical thought can be useful without changing the plan.

The current onboarding pass also inspected [using-superpowers](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/using-superpowers/SKILL.md) and its separate [session-start hook](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/hooks/session-start). We adapted the distinction between instructions and a real runtime entry, and rejected global forced activation. Requirements Interview informed reusing a supplied mood instead of asking again. Our mood-first welcome is a design choice, not a result established by either source. No third-party code was copied or executed.

Rechecked for the shorter entry flow: retain a person’s own reflection, use plain questions, and preserve an easy exit; reject mandatory diagnostic interviews or forcing every thought into an action. Only these main instruction files were read for this comparison; their examples, references and runtime behavior were not evaluated. These are design inputs, not evidence that a questioning method improves outcomes.

## Evidence

The release checks skill structure, offline interaction and source/package consistency. Controlled model-response exercises and labeled failure simulations inspect conversational behavior; they are not field research. No measured productivity, wellbeing or creativity improvement is claimed. Live automatic routing and cross-host chat creation remain unverified.

The [legacy v1 helper](skills/breakinggap/references/session-format.md) is retained for existing file-backed sessions. It manages task/checkpoint records and does not generate this reflection experience.

## Author

Made by Ming. Useful feedback describes the situation, which question caught your attention, whether the synthesis represented your thought fairly, and whether you wanted to continue. Keep private project notes out of public issues.
