# ASR Correction Dictionary

> **Context guard**: Apply a mapping only when the input is dictated AND the mapping fits the sentence context; when the surrounding context is not marketing/platform talk, ask instead of fixing silently. Users add their own names/brands here — or better, in a personal dictionary at `~/.prompt-craft/asr-corrections.md`, which is merged on top of this file (user entries win) and survives package updates.

Fix silently, flag in the verification summary under "I guessed" (中文核对 → "我猜的").

## Platform / Tool Names

| ASR output | Correct | Notes |
|---|---|---|
| claude design, claude cold, clock cold | Claude Code | Common dictation error |
| ex, twitter ex, the X | X (Twitter) | Platform |
| tick talk, tick-tock, TicToc | TikTok | Platform |
| chrome extension, chrome plug-in | Chrome extension | Normalize casing |

## Domain Terms *(apply only when the audience/domain matches)*

*(Empty by design — your own domain shorthand goes here or in your personal dictionary. The previous owner's trading/web3 entries are kept only as commented-out examples of the format, e.g. `| see tee, CT | CT (Crypto Twitter) | trading context only |`, `| front running | front-running | hyphenate — trading context |`, `| cents, sense (in pricing context) | ¢ (cents) | prediction-market pricing: 58¢ → 67¢ |`, `| far caster, forecaster | Farcaster | web3 context only |`.)*

| ASR output | Correct | Notes |
|---|---|---|
| | | |

## Chinese Homophone Confusions

| ASR output | Likely meant | Context clue |
|---|---|---|
| 最后一针 | 最后一帧 (final frame) | Video/animation context |
| 最后一镜头 | 最后一镜 (final shot) | Video context |
| 一阵 (when counting) | 一帧 (one frame) | Video context |

## Person / Brand Names

*(Empty by design — your team members, product names, and reference-voice accounts go here or in your personal dictionary. Include the forms your dictation tool actually mishears, e.g. `| kay den, cade in | Kaiden | co-founder |`.)*

| ASR output | Correct | Notes |
|---|---|---|
| | | |

## General Rules

- Random capitalizations from ASR → normalize to standard casing
- Country name run-ons (西班牙法国英格兰阿根廷巴西) → separate: Spain / France / England / Argentina / Brazil
- Number strings without separators → add commas/structure

## Growing This Dictionary

When prompt-craft encounters a new ASR error:
1. Fix silently in the current prompt
2. Flag in the verification summary under "I guessed"
3. Suggest: "New ASR pattern: '<heard>' → '<corrected>'. Add to dictionary?"

If the user confirms: write the entry to `~/.prompt-craft/asr-corrections.md` when the filesystem is writable; otherwise output the table row as copyable text for the user to paste in themselves.
