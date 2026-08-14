# Common Marketing Prompt Failure Modes

25 failure modes that break marketing prompts. Each entry has:
- **Symptom**: what the bad output looks like
- **Root cause**: why the prompt let it happen
- **Fix pattern**: the prompt-level defense

`prompt-craft` DEEP Step D2 pulls from this list when enumerating failure modes for a given prompt type. Match the sub-domain (generic / copy / video / campaign / brand / content) detected in L1 to pull the right ones.

---

## §generic — applies to ANY marketing prompt

### generic-1: Output is so generic it could be for any brand in any category

- **Symptom**: "Discover our revolutionary new product that will transform your life! With cutting-edge innovation and unmatched quality, we are the perfect solution for modern consumers." You could swap the product, category, and audience, and nothing would change.
- **Root cause**: prompt didn't force the writer to ingest and use brand-specific constraints. No audience specificity. No proof points. No voice rules.
- **Fix pattern**: require `<brand_context>` block with 3+ concrete constraints. Require `<audience>` block with at least one non-demographic detail. Ban generic adjectives as a list.

### generic-2: Adjective stacking as a substitute for substance

- **Symptom**: "Beautiful, elegant, sophisticated, timeless, refined..." — a string of positive adjectives with no concrete claim behind any of them.
- **Root cause**: prompt asked for "persuasive copy" without forcing a single concrete claim or proof point.
- **Fix pattern**: require at least one `<concrete_claim>` element per section. Require each adjective to be followed by a supporting detail in parentheses. Ban standalone adjective lists longer than 3.

### generic-3: Vague "call to action" that doesn't actually call to any action

- **Symptom**: "Learn more" / "Click here" / "Contact us today" / "Discover more". Zero specificity. No first-person framing.
- **Root cause**: prompt said "include a CTA" without defining what makes a CTA work.
- **Fix pattern**: require CTA to be (a) first-person ("Get my free trial" not "Get your free trial" in some markets; the preference flips in others, e.g. Chinese-language markets — check the user context), (b) specific about what happens next, (c) low-friction language. Provide 3 good examples in the prompt.

### generic-4: Skipping the specified format / structure requirements

- **Symptom**: asked for "5 hooks, each under 12 words, with a reason why it works", got 3 hooks, some 20 words long, no explanations.
- **Root cause**: soft instruction without verification step. No execution discipline.
- **Fix pattern**: explicit numbered format with count verification in `<execution_discipline>`. Add "before delivering, count the items and verify each constraint is met — if not, regenerate the failing ones, do not submit partial."

### generic-5: "Handled that" fake completion

- **Symptom**: "I've incorporated your brand voice and audience specifics into the copy above." — but you read the copy and it did neither.
- **Root cause**: the prompt didn't force the writer to cite or quote the constraint when using it.
- **Fix pattern**: require `<verification>` block at the end of output where the writer lists which brand-voice rules and which audience traits were applied, with the specific line of copy that applies them.

---

## §copy — specific to copywriting prompts

### copy-1: Feature-dumping instead of benefit framing

- **Symptom**: "Contains 2% hyaluronic acid, ceramides, and vitamin B5. pH-balanced formula. Non-comedogenic." — all features, zero benefits.
- **Root cause**: prompt didn't require translation from feature → benefit → emotional payoff.
- **Fix pattern**: enforce the "so that" chain — every feature must be followed by "so that <benefit> so that <emotional payoff>". Give an example.

### copy-2: Headlines that are captions

- **Symptom**: "A great new product for everyone who cares about their skin" — neutral, no hook, no stop-scroll energy.
- **Root cause**: prompt asked for "a headline" without naming hook patterns or giving examples of strong ones.
- **Fix pattern**: provide 3+ headline formulas (see `copywriting.md §1`). Require the output to state which formula each headline uses.

### copy-3: Passive voice as default

- **Symptom**: "Results can be seen in 4 weeks." "Our ingredients are sourced from..."
- **Root cause**: prompt didn't ban passive or reward active voice.
- **Fix pattern**: ban passive voice explicitly with 3 concrete examples of passive → active rewrites in the prompt.

### copy-4: No stance / no point of view

- **Symptom**: balanced, reasonable, persuades no one. "Some people like X, others prefer Y, both have their merits."
- **Root cause**: prompt asked for "professional copy" which the writer interpreted as "safe and neutral".
- **Fix pattern**: require a `<stance>` block that explicitly states the one thing this piece is arguing. Require the copy to make that argument.

---

## §video — specific to video/script prompts

### video-1: No hook in the first 3 seconds

- **Symptom**: Script opens with "Hey guys, today I'm going to talk about..." — by then the viewer has scrolled.
- **Root cause**: prompt asked for "engaging video script" without specifying what must happen in the first 3 seconds.
- **Fix pattern**: require the script to state the hook type explicitly in the first beat (pattern interrupt / shocking stat / contrarian claim / visual hook / question). Reject any opening that takes >2 seconds to deliver the hook.

### video-2: Wrong pacing for platform

- **Symptom**: a 60-second TikTok script with 2 scene changes. Dead.
- **Root cause**: prompt didn't specify target platform's pacing norm.
- **Fix pattern**: load `video.md §4` and inject platform-specific cut cadence into the prompt (TikTok/Reels: cut every 1-3s; YouTube Shorts: 1-3s; YouTube long: 3-8s).

