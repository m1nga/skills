# Video Reference

Production knowledge for video scripts, from 15-second TikToks to 20-minute YouTube deep-dives. `prompt-craft` loads this when drafting video-related prompts.

> Retention and platform figures below are directional heuristics drawn from platform-reported patterns — treat them as design guidance, not citations. Brand examples are fictional ("Meridian", "Openbook", "Tally").

---

## §1 The 3-Second Rule

**The first 3 seconds determine whether anyone watches the rest.** This is not a guideline — it's physics. Platform data consistently shows:

- TikTok: viewers who make it past 3 seconds mostly watch to the end
- Instagram Reels: similar pattern, slightly more forgiving (4 seconds)
- YouTube Shorts: swipe-away decision made in 1-3 seconds
- YouTube long-form: first 30 seconds = the real hook (but first 5 seconds determines skip vs watch on pre-roll ads)

### What must happen in the first 3 seconds

One of these — not "building up to" one of these:

1. **Visual pattern interrupt**: something visually unexpected (fast zoom, unusual angle, color flash, unexpected object)
2. **Verbal hook**: a complete, provocative statement (not "Hey guys, today we're going to...")
3. **Text-on-screen hook**: bold text with a hook line (works even sound-off)
4. **Action in progress**: start mid-action, not at the beginning of the action
5. **Data flash**: a number that surprises (works especially well for data-driven content)

### What kills the first 3 seconds

- Logo animation / brand intro
- "Hey guys, welcome to my channel"
- Slow fade-in from black
- Setting the scene before the hook
- Any sentence that starts with "So" or "Today"

### Prompt rule

Every video prompt must specify what happens in the first 3 seconds. If the script doesn't have a defined hook for the opening, `prompt-craft` should flag it as a failure risk and require it.

---

## §2 Retention Curves

### The universal retention shape

All video platforms share a similar retention pattern:

```
100% ─┐
      │╲
      │  ╲
      │    ╲─── rapid drop (first 15-30% of video)
      │      ╲
      │        ────────── plateau (middle 40-60%)
      │                  ╲
      │                    ╲── gradual decline (final 20-30%)
      │                      ╲
  0%  └──────────────────────────
      0s                    end
```

### Retention benchmarks by platform *(directional)*

| Platform | Good avg retention | Great avg retention | Where viewers drop |
|---|---|---|---|
| TikTok (15-30s) | 60% | 80%+ | First 2-3 seconds |
| TikTok (60s) | 40% | 55%+ | First 3 seconds, again at 30s |
| IG Reels (30s) | 50% | 70%+ | First 3-4 seconds |
| YouTube Shorts | 55% | 75%+ | First 2 seconds (swipe) |
| YouTube (10min) | 40% | 55%+ | 30-second mark, 2-minute mark |
| YouTube (20min) | 35% | 50%+ | Every 3-5 minutes without payoff |

### Retention killers (ranked by severity)

1. **No hook** — immediate drop at 0-3 seconds
2. **No payoff after setup** — drop at 15-30 second mark
3. **Pacing plateau** — drop when visual rhythm stays static for >8 seconds
4. **Promised content not delivered** — drop when viewer realizes the title/hook was bait
5. **Recap/summary too long** — drop at end when content repeats itself
6. **Single visual for too long** — drop after 5-8 seconds of same shot (short-form) or 15-20 seconds (long-form)

### Retention boosters

1. **Pattern interrupts** at predicted drop points (zoom, cut, text, sound change)
2. **Open loops** ("but first..." / "we'll get to that in a second...")
3. **Progress indicators** ("Step 2 of 5" / numbered structure)
4. **Curiosity gaps** held across sections
5. **Payoff density** — reward attention frequently, not just at the end

---

## §3 Script Structures

### Structure 1: Hook → Problem → Solution → CTA (15-30s)

**Best for**: product demos, ads, quick tips

```
[0-3s]   HOOK: pattern interrupt or shocking stat
[3-10s]  PROBLEM: name the pain quickly, specifically
[10-20s] SOLUTION: show the product solving it (visual proof preferred)
[20-30s] CTA: one specific action
```

