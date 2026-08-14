# Platform Reference

Specs, algorithm notes, native conventions, common failures, and prompt constraints for each major platform. `prompt-craft` loads this when drafting platform-specific content.

> **Freshness**: every section carries an as-of date. Platform specs and algorithm behavior drift constantly — treat dated notes as a starting point and verify before high-stakes use (paid campaigns, client deliverables). When prompt-craft injects a constraint from a section older than ~a year, it should flag it as "verify current".

---

## §TikTok

*As of 2026-04.*

### Specs

- **Video length**: 15s, 30s, 60s, 3min, 10min. Sweet spot for ads: 21-34s. Sweet spot for organic: 30-60s.
- **Aspect ratio**: 9:16 (1080×1920). Full-screen vertical only.
- **Text safe zone**: keep text within center 80% — top/bottom 10% obscured by UI.
- **Caption length**: 150 chars visible without "more"; max 2200 chars.
- **Hashtags**: 3-5 relevant. Mix broad (#fyp) with niche. Over-hashtagging penalized.
- **Sound**: a discovery vector — trending audio boosts distribution. But always design text-on-screen to carry the core message sound-off; a meaningful share of viewers watch muted.
- **Upload**: native upload preferred. Third-party watermarks (IG Reels logo) suppressed by algorithm.

### Algorithm notes

- **Initial distribution**: pushed to a small For You Page test batch. Performance in first 1-2 hours determines next push.
- **Key signals (ranked)**: completion rate > rewatch rate > share > comment > like > follow.
- **Completion rate is king**. A 15s video watched fully beats a 60s video watched 50%. Design for full watch-through.
- **Loop content**: videos that seamlessly loop trick the algorithm into counting multiple views. Effective but don't overuse.
- **Posting frequency**: 1-3x/day for growth phase. Consistency > volume.
- **Best posting times (US)**: Tue-Thu 10am-12pm, 7-9pm EST. Test and adjust.

### Native conventions

- No polish. Raw > produced. Phone-shot aesthetic wins.
- Text-on-screen as primary information delivery.
- Green screen format for commentary/reaction.
- Trending sounds as distribution hooks — even 1-2 seconds of a trending sound helps.
- Stitch and Duet as engagement formats — react to others' content.
- "Part 1, Part 2..." series format for retention.
- POV format for storytelling.

### Common failures

- Over-produced brand video (instant scroll — looks like an ad)
- No hook in first 1-2 seconds (dead on arrival)
- Landscape or square video (doesn't fill screen, amateur)
- Ignoring sound design (loses the trending-audio discovery vector)
- Posting once a week expecting growth (algorithm rewards frequency)

### Prompt constraints to inject

```xml
<platform_constraints platform="tiktok">
- Video length: [15s|30s|60s] — specify in prompt
- Aspect ratio: 9:16 vertical (1080×1920)
- Hook must land in first 1-2 seconds — state the hook type
- Script must include text-on-screen callouts (not just voiceover)
- Sound direction required: trending sound / original audio / voiceover / music
- Message must survive sound-off viewing (text carries the core)
- Raw aesthetic preferred over polished production
- Design for completion rate: every second must earn the next second
- Caption: ≤150 chars for visible portion
</platform_constraints>
```

---

## §Instagram Reels

*As of 2026-04.*

### Specs

- **Video length**: 15s, 30s, 60s, 90s. Sweet spot: 15-30s for reach, 60-90s for depth.
- **Aspect ratio**: 9:16 (1080×1920). Can post 4:5 but 9:16 gets more distribution.
- **Caption length**: 2200 chars. First 125 chars visible without "more".
- **Hashtags**: 3-5 in caption. Keyword-rich caption > hashtag spam (2024+ algorithm shift).
- **Cover image**: custom cover matters for profile grid aesthetic.
- **Audio**: original audio or IG music library. Trending audio boosts reach.

### Algorithm notes

- **Reels distribution**: Explore page + Reels tab + home feed. Reels are IG's primary growth vector.
- **Key signals**: shares (DM shares especially) > saves > comments > likes > follows.
- **Shares are the new likes**. Content that people send to friends in DMs gets a large algorithmic boost (2024+ shift).
- **Consistency**: 3-5 Reels/week for growth. Daily posting helps but quality > quantity.
- **Cross-posting from TikTok**: remove the watermark or IG suppresses distribution — export a clean, watermark-free copy from your original editor rather than ripping the posted version.
- **SEO matters**: IG indexes captions and on-screen text for search. Keyword-optimize.

### Native conventions

- Slightly more polished than TikTok but still authentic.
- Carousel posts for information-dense content (10 slides max, 1080×1350 for feed).
- Stories for ephemeral engagement (polls, questions, behind-scenes).
- Collab posts for cross-audience reach.
- Caption as micro-blog format (especially for business/educational content).
- Aesthetic grid still matters for profile visitors deciding whether to follow.

### Common failures

- TikTok watermark on Reels (algorithm punishment)
- Ignoring Reels for static posts only (missing primary distribution channel)
- Over-polished brand content that doesn't match platform vibe
- No call-to-action in caption (save this / share with someone who...)
- Hashtag spamming (30 hashtags era is over)

### Prompt constraints to inject

```xml
<platform_constraints platform="instagram_reels">
- Video length: [15s|30s|60s|90s] — specify
- Aspect ratio: 9:16 vertical
- Hook in first 1-2 seconds
- Include save/share trigger in caption
- Caption: front-load first 125 chars (visible portion)
- Audio direction: trending audio / original / voiceover
- Design for share-worthiness (DM shares = #1 signal)
- Cover image direction if profile grid matters
</platform_constraints>
```

---

## §YouTube Shorts

*As of 2026-04.*

### Specs

- **Video length**: ≤60 seconds. Sweet spot: 30-58s.
- **Aspect ratio**: 9:16 (1080×1920).
- **Title**: ≤100 chars. Appears below the video.
- **Description**: standard YouTube description. Less visible on Shorts but helps SEO.
- **No custom thumbnail** for Shorts (unlike long-form). First frame matters.

### Algorithm notes

- **Distribution**: Shorts shelf on mobile, Shorts tab, home feed.
- **Key signals**: swipe-away rate (inverse of completion) is #1. Low swipe-away = more push.
- **Subscribe button**: Shorts are YouTube's top new-subscriber driver. Massive for channel growth.
- **Monetization**: Shorts ad-revenue sharing (the earlier Shorts Fund was discontinued and replaced by revenue sharing in 2023).
- **Long-form bridge**: Shorts viewers convert to long-form subscribers at a higher rate than cross-platform traffic.
- **Frequency**: daily posting helps discovery. 1-2/day during growth phase.

### Native conventions

- Commentary/reaction format popular.
- "Did you know" educational hook.
- Numbered lists ("3 things about...").
- Clip-from-long-form as Shorts (works extremely well for channels with existing long content).
- Less trend-dependent than TikTok. Evergreen content performs longer.

### Common failures

- Vertical video over 60s (won't register as Short)
- No hook — YouTube Shorts swipe-away is instant and unforgiving
- Ignoring the title field (it's indexed for search)
- Not pinning a comment with CTA
- Treating Shorts as throwaway instead of subscriber pipeline

### Prompt constraints to inject

```xml
<platform_constraints platform="youtube_shorts">
- Video length: ≤60s, aim for 30-58s
- Aspect ratio: 9:16
- Hook in first 1-2 seconds — swipe-away rate is primary signal
- Title: keyword-optimized, ≤100 chars
- Pinned comment CTA planned
- Design as subscriber pipeline to long-form (if applicable)
- First frame = thumbnail — make it count
</platform_constraints>
```

---

## §YouTube Long-form

*As of 2026-04.*

### Specs

- **Video length**: 8-20 min sweet spot for ad revenue. 10+ min enables mid-roll ads.
- **Aspect ratio**: 16:9 (1920×1080) standard. 4K increasingly expected.
- **Thumbnail**: custom, 1280×720, <2MB. THE most important asset for CTR.
- **Title**: ≤70 chars visible. ≤100 chars total.
- **Description**: first 2 lines visible without expand. Front-load keywords and CTA.
- **Tags**: less important than title/description/thumbnail but still index.
- **End screens**: last 20 seconds for subscribe + next video cards.
- **Cards**: up to 5 per video for internal linking.

### Algorithm notes

- **Key signals**: CTR (thumbnail + title) × average view duration = the formula.
- **CTR benchmark**: 4-10% for most channels. Below 4% = thumbnail/title problem.
- **Retention**: aim for 50%+ average view duration. 40% is acceptable for 20+ min videos.
- **Session time**: YouTube rewards videos that keep people on the platform. End screens and playlists help.
- **Upload consistency**: weekly minimum. Same day/time builds audience habit.
- **First 48 hours**: critical push window. Promote across channels immediately.

### Native conventions

- Thumbnail: high contrast, large face (if personality-driven), max 3-4 words text, curiosity gap.
- Cold open (no intro bumper) — first 30s is the real hook.
- Pattern interrupt every 3-8 seconds in the visual (cut, zoom, B-roll, text overlay).
- Chapters (timestamps in description or via YouTube's chapter feature).
- Community tab for audience interaction and content teasing.
- Shorts as top-of-funnel → long-form as conversion.

### Common failures

- Boring thumbnail (stock photo, small text, no face, no contrast)
- 30-second branded intro before the content starts (kills retention)
- No pattern interrupts in the first 2 minutes (audience drops off)
- Ignoring retention analytics (not adjusting based on where viewers drop)
- No end screen / cards (leaving subscribers on the table)

### Prompt constraints to inject

```xml
<platform_constraints platform="youtube_longform">
- Video length: [target minutes] — specify
- Cold open: first 30s must hook. No intro bumper.
- Thumbnail concept required alongside script
- Title: curiosity gap + keyword, ≤70 visible chars
- Pattern interrupt every 3-8 seconds in visual direction
- Retention checkpoints: what keeps viewer at 30s? 2min? midpoint?
- End screen plan: what video next? Subscribe CTA?
- Chapter timestamps planned
</platform_constraints>
```

---

## §LinkedIn

*As of 2026-04.*

### Specs

- **Post length**: 3000 chars max. First 140 chars visible before "see more".
- **Image**: 1200×627 (landscape) or 1080×1080 (square). Square gets more feed real estate.
- **Video**: native upload, ≤10 min. Vertical or square. Subtitles mandatory (most watch muted).
- **Document/carousel**: PDF upload, up to 300 pages. 1080×1080 or 1080×1350 per page.
- **Newsletter**: long-form publishing to subscribers. Notifies all followers on publish.

### Algorithm notes

- **Dwell time**: how long someone spends reading your post is the #1 signal (2024+).
- **Comments > reactions**. A comment is worth roughly an order of magnitude more than a like in algorithm weight.
- **First hour**: performance in first 60 minutes determines distribution curve.
- **External links penalized**: link in comments or use built-in features instead.
- **Engagement pods** are detected and penalized. Organic comments from your network matter most.
- **Posting frequency**: 3-5x/week. Over-posting (2+/day) can dilute each post's reach.

### Native conventions

- "Hook line + line breaks" format. First line is the headline.
- Personal storytelling outperforms corporate content massively.
- Document carousels for frameworks, how-tos, lists (highest save rate format).
- Tagging people in context (not spam-tagging for reach).
- Polls for engagement (but low-value engagement — use sparingly).
- "I [verbed] something and learned..." narrative format.

### Common failures

- External link in the post body (algorithm buries it)
- Corporate-speak on a personal platform (LinkedIn rewards human, not brand)
- Wall of text with no line breaks (no one reads it)
- No hook in first line (the "see more" click never happens)
- Treating LinkedIn like Twitter (different pacing, different audience expectations)

### Prompt constraints to inject

```xml
<platform_constraints platform="linkedin">
- First line: hook that earns the "see more" click
- Line breaks: single idea per line, generous white space
- No external links in post body — link in first comment
- Design for dwell time: make them read slowly
- Subtitles mandatory for any video
- Document carousel if information-dense
- Personal voice > corporate voice (even for brand accounts)
</platform_constraints>
```

---

## §Meta Ads (Facebook + Instagram)

*As of 2026-04.*

### Specs

- **Image**: 1080×1080 (feed), 1080×1920 (stories/reels). Note: the old "max 20% text on image" rule was retired by Meta in 2021 — text-heavy images are no longer rejected or throttled at review, though low-text creative still tends to perform better.
- **Video**: ≤240 min. Recommended: 15-30s for feed, 5-15s for stories.
- **Primary text**: 125 chars visible (feed). Full text requires "see more".
- **Headline**: 40 chars (link ads). Appears below image.
- **Description**: 30 chars (link ads). Below headline.
- **Ad formats**: single image, carousel (up to 10), video, collection, instant experience.

### Algorithm notes

- **Auction-based**: bid × estimated action rate × ad quality score.
- **Learning phase**: first ~50 conversions. Don't touch the ad during this period.
- **Creative fatigue**: refresh creative every 2-4 weeks or when frequency > 3.
- **Advantage+ placements**: let Meta optimize placement unless you have a specific reason not to.
- **Broad targeting**: increasingly effective with Meta's AI. Detailed targeting is losing edge.
- **Conversion API (CAPI)**: server-side tracking now essential. Pixel alone misses a substantial share of events.

### Native conventions

- UGC-style creative typically outperforms polished brand ads by a wide margin.
- Carousel for e-commerce (product catalog) and storytelling (sequential narrative).
- "Ugly ads" trend: intentionally raw creative that looks organic in feed.
- Social proof in primary text ("Join 10,000+ traders who..." — number must be real).
- Dynamic creative testing: let Meta mix headlines, images, descriptions.

### Common failures

- Over-produced creative (looks like an ad, gets scrolled)
- Same creative for all funnel stages
- Too many ad sets diluting budget (audience fragmentation)
- Not using Conversion API alongside pixel
- Testing too many variables at once (can't isolate what works)
- Ignoring frequency metrics (ad fatigue kills ROAS)

### Prompt constraints to inject

```xml
<platform_constraints platform="meta_ads">
- Funnel stage: [awareness|consideration|conversion|retention] — determines creative approach
- Primary text: front-load value in first 125 chars
- Headline: ≤40 chars, benefit-driven
- Creative format: [image|video|carousel] — specify
- UGC aesthetic preferred over polished (unless luxury/premium)
- Social proof element required for consideration/conversion stages
- A/B test hypothesis required: what are we testing and why?
</platform_constraints>
```

---

## §Google Ads (Search + Display + YouTube)

*As of 2026-04.*

### Specs (Search)

- **Headlines**: up to 15, each ≤30 chars. Min 3 shown.
- **Descriptions**: up to 4, each ≤90 chars. Min 2 shown.
- **Display URL paths**: 2 fields, each ≤15 chars.
- **Responsive Search Ads (RSA)**: Google mixes and matches headlines/descriptions. Write for independence.

### Specs (Display)

- **Image sizes**: 1200×628 (landscape), 1200×1200 (square), 960×1200 (portrait).
- **Responsive Display Ads**: provide images, headlines, descriptions, logos — Google assembles.
- **Banner ads**: standard IAB sizes (728×90, 300×250, 160×600, etc.).

### Algorithm notes

- **Quality Score** (Search): expected CTR × ad relevance × landing page experience. Scale 1-10.
- **Ad Rank**: bid × Quality Score. Higher QS = lower CPC.
- **Smart Bidding**: tCPA, tROAS, maximize conversions. Let the algorithm bid unless you have strong manual reasons.
- **Broad match + smart bidding**: Google's recommended combo (2024+). Phrase/exact still useful for control.
- **Performance Max**: Google's all-in-one campaign type. Less control, more reach. Good for e-commerce, risky for lead gen.

### Native conventions

- Search: match intent precisely. Keyword in headline. Benefit in description. Strong CTA.
- Display: awareness only. Don't expect direct conversions from display.
- YouTube pre-roll: hook in first 5 seconds (skip button appears at 5s).
- YouTube discovery: thumbnail + title optimization (same as organic YouTube).

### Common failures

- Same ad copy for all keywords (no relevance)
- Not using negative keywords (wasting budget on irrelevant searches)
- Display campaigns expecting conversion-level performance
- Not separating brand and non-brand campaigns (muddles metrics)
- Landing page mismatch (ad promises X, page shows Y)

### Prompt constraints to inject

```xml
<platform_constraints platform="google_ads">
- Campaign type: [search|display|youtube|pmax] — determines approach
- Headlines: ≤30 chars each, write 10-15 for RSA variety
- Descriptions: ≤90 chars each, write 4 for RSA
- Each headline must be independently meaningful (RSA mixes them)
- Keyword intent alignment: what is the searcher looking for?
- Landing page consistency: ad promise must match page
- Negative keyword suggestions included
</platform_constraints>
```

---

## §Twitter / X

*As of 2026-04.*

### Specs

- **Tweet length**: 280 chars (free), 25,000 chars (Premium).
- **Image**: up to 4. 1600×900 (16:9) or 1080×1080. In-feed crop varies.
- **Video**: ≤2:20 (free), longer with Premium. 1280×720 minimum.
- **Thread**: unlimited tweets chained. First tweet is the hook.
- **Polls**: 2-4 options, 5min-7day duration.
- **Spaces**: live audio rooms.

### Algorithm notes

- **For You feed**: algorithmic. Engagement velocity in first 30-60 min determines push.
- **Key signals**: replies > retweets > likes. Replies weighted highest.
- **Quote tweets**: powerful for distribution AND controversy. Designed to spread takes.
- **Replies to large accounts**: quality replies surface prominently. Reply engagement can exceed original post engagement.
- **Posting frequency**: 3-10x/day for growth accounts. More is fine if quality holds.
- **Best times (US)**: 8-10am, 12-1pm, 7-9pm EST. But varies wildly by niche.
- **Bookmarks**: increasingly a signal (2024+). "Bookmark this" as CTA.

### Native conventions

- One idea per tweet. Brevity is the platform.
- Thread format: hook tweet → supporting points → CTA at end. Number your threads.
- Screenshot tweets of other content (charts, data, other tweets) for commentary.
- QT (quote tweet) as debate/commentary format.
- Dry, ironic, deadpan tone performs in trading/crypto/tech niches.
- No hashtags (or 1 max, ironically). Hashtag-heavy tweets read as spam.
- Sentence fragments. Line breaks between ideas. Punchy.
- Niche in-group rituals (e.g., "gm" culture in crypto) — knowing when to use them and when not to = in-group signal.
- Ratio culture: getting more replies than likes = controversial (sometimes intentionally good).

### Common failures

- Thread without a hook tweet (nobody clicks "Show this thread")
- Over-explaining in tweets (the insight should land in one read)
- Hashtag spam (#crypto #trading #AI — instant spam signal)
- Corporate voice on X (platform punishes polish)
- Not engaging in replies (posting into void)
- Posting links without commentary (algorithm suppresses external links slightly)

### Prompt constraints to inject

```xml
<platform_constraints platform="twitter_x">
- Tweet: ≤280 chars unless Premium-length justified
- Hook tweet for threads: must stand alone AND compel thread read
- No hashtags (or 1 max, ironic use only)
- Voice: [specify register from the user context's voice channels — e.g., brand/observer or personal]
- Receipt format: screenshot/data/timestamp if claiming something
- Reply target: if this is a reply, specify the account and their likely post type
- Thread numbering: 1/N format
- Domain conventions from the user context (e.g., cents format 58¢ for prediction-market pricing) if applicable
</platform_constraints>
```

---

## §Email / Newsletter

*As of 2026-04.*

### Specs

- **Subject line**: 30-50 chars ideal (mobile preview). 6-10 words.
- **Preview text**: 40-130 chars. Extends the subject line's pitch.
- **Body**: 200-500 words for promotional. 500-1500 words for newsletter. Longer OK if earned.
- **From name**: personal name > brand name for open rates.
- **Width**: 600px max for email body (rendering compatibility).
- **Images**: not all clients load images by default. Never rely on images for key info.
- **CTA buttons**: 44×44px minimum tap target. One primary CTA per email.

### Algorithm notes (deliverability)

- **Sender reputation**: domain + IP reputation determines inbox vs spam.
- **Authentication**: SPF + DKIM + DMARC all required. Non-negotiable.
- **Engagement signals**: opens + clicks + replies improve reputation. Spam complaints + bounces hurt it.
- **List hygiene**: remove unengaged subscribers every 90 days. Smaller engaged list > large dead list.
- **Warm-up**: new domains need gradual send volume increase over 2-4 weeks.
- **Spam triggers**: ALL CAPS in subject, excessive exclamation marks, "free", "act now", "limited time" overuse.

### Native conventions

- Personal, conversational tone. Like an email from a smart friend.
- One topic per email. Don't make it a newspaper.
- P.S. line: second-highest read section after subject line.
- Plain text emails often outperform HTML for engagement (counterintuitive but true for B2B/founder audiences).
- Welcome sequence: 3-5 emails over first 2 weeks. Sets expectations and builds relationship.
- Segmentation: even basic (new vs returning, engaged vs dormant) dramatically improves performance.

### Common failures

- Subject line that doesn't create a curiosity gap or state a benefit
- No preview text (wastes the second-most-visible real estate)
- Multiple CTAs competing for attention
- HTML-heavy emails that break in Outlook/Gmail dark mode
- No welcome sequence (first email = highest open rate, wasted if generic)
- Not pruning dead subscribers (kills deliverability over time)
- Treating newsletter like a blog repost instead of a standalone reading experience

### Prompt constraints to inject

```xml
<platform_constraints platform="email">
- Subject line: ≤50 chars, curiosity gap or clear benefit
- Preview text: extends subject line, ≤130 chars
- From name: [personal name|brand name] — specify
- Body length: [200-500 promotional | 500-1500 newsletter]
- One primary CTA — what is the single action?
- P.S. line: use for secondary hook or social proof
- Plain text or HTML? (specify based on audience)
- Segment: who receives this? (all / new / engaged / specific trigger)
</platform_constraints>
```

---

## How `prompt-craft` uses this file

1. Detect platform from user input or ask.
2. Load the matching section's prompt constraints.
3. Inject `<platform_constraints>` block into the generated prompt.
4. Cite specific rules in rationale: "platforms.md §TikTok — completion rate is primary signal, so script designed for full watch-through."
5. If multi-platform: generate per-platform variants, each with its own constraints.
6. Check the section's as-of date — if it's over a year old, flag injected specs as "verify current".
