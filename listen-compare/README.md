# listen-compare

**Turn documents you have no time to read into a Chinese briefing you can listen to — with the disagreements surfaced first.**

## What it does

Someone who asks to *listen* to two documents is really asking one question: where
do these disagree, and does it matter? This skill answers that question in a form
built for ears, not eyes. It reads your documents (PDF, Word, pasted text — any
mix), then writes a spoken-style Chinese script: conclusions first, then each
document's key points, then what they agree on, then the differences organized by
topic — each one tagged 要紧 or 不要紧.

The script obeys ear rules a written summary ignores: no tables or bullets, spoken
signposts between sections, numbers rounded to what a listener can hold ("大概三成"
not "31.4%"), English terms glossed in Chinese on first use, every paragraph under
45 seconds.

Delivery is deliberately low-tech so it works anywhere: the full script lands as
plain text (any read-aloud feature can speak it), and where HTML artifacts are
available you also get a tap-to-play player — per-section play, 连播, speed
control, no network, no account. When the briefing is generated on a Mac, the
player ships with real embedded recordings (identical on every device); generated
on the phone itself, it falls back to the phone's own Chinese voice, and refuses
with a clear message if no Chinese voice is installed.

## When it fires

- "这两份分析我没时间看,念给我听,告诉我异同。"
- "开车路上想听一下这两份报告的区别。"
- "Read these two PDFs to me and tell me where they disagree."
- "我只能听不能看,把这份文档讲给我听。" (single doc — skips the comparison)

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
routes: embedded m4a recordings when the briefing was made somewhere that can
synthesize speech (the default — device-independent), and the phone's built-in
speechSynthesis voice otherwise. The fallback fails loudly, not weirdly: an absent
Chinese voice produces an explanation and a fix, never an English voice reading
punctuation aloud.

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