**Example (fictional Meridian, 30s)**:
- [0-3s] TEXT: "Openbook 71¢. Tally 65¢. Same market."
- [3-10s] "By the time you find this in your feed, someone's already arbing it."
- [10-22s] SCREEN RECORDING: the extension showing the arb alert in real-time
- [22-30s] TEXT: "Free extension. Link in bio."

### Structure 2: Story Arc (30-90s)

**Best for**: narrative content, testimonials, case studies

```
[0-3s]   HOOK: in medias res or shocking outcome
[3-15s]  SETUP: character + situation (brief)
[15-40s] CONFRONTATION: obstacle, struggle, turning point
[40-60s] RESOLUTION: transformation, outcome, proof
[60-90s] REFLECTION + CTA: lesson learned + what to do
```

### Structure 3: List / Countdown (30-60s)

**Best for**: educational content, tips, rankings

```
[0-3s]   HOOK: "N things that..." with strongest teased
[3-10s]  ITEM 1 (weakest — save best for last)
[10-20s] ITEM 2
[20-30s] ITEM 3
[30-45s] ITEM N (strongest — reward for watching)
[45-60s] CTA or bonus item
```

**Rule**: reverse order — weakest first, strongest last. Viewers who make it to the end are the most engaged; reward them.

### Structure 4: Tutorial / How-To (60s-10min)

**Best for**: educational content, product walkthroughs

```
[0-5s]    HOOK: show the end result FIRST
[5-15s]   CONTEXT: why this matters (brief)
[15-80%]  STEPS: numbered, each with clear visual
[80-90%]  RESULT: show the outcome again
[90-100%] CTA: what to do next
```

**Rule**: show the end result before the process. If viewers don't want the outcome, they won't watch the process.

### Structure 5: Reaction / Commentary (15-60s)

**Best for**: trending topic responses, quote-tweet video, duet/stitch

```
[0-3s]   HOOK: show the thing being reacted to
[3-20s]  REACTION: hot take, analysis, disagreement
[20-40s] EVIDENCE: why your reaction is right
[40-60s] PUNCHLINE: one-line landing
```

---

## §4 Pacing by Platform

### Cut cadence (visual changes per unit time)

| Platform | Min cuts per minute | Sweet spot | Too fast | Too slow |
|---|---|---|---|---|
| TikTok | 20 | 25-40 | >50 (disorienting) | <15 (boring) |
| IG Reels | 15 | 20-35 | >45 | <12 |
| YouTube Shorts | 15 | 20-35 | >45 | <12 |
| YouTube (long) | 8 | 10-20 | >30 (exhausting) | <6 (static) |
| LinkedIn Video | 5 | 8-15 | >20 | <4 |

### What counts as a "cut"

- Camera angle change
- Zoom in/out
- B-roll insert
- Text overlay appearing/changing
- Screen recording transition
- Animation/motion graphic
- Color/filter change
- Split-screen change

### Pacing rules

1. **Never hold a single visual for more than**: 3s (TikTok), 4s (Reels/Shorts), 8s (YouTube long), 10s (LinkedIn)
2. **Pattern interrupt at predicted drop points**: hook at 0s, interrupt at 15s, interrupt at 30s, interrupt at 60s
3. **Speed up at the end**: final 20% of video should have 20-30% faster pacing than the middle
4. **Match audio to cuts**: music beat drops and visual cuts should align

---

## §5 Visual Cues

### Text-on-screen rules

- **Size**: readable on mobile without squinting. Minimum 48pt equivalent.
- **Duration**: 2-4 seconds per text card. Longer = viewer reads and waits (bored). Shorter = can't read (frustrated).
- **Position**: center or lower-third. Never near platform UI elements (like/comment buttons, captions).
- **Font**: sans-serif, bold weight, high contrast against background. Drop shadow or background box for readability.
- **Amount**: max 8-10 words per text card. If more, split into multiple cards.
- **Animation**: simple entrance (fade, slide, pop). No spinning, bouncing, or complex transitions — they look amateur.

