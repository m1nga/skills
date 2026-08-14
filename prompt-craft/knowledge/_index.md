# Knowledge Base Index

This directory holds the domain knowledge `prompt-craft` loads when drafting prompts. Claude reads this index first, then pulls files based on the detected sub-domain.

## Load order (always)

1. **User brand context** — brand/audience/tone context. **ALWAYS load first** for any marketing-domain prompt. Non-negotiable. Lookup order: `~/.prompt-craft/user-context.md` → `knowledge/user-context.md` (legacy in-package) → `knowledge/user-context.example.md` (template; triggers generic mode + a one-time setup notice). Check the file's `Status` date — time-scoped facts older than 60 days are stale and must not be injected.
2. **`asr-corrections.md`** — voice transcription error dictionary (plus the user's personal dictionary at `~/.prompt-craft/asr-corrections.md`, merged on top). **Load when input looks voice-dictated** (filler words, broken grammar, run-on structure, mixed-language input). Lightweight file, low cost to load.

## Load on demand

Select 2–3 based on detected sub-domain. Do not load everything — it wastes context.

| File | Contents | Load when |
|---|---|---|
| **`frameworks.md`** | AIDA, PAS, BAB, FAB, StoryBrand, JTBD, 4Ps, AARRR, Hook-Story-Offer, 3-act video | ads, copy, brand, campaign, content |
| **`platforms.md`** | Specs + algorithm notes + native conventions for TikTok, IG Reels, YouTube Shorts, YouTube long-form, LinkedIn, Meta Ads, Google Ads, Twitter/X, Email (as-of dated — verify before high-stakes use) | ads, video, content, campaign |
| **`brand-voice.md`** | 12 Jungian archetypes, tone-ladder (4 axes), do/don't patterns, brand-voice failures | brand, content, copy (tone concerns) |
| **`copywriting.md`** | 16 headline formulas, 12 hook patterns, 8 CTA patterns, 10 mini-rules | copy, content, ads, video (hook + CTA) |
| **`video.md`** | 3-second rule, retention curves, 5 script structures, pacing, visual cues, sound design | video |
| **`campaigns.md`** | Funnel stages, creative matching, retargeting, multi-touch, budget heuristics, benchmarks | ads, campaign, content |
| **`common-failures.md`** | 25 marketing prompt failure modes (generic / copy / video / campaign / brand / content) | always, for any marketing prompt |

## Typical load bundles

- **"Write a TikTok ad"** → user context + `asr-corrections.md` + `video.md` + `platforms.md` + `copywriting.md`
- **"Write Meta Ads campaign brief"** → user context + `campaigns.md` + `platforms.md` + `common-failures.md`
- **"Define brand voice"** → user context + `brand-voice.md` + `frameworks.md`
- **"Write landing page copy"** → user context + `copywriting.md` + `frameworks.md` + `common-failures.md`
- **"Write email sequence"** → user context + `copywriting.md` + `campaigns.md` + `platforms.md`
- **Voice-dictated anything** → add `asr-corrections.md` to the bundle

## Expansion

To add a domain (SEO, PR, EDM, influencer brief), create a new topic file + add a row above. Keep each file under 600 lines.

## Citation format

When a prompt design decision is grounded in a knowledge file, cite as: `file.md §section`

- `video.md §3-sec rule`
- `common-failures.md §video-2 "no pattern interrupt"`
- `copywriting.md §CTA patterns — first person`
- `user-context §Brand voice — don't`
- `asr-corrections.md §Chinese homophone` *(for ASR correction rationale)*
