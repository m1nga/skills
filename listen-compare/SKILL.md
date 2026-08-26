---
name: listen-compare
description: >-
  Turn documents the user has NO TIME TO READ into one Chinese briefing they can LISTEN to on a
  phone. For two or more documents it produces per-document key points plus a topic-by-topic
  comparison — what they agree on, where they differ, and whether each difference matters; for a
  single document, a listening version. The script is written for ears (short spoken sentences,
  conclusions first, no tables, bullets, or markdown) and delivered both as plain text — so any
  read-aloud feature can speak it — and, where HTML artifacts are available, as a tap-to-play
  player using the phone's built-in Chinese voice. Use whenever the user wants to HEAR content
  instead of reading it: 念给我听 / 读给我听 / 听一下这两份文档 / 我没时间看,讲给我听 / 开车路上听 /
  这两份报告有什么异同,说给我听 / listen to these docs / read this to me / audio briefing.
  NOT for written summaries the user will read with their eyes (just summarize normally),
  conversation recaps (use conclude-rounds if installed), podcast production, voice cloning,
  or transcribing audio to text.
---

# Listen-Compare

The user's eyes are busy; their ears are free. A summary written for eyes — tables,
bullets, precise decimals, nested parentheses — collapses when read aloud. This skill
produces the opposite artifact: a script that was *born* spoken, then hands it to
whatever voice is nearest (the phone's built-in TTS, a read-aloud feature, or a real
audio file).

The comparison is the point, not a bonus. Someone who asks to *listen* to two
documents is almost always asking one real question: **where do these two disagree,
and does it matter?** Answer that question first; the per-document recaps exist to
make the answer trustworthy.

## Step 1 — Get the documents

- Accept any mix: uploaded files, pasted text, file paths, links already fetched.
  PDF / Word / PPT: extract the text first with whatever the environment offers
  (dedicated pdf/docx skills, or plain reading).
- One document only → no comparison; the structure collapses to 开场 → 结论 →
  要点 → 收尾. Say so in one line, don't refuse.
- Three or more → same structure; the comparison stays organized **by topic**, never
  pairwise (pairwise explodes and is unlistenable).
- If a document can't be read (e.g. a scanned PDF with no OCR available), name which
  one and deliver the rest. Never silently drop a document.

## Step 2 — Write the 听稿 (the script)

**Before writing a word, read `references/spoken-chinese.md`.** It defines the
spoken register — 冒号句改"是"字句、每句有动词、自问自答带路、判词说白话 — with
before/after pairs. This skill's #1 field-observed failure is a script that is
structurally correct but written in report register (PPT 腔/公文腔/翻译腔); the
user hears it instantly and hates it. The reference ends with a mandatory
read-aloud self-check — do it before delivering.

### Structure — conclusions first, because listeners quit early

Use these section labels in this order. Each label becomes a tappable section in the
player, so keep them short.

1. **开场** (~20 秒) — 一句话说清今天听的是哪几份文档,各自一句话定位(谁写的、关于什么、立场是什么)。
2. **先说结论** (~40 秒) — 最大的共识一句话,最大的分歧一句话,以及"如果只记住一件事,记这个"。
3. **第一份:〈口语化的文档名〉** — 3 到 5 个要点,按重要性排,不按原文顺序。
4. **第二份:〈口语化的文档名〉** — 同上。刻意呼应第一份的维度,方便耳朵对齐。
5. **相同点** — 2 到 4 条,合并同类项,说"两份都认为……"。
6. **不同点** — 按问题维度组织,每条的句式是:"在〈什么问题〉上,第一份认为……,第二份认为……。这个分歧〈要紧/不要紧〉,因为……"。
7. **收尾** (~20 秒) — 一句话判决:两份合起来告诉你什么,或者下一步该做什么。

### Ear rules — what makes this different from a summary