### Color and contrast

- High contrast between subject and background
- Consistent color palette across the video (builds visual identity)
- Use color to draw attention: highlight key text in brand color
- Dark mode friendly: many viewers watch in dark mode or at night

### B-roll and visual proof

- Screen recordings for software/app demos (with cursor highlight or zoom)
- Screenshots with annotation (circle, arrow, highlight) for proof/receipts
- Data visualization for numbers (simple charts, counters, comparisons)
- Face on camera builds trust (but not required for brand accounts)

---

## §6 Sound Design

### Music selection

- **Trending sounds** (TikTok/Reels): use even 1-2 seconds for algorithmic boost
- **Background music**: match energy to content tone. Upbeat for excitement, lo-fi for analysis, ambient for professional.
- **Volume levels**: music at 20-30% when voice is present, 80-100% for transitions/intros
- **Licensed music**: use platform music libraries to avoid copyright strikes

### Voiceover rules

- **Pace**: 130-160 words per minute (natural speaking pace). Faster for short-form energy, slower for authority.
- **Tone**: match brand voice axes (formality, energy, humor, warmth)
- **Quality**: clean audio is non-negotiable. Background noise = amateur.
- **AI voice**: acceptable for brand accounts, but flag the choice — human voice builds more trust.

### Sound effects

- Use sparingly for emphasis (notification ding, whoosh for transition, pop for text appearance)
- Never more than 3 SFX types in a single video
- SFX should feel invisible — if the viewer notices the SFX, it's too much

### Silence

- Strategic silence (0.5-1s) before a key point creates emphasis
- Works especially well in long-form content to signal "this next part matters"
- Never use silence in the first 5 seconds of short-form (reads as dead content)

---

## §7 Common Video Failure Modes

### Failure 1: Script is a monologue with no visual direction

- **Symptom**: 500 words of voiceover, zero indication of what's on screen
- **Fix**: require 2-column format (VISUAL | AUDIO) in every video prompt
- **Cited in**: `common-failures.md §video-3`

### Failure 2: No hook — opens with greeting or branding

- **Symptom**: "Hey everyone, welcome back to..." — most viewers gone in the first 3 seconds
- **Fix**: specify hook type and content in first beat of script
- **Cited in**: `common-failures.md §video-1`

### Failure 3: Pacing doesn't match platform

- **Symptom**: 60-second TikTok with 2 scene changes (should have 25-40)
- **Fix**: inject platform pacing requirements from §4 above
- **Cited in**: `common-failures.md §video-2`

### Failure 4: No retention plan

- **Symptom**: viewer interest drops linearly — nothing keeps them watching
- **Fix**: require pattern interrupts at predicted drop points (15s, 30s, 60s)
- **Defense**: open loops, numbered structure, payoff promises

### Failure 5: CTA is an afterthought

- **Symptom**: great content → "follow for more" slapped on the end
- **Fix**: CTA must be foreshadowed earlier; the video must earn the right to ask
- **Cited in**: `common-failures.md §video-4`

### Failure 6: Talking head without visual variety

- **Symptom**: same camera angle, same framing, for 60+ seconds
- **Fix**: require one of: B-roll, screen recording, text overlay, zoom variation
- **Cited in**: `common-failures.md §video-5`

### Failure 7: Sound-off incompatible

- **Symptom**: video relies entirely on voiceover for information — muted viewers learn nothing
- **Fix**: require text-on-screen that carries the core message independently of audio

---

## How `prompt-craft` uses this file

1. **Any video prompt**: load this file + `platforms.md` for the target platform.
2. **Script structure**: recommend structure from §3 based on length and purpose.
3. **Pacing constraints**: inject platform-specific cut cadence from §4.
4. **Hook specification**: require hook type and content from §1 in every script's first beat.
5. **2-column format**: require VISUAL | AUDIO columns for any script longer than 15 seconds.
6. **Failure defense**: cross-reference §7 with `common-failures.md §video` section.
7. **In rationale**: cite specific rules: "video.md §3-sec rule — hook specified as data flash."