### video-3: No visual cues in the script

- **Symptom**: script is pure voiceover with no indication of what's on screen. The video team has to guess.
- **Root cause**: prompt asked for "a script" without specifying the shot/B-roll column.
- **Fix pattern**: require a 2-column format: LEFT = visual/action; RIGHT = voiceover/text. Provide an example row.

### video-4: CTA stapled onto the end

- **Symptom**: a great video about the problem, then "follow us for more" tacked on with no connective tissue.
- **Root cause**: CTA wasn't designed into the arc.
- **Fix pattern**: require the CTA to be foreshadowed earlier in the script. Add a check: "Does the CTA feel earned by the preceding 10 seconds? If no, rewrite."

### video-5: Talking-head without a reason

- **Symptom**: script is an expert talking to camera about a topic, with no hook, no narrative, no visual interest.
- **Root cause**: prompt treated script as a speech.
- **Fix pattern**: require one of: demonstration, transformation, reveal, or story arc. Pure talking-head allowed only if the speaker has high face value and the prompt explicitly calls for it.

---

## §campaign — specific to campaign planning / ad strategy prompts

### campaign-1: Creative that doesn't match the funnel stage

- **Symptom**: a "buy now 30% off" ad served as cold traffic / TOFU. Or a general awareness hook served to people already in cart.
- **Root cause**: prompt didn't specify funnel stage + creative type matching.
- **Fix pattern**: require the output to declare funnel stage (awareness / consideration / conversion / retention) and use creative type appropriate for that stage (see `campaigns.md §2`).

### campaign-2: One-size-fits-all creative across audiences

- **Symptom**: same ad for cold, warm, and hot audiences.
- **Root cause**: prompt treated "the campaign" as a single asset.
- **Fix pattern**: require 3 creative variants (cold / warm / hot) with explicit differences. Each variant cites what changed and why.

### campaign-3: No measurement / optimization plan

- **Symptom**: creative delivered with no KPI, no test hypothesis, no iteration plan.
- **Root cause**: prompt was framed as "creative brief" not "campaign brief".
- **Fix pattern**: add a mandatory `<measurement>` block: primary KPI + secondary KPIs + test hypothesis + optimization trigger.

### campaign-4: Platform-agnostic creative

- **Symptom**: same caption, same length, same aspect ratio for every platform.
- **Root cause**: prompt didn't require platform-native adaptation.
- **Fix pattern**: force per-platform variants with the specs from `platforms.md`. Each platform gets its own section in the output.

---

## §brand — specific to brand voice / positioning prompts

### brand-1: Tone words that mean nothing

- **Symptom**: "Our brand voice is friendly, professional, and trustworthy." — every brand says this.
- **Root cause**: prompt asked for tone words without asking for operational rules.
- **Fix pattern**: reject bare tone words. Require each tone word to be followed by 2 do-this / 2 don't-do-this examples that are executable by a copywriter.

### brand-2: Inconsistent voice across assets

- **Symptom**: Instagram is playful, LinkedIn is corporate, the website is formal. No thread connecting them.
- **Root cause**: prompt wrote voice per-platform without a north-star archetype.
- **Fix pattern**: require a single archetype (see `brand-voice.md §1`) from which platform variations flex. Output must show how each variation maps back.

### brand-3: Cliché metaphors as substance

- **Symptom**: "Our journey" / "We're family" / "Game-changer" / "Disruptor".
- **Root cause**: prompt didn't ban overused brand metaphors.
- **Fix pattern**: ban list in the prompt. Force original metaphors grounded in the product category.

### brand-4: Archetype mismatch with audience

- **Symptom**: Luxury skincare with Outlaw archetype targeting conservative middle-age women. Dissonance.
- **Root cause**: prompt didn't cross-check archetype vs audience.
- **Fix pattern**: require the prompt to justify the archetype choice against the audience from the user context.

---

## §content — specific to content marketing / long-form

### content-1: No point of view

- **Symptom**: "10 things to consider when choosing X" — balanced listicle, no argument, no reason to read this version over the 50 others.
- **Root cause**: prompt asked for "informative content" which defaulted to neutral.
- **Fix pattern**: require a thesis in the first 100 words. The thesis must be arguable, not consensus.

### content-2: SEO keyword stuffing that breaks the read

- **Symptom**: "best skincare routine skincare routine for oily skin skincare tips"
- **Root cause**: prompt treated SEO and readability as separate concerns.
- **Fix pattern**: target keyword density ≤1%. Require the keyword to appear naturally (and only if it appears naturally — otherwise don't force it).

### content-3: Generic opener

- **Symptom**: "In today's fast-paced world..." / "Have you ever wondered..."
- **Root cause**: no ban list, no better example.
- **Fix pattern**: ban list + require opener to either (a) make a specific claim, (b) tell a specific story, or (c) present a specific problem.

---

## How `prompt-craft` uses this file

In DEEP Step D2 (enumerate failure modes), after the user states the worst failure they're worried about, `prompt-craft` should:

1. Identify the sub-domain(s) from the L1 parse.
2. Pull 2–4 additional failure modes from the matching sections above.
3. Bind each pulled failure to a planned defense in the D3 draft.
4. Cite the failure mode ID in rationale: "Addresses video-1 (no hook in first 3 seconds) via `<hook>` block on line 3."

Never silently apply these. Always name them in the D2 failure list so the user can see the contract.
