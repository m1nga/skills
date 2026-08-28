# listen-compare

**A personal work radio: turn work content into Chinese audio you listen to while cooking, driving, or doing chores — comparisons, summaries, second opinions, risk scans.**

## What it does

Your ears are free when your hands are busy. This skill turns work content into
programs for that time, in four types: 对比 (2+ documents — key points, then
agreements, then differences organized by topic), 总结 (one document or a piece of
work), 观点 (more perspectives on the work at hand, always including the strongest
counter-case), and 潜在问题 (a risk scan that separates evidence from guesses).

It also solves the delivery problem with two conventions. A **fixed radio link**:
every program publishes to the same URL, so the phone bookmark always opens the
latest episode. And a **parking protocol**: any mid-task Claude window can drop a
self-contained material file into the 收件箱 folder and go straight back to work —
audio is never produced inside a task window; the radio window picks material up
later with one phrase (出音频).

The script obeys ear rules a written summary ignores: no tables or bullets, spoken
signposts between sections, numbers rounded to what a listener can hold ("大概三成"
not "31.4%"), English terms glossed in Chinese on first use, every paragraph under
~35 seconds (≤150 characters).

Delivery is deliberately low-tech: the full script lands as plain text (any
read-aloud feature can speak it), and where HTML artifacts are available you also
get a tap-to-play player — tap any section to play on from there, pause, speed
control; playback needs no network and no account. Wherever the producer can run
edge-tts (free neural voices, network required at production time), the player
ships with embedded recordings that sound identical on every device; produced on
the phone itself, it falls back to the phone's own Chinese voice, and refuses with
a clear message if no Chinese voice is installed.

## When it fires

- "这两份分析我没时间看,念给我听,告诉我异同。" (produce: 对比)
- "出音频。" / "收件箱里有什么,播了。" (produce: whatever is parked)
- "给我做个15分钟的音频,要更多观点和思考,回头我做饭的时候听。" — said mid-task
  in another window (park: writes the material file, replies one line, returns to
  the task)
- "Read these two PDFs to me and tell me where they disagree."

It stays quiet for written summaries you'll read with your eyes, podcast
production, and audio transcription.

## Install

```bash
npx skills add m1nga/skills@listen-compare
```

## Example

> **You:** 这两份市场分析我没时间看,念给我听,重点是它们哪里不一样。
>
> **Claude:** *(reads both, replies with the script — 开场 → 先说结论 → 第一份 →
> 第二份 → 相同点 → 不同点 → 收尾 — and a tap-to-play player link)* 手机点开,按 ▶ 就能听,约 5 分钟。

## Works well with

- [one-sentence](../one-sentence/) — the 收尾 verdict is a one-sentence discipline
- [conclude-rounds](../conclude-rounds/) — recap rounds in text; this skill is the same honesty for ears

## Design notes

The comparison section is organized by question, never by document — "在增长预期上,
A 乐观 B 保守" is a comparison; "A 说了这些,B 说了那些" is two summaries stapled
together. Honesty rules are load-bearing: if the two documents don't actually
disagree, the skill says so instead of manufacturing differences, and when their
scopes aren't comparable (one covers 2025, one covers only Q1) it reports that
before comparing anything. The player is a single self-contained HTML file with two
routes: embedded neural-voice recordings (edge-tts mp3 — the default, identical on
every device) and the phone's built-in speechSynthesis voice as the fallback. The
fallback fails loudly, not weirdly: an absent Chinese voice produces an explanation
and a fix, never an English voice reading punctuation aloud.

## Field-tested

Wind-tunneled before release: 7 scenarios across 6 personas (dictated-Chinese
commuter, English requests, a written-summary decoy, a sibling-skill boundary,
an English-only stranger with a single-skill install, and a no-artifact host).
Score: 3 clean passes · 1 correct refusal · 2 degraded · 1 failure — the failure
(Chinese-default output reaching an English-only user invited in by the English
trigger phrases) was caught by the probe and fixed before this release: delivery
language now follows the requester's language.

> "呃把这两份就是那个市场报告哦,我下午开车去机场,路上听一下,重点是哪不一样"
> — dictated, noisy, goal buried at the end. Fired correctly; full recording-route
> player delivered.

> "这两份文档给我个书面 tl;dr,列成 bullet,我待会儿自己看" — correctly stayed
> silent. Written summaries belong to normal summarization; the NOT-clause held.

The plain-text degradation path (no HTML artifacts available) passed without
notes: the script is a first-class deliverable, not a fallback.

Probe method: [scenario-probe](../scenario-probe/)
