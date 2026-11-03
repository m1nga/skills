# BreakingGap — Playful Brainstorming While AI Works

<img src="skills/breakinggap/assets/wordmark.svg" alt="BreakingGap" width="460">

**Let a different thought in.**

Your agent is working. You have a gap. BreakingGap gives you one interesting opening: a sideways question about your project, a surprising connection, or a gentle return to an idea you once wanted to try. You answer; the conversation develops from there.

## What it does

BreakingGap is an Agent Skill for short, playful thinking breaks inside your existing AI conversation. It uses the context that is actually available, invites your own thinking, and lets you leave as soon as you want.

| Direction | What a conversation might open up |
| --- | --- |
| Change the angle | “What would a visitor enjoy here if they never created an account?” |
| Make a strange connection | “What could this onboarding learn from a good dinner host?” |
| Revisit an idea | “You mentioned giving photographs their own soundtracks. I don't know whether you tried it since. Want to imagine the first five seconds?” |

These are illustrative prompts, not facts about you. A repeated intention needs distinct, direct user mentions; lack of a progress note does not prove you never started. If you want a completely unrelated game or a quiet break, that choice counts too.

## Who it's for

Independent makers, developers, writers, and curious knowledge workers who already use AI agents and sometimes want a lighter way to think while waiting. You do not need another backlog, timer, or productivity score. A conversation can be worthwhile without producing a document.

It is not a full design workshop, automatic agent monitor, reminder service, or universal memory system. It cannot access other chats merely because you installed it. It respects the host's available tools, source access, and permissions.

## Install

```sh
npx skills add m1nga/breakinggap
```

Select your supported agent during installation. Then invoke the installed skill explicitly:

**Codex**

> Use $breakinggap. I have a gap while my agent works. Give me one interesting angle to explore together.

**Claude Code**

> /breakinggap I have a gap. Let's play with a different angle on this project.

Or say “I have a gap—what could we explore?” Automatic selection depends on the host. The same portable `SKILL.md` is used in both; no custom service or API key is required. See [Codex's skills documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code's skills documentation](https://code.claude.com/docs/en/skills) for current host setup. Codex installation is verified in this release; Claude Code compatibility is based on the documented skill format, not a runtime test.

## A conversation, not just a prompt

An **illustrative** exchange while a signup feature is being built:

> **You:** I have a gap. I'm tired of staring at this registration flow.
>
> **BreakingGap:** Imagine someone visits this community every week and never posts. What could happen on their first visit that makes them feel welcome?
>
> **You:** They could choose a photo they want to sit with, without having to like or comment.
>
> **BreakingGap:** That makes browsing feel like choosing a place to stay. What would help them feel they can leave without owing the community a response?
>
> **You:** My agent's back.
>
> **BreakingGap:** Back to the signup review. The thought to keep, if useful: browsing can be a complete form of participation.

No mandatory recap, saving step, or unfinished-exercise penalty. It does not write to project files unless asked or already authorized.

## Why use a skill when AI can already do this?

You can ask ordinary AI for this. BreakingGap does not add intelligence or unlock hidden memory. It packages a particular interaction: start from the actual situation, choose one fresh angle, wait for your answer, develop that answer, handle remembered intentions carefully, and get out of the way when you return.

That consistency is the intended value. It has to earn its place through use. A small same-model response exercise during this revision produced enjoyable replies with both a plain request and the skill. It did **not** establish that the skill is better. We are testing whether people prefer this behavior repeatedly, not claiming a capability they cannot get from AI otherwise.

## Try the visual playground

Download the repository and open [`companion.html`](skills/breakinggap/assets/companion.html). It is a single-file offline playground with clearly fictional dialogues and an editable starter to copy into your AI. It does not run a model, read history, or connect to agents. It keeps newly entered context only in the current tab. Previous v1 browser data is left untouched and can be exported from the same browser origin when available.

The visual identity uses a **text-only BreakingGap wordmark**, element-like Br/Ga tiles, dark chemical greens and aged off-white type. The [brand guide](BRAND.md) explains the audience and direction. There is no separate icon mark.

## Design notes

The originating question was about ten-to-twenty-minute agent waits. The first version emphasized finding small tasks and keeping checkpoints. The direction changed after the creator pointed out that ordinary AI already covers task suggestions: the interesting part was brainstorming, curiosity, and thoughtful recall, with room to step away from heavy work.

Current author-source research changed the actual instructions:

- [creative-thinking](https://github.com/ysskrishna/ai-agent-skills/blob/f2bebb8e94b6292d372e1db8dbc4401fc3e2346f/skills/creative-thinking/SKILL.md): adapt analogy, rule reversal, and changes of viewpoint into one conversational opening. Leave the full workshop and long idea lists out.
- [unforget](https://github.com/Terryc21/unforget/blob/cf907b2c35aa2a2cc1a4cc2c75cb75f60f3ff5fc/skills/unforget/SKILL.md): adopt checking whether old work is still open; distinguish a sourced intention from an inferred wish or missing progress record. Do not build a debt ledger.
- [superpowers brainstorming](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md): adopt reading the existing context before asking questions; leave its design-document and planning workflow out of short breaks.
- [Oblique Strategies](https://enoshop.co.uk/products/oblique-strategies): the compact creative prompt is a useful form reference. BreakingGap's example prompts are original; it does not reproduce the card deck.

## Evidence

This revision includes controlled model-response exercises, labeled instruction simulations, offline playground checks and browser interaction. They test instruction behavior and UI function, not proven creativity, engagement, wellbeing, or productivity improvements. Actual host routing and long-term user preference remain unverified. No customer numbers, testimonials, or measured time savings are claimed.

The optional v1 [Python helper](skills/breakinggap/references/session-format.md) remains for existing file-backed sessions. It verifies task source hashes and preserves its checkpoint journal; it does not generate creative dialogue or discover repeated intentions. It is not the default v2 experience.

## Author

Made by Ming. Useful feedback describes the waiting situation, the first question, whether you wanted to answer, and whether returning was easy. Keep private project notes out of public issues.