- **每句话都要能读出来。** 没有表格、列表符号、markdown、括号堆叠、斜杠选项。写完在脑子里读一遍,读不顺就重写。
- **标点用全角**(,。;:),不用半角。半角标点落在英文语音手里会被念成 comma、semicolon。
- **路标句开路。** 段落之间用口语路标:"先说第一份"、"接下来是两份一致的地方"、"最大的分歧来了"。耳朵没有滚动条,路标就是滚动条。
- **数字口语化。** "31.4%" 默认说"大概三成";只有当精确值本身是重点时才读作"百分之三十一点四",而且一份听稿里这样的精确数字不超过三个。年份、金额同理取整。
- **英文术语先给中文。** 第一次出现时用"中文说法,也就是英文的 XXX",之后一律用中文。文档里的产品名、人名保留原文读音。
- **段落 ≤ 150 字**(约 45 秒),一段只讲一件事。
- **差异按问题组织,不按文档组织。** "A 说了 1234,B 说了 3456" 是清单;"在增长预期上 A 乐观 B 保守" 才是对比。
- **结论前置。** 每个要点先给判断,再给依据,永远不做悬念铺垫——听的人随时会被打断。

### Length and language

- 默认长度 **4–6 分钟**,约 1000–1400 字。用户说"短版"给 90 秒(~350 字);说"长版"或"每份展开讲"给 8–10 分钟。
- **默认中文输出**——当用户的请求本身是中文,或用户主动要求中文时(哪怕文档全是英文——这是这个 skill 存在的一半理由)。**用户的请求不是中文且未要求中文时,听稿与全部交付物跟随用户语言**,ear rules 不变;全角标点规则仅适用于中文稿,估时按非 CJK 语速调整。非中文听稿不走 device-TTS 播放器模板(其 UI 文案与选声逻辑为中文硬编码)——改走录音路线(用对应语言的系统人声)或纯文本;两者都做不到就明说,绝不把一份用户听不懂的稿子当成功交付。

### Honesty rules

- 文档没写的不编。两份口径不可比时明说(比如一份讲 2025 全年,一份只讲 Q1)。
- 两份其实没有实质分歧时,不要制造分歧——直接说"这两份基本是同一个结论,区别只在措辞/侧重",这本身就是重要结论。
- 数据打架时报告冲突本身("同一个指标,A 说三成,B 说五成,没法从文档内部判断谁对"),不替文档选边。

## Step 3 — Deliver

**Always** paste the full script as plain text in the reply, with the section labels
as plain lines (no markdown headers — the text itself may get read aloud verbatim).
Any built-in read-aloud can speak this directly. If the user seems to be on iPhone
and no player is possible, add one line: iOS 自带"朗读屏幕"(设置 → 辅助功能 →
朗读内容 → 朗读屏幕,两指从屏幕顶端下滑)可以直接读这段文字。

**If HTML artifacts are available** (Claude app, Claude Code with the Artifact
tool): also build the tap-to-play player. Read `references/player-template.html`,
replace `__TITLE__` with a short title and `__SECTIONS_JSON__` with a JSON array of
`{"label": "...", "text": "...", "audio": "..."}` in script order, and publish it.
Hand the user the link: 手机点开,按▶就能听。The `audio` field decides which of the
player's two routes runs, and they are not equals:

- **Recording route (default whenever you can synthesize NATURAL audio — e.g. macOS
  with shell access; robotic synths like espeak/festival do NOT count as "can
  synthesize" and fall through to device-TTS or plain text).** Generate one m4a per section and embed it as a `data:` URI in
  `audio`: `say -v Tingting -o s.aiff s.txt && afconvert s.aiff s.m4a -f m4af -d aac
  -b 48000` (prefer an Enhanced/Premium zh_CN voice over plain Tingting if
  `say -v '?'` lists one; never the novelty voices — Eddy, Flo, Grandma…). Base64
  adds ~33%; a 6-minute briefing lands around 4 MB, well under the 16 MB artifact
  cap — if you somehow exceed ~12 MB, lower the bitrate before dropping audio.
  Embedded recordings sound identical on every device, which is why this route
  wins whenever it's available.
- **Device-TTS route (fallback — no way to synthesize, e.g. running on the phone
  itself).** Omit `audio`; the player uses the phone's own Chinese voice. The
  template already guards the known failure: it waits for the async voice list,
  refuses to play with a clear message when the device has no Chinese voice
  (instead of letting an English voice read punctuation aloud), and flags
  suspiciously instant playback. Mention to the user that this version depends on
  their phone having a Chinese voice installed.

**If the user asks for a standalone audio file** (要 mp3 / 音频文件 / 存下来听):
concatenate the section m4a files (or synthesize once from the full script) and
send the .m4a itself in addition to the player.

## Not this skill's job

A written executive summary, podcast-style production (two hosts, jingles), voice
cloning, and audio transcription are all adjacent but different jobs — hand them
back to normal summarization or the right tool, in one line.
