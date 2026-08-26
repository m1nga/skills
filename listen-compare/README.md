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
available you also get a tap-to-play player that uses your phone's own Chinese
voice — per-section play, 连播, speed control, no network, no account. On a Mac it
can also render a real .m4a file on request.

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
before comparing anything. The player is a single self-contained HTML file driving
the phone's built-in speechSynthesis voice — chosen over generated audio because it
needs no server, no file transfer, and no cloud TTS account.
