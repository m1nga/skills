# Campaign Reference

Funnel strategy, creative matching, retargeting, multi-touch sequencing, budget allocation, testing frameworks, and measurement benchmarks. `prompt-craft` loads this for campaign planning and ad strategy prompts.

> Brand examples below are **fictional** ("Meridian" — invented market-data tool). Benchmark figures are directional heuristics, not citations — verify against current data before using them as targets. **If the user context defines an actual budget structure, funnel model, or KPI set, it overrides the defaults in this file.**

---

## §1 Funnel Stages

### Stage 1: Awareness (TOFU — Top of Funnel)

- **Goal**: make strangers aware the brand/product exists
- **Audience state**: don't know you, may not know they have the problem
- **Content type**: entertaining, educational, pattern-interrupting. Zero ask.
- **Metrics**: reach, impressions, video views, brand lift
- **CTA**: none or soft (follow, bookmark, "more like this")
- **Creative approach**: broadest appeal, lowest friction, highest entertainment value
- **Budget allocation**: 40-60% of total in growth phase

### Stage 2: Consideration (MOFU — Middle of Funnel)

- **Goal**: make aware people interested in your specific solution
- **Audience state**: know you exist, evaluating options, comparing
- **Content type**: product demos, comparisons, social proof, how-it-works
- **Metrics**: engagement rate, click-through rate, time on site, saves
- **CTA**: medium friction (visit site, watch demo, read case study)
- **Creative approach**: specific, proof-heavy, differentiation-focused
- **Budget allocation**: 20-30% of total

### Stage 3: Conversion (BOFU — Bottom of Funnel)

- **Goal**: turn interested people into customers/users
- **Audience state**: ready to act, need final push or friction removal
- **Content type**: testimonials, offers, urgency, direct response, removal of objections
- **Metrics**: conversion rate, cost per acquisition, ROAS
- **CTA**: high friction acceptable (install, sign up, buy, subscribe)
- **Creative approach**: direct, benefit-focused, objection-handling
- **Budget allocation**: 15-25% of total

### Stage 4: Activation

- **Goal**: turn sign-ups into active users who experience core value
- **Audience state**: signed up but haven't experienced the "aha moment"
- **Content type**: onboarding, first-use guides, welcome sequences
- **Metrics**: activation rate, time-to-first-value, feature adoption
- **CTA**: specific first action ("Set up your first alert", "Install the extension")
- **Creative approach**: clear, step-by-step, friction-removing
- **Budget allocation**: 5-10% (often email/in-product, not paid)

### Stage 5: Retention & Referral

- **Goal**: keep active users engaged and turn them into advocates
- **Audience state**: using product, potentially drifting or becoming champions
- **Content type**: advanced tips, community, exclusive content, referral incentives
- **Metrics**: retention rate, NPS, referral rate, LTV
- **CTA**: share, refer, contribute, upgrade
- **Creative approach**: community-building, reward-based, exclusive
- **Budget allocation**: 5-10%

---

## §2 Funnel × Creative Matching

### The cardinal rule

**Never serve conversion creative to a cold audience. Never serve awareness creative to a hot audience.** This single mistake wastes more ad budget than any other.

### Matching matrix

| Funnel Stage | Creative Type | Hook Style | CTA Level | Proof Required |
|---|---|---|---|---|
| Awareness | Entertainment, education, trend-riding | Pattern interrupt, shocking stat | None or soft | None |
| Consideration | Demo, comparison, how-it-works | Problem statement, curiosity gap | Medium | Social proof, data |
| Conversion | Testimonial, offer, direct response | Direct benefit, urgency | High friction OK | Heavy proof, receipts |
| Activation | Onboarding, tutorial, welcome | "Here's what to do first" | Specific action | Product screenshots |
| Retention | Advanced tips, community, exclusive | "You're already using X, now try Y" | Engage/share | Usage data |

### Example matching (fictional Meridian — derive the real one from the user context)

| Funnel Stage | Example Creative | Platform |
|---|---|---|
| Awareness | Signal catch receipts, arb alerts, "market is wrong" takes | X, TikTok, Reels |
| Consideration | Extension demo, API walkthrough, signal → trade timeline | X threads, YouTube |
| Conversion | "Free. No rate limits. Just install." + receipt | X, landing page |
| Activation | "First signal in 2 minutes" onboarding | Email, in-product |
| Retention | Advanced signal patterns, community, feedback loops | Discord, email |

---

## §3 Retargeting Strategy

### Retargeting tiers

| Tier | Audience | Window | Creative | Goal |
|---|---|---|---|---|
| 1 | Visited site, didn't convert | 1-7 days | Objection-handling, social proof | Convert |
| 2 | Visited site, didn't convert | 8-30 days | Different angle, stronger proof | Re-engage |
| 3 | Engaged with content (liked, saved, watched 50%+) | 1-14 days | Product demo, next-step | Move to consideration |
| 4 | Past converters / active users | Ongoing | Upsell, referral, community | Retain, expand |
| 5 | Lookalike of converters | Ongoing | Best-performing awareness creative | Acquire |

### Retargeting rules

1. **Exclude converters** from conversion retargeting (don't ask people to do what they already did)
2. **Frequency cap**: 3-5 impressions per user per week. Beyond that = annoyance.
3. **Creative rotation**: 2-3 variants per tier. Rotate every 2 weeks minimum.
4. **Sequential messaging**: Tier 3 → Tier 1 → Tier 2. Not random.
5. **Burn pixels**: stop showing ads after conversion event fires.

---

## §4 Multi-Touch Sequencing

### The multi-touch reality

Average touches to conversion by category *(directional heuristics)*:

| Category | Average touches | Range |
|---|---|---|
| Impulse / low-friction (free tool) | 3-5 | 1-8 |
| Considered purchase (SaaS $50-200/mo) | 7-13 | 4-20 |
| High-ticket (enterprise, $1K+) | 15-25 | 8-40 |
| Free product with friction (extension install) | 4-7 | 2-12 |

### Sequencing principles

1. **First touch = pure value**, no ask. Earn attention before requesting it.
2. **Vary the format**: video → image → text → video. Same message, different modality.
3. **Escalate the ask gradually**: follow → engage → visit → try → commit.
4. **Each touch must be independently valuable**. If someone sees only touch #4, it should still make sense.
5. **Acknowledge the relationship**: "You watched our signal catch video. Here's what that signal looks like in real-time." Not "BUY NOW" after one video view.

### Sequencing example (fictional Meridian, awareness → activation)

1. **X post**: Signal catch receipt (awareness, zero ask)
2. **X post**: Arb alert screenshot (awareness, soft follow CTA)
3. **X thread**: "How we caught 3 moves this week" (consideration, link to site)
4. **Retargeting ad**: Extension demo video (conversion, install CTA)
5. **Email**: "Your first signal is waiting" (activation, first-use guide)
6. **Community invite**: "Join 500 traders in the signal room" `[ILLUSTRATIVE — number must be real]` (retention, community)

---

## §5 Budget Allocation

### Budget split by channel (organic-first model)

*If the user context defines an actual budget structure, use that — this table is the default shape for an organic-first early-stage brand.*

| Channel | % of budget | Purpose |
|---|---|---|
| Organic content production | 60-70% | Tools, time, AI systems |
| Paid social (Meta, X) | 15-25% | Amplification of best organic + retargeting |
| Paid search | 5-10% | Brand protection + high-intent keywords |
| Influencer/KOL | 0-10% | When organic proves the message, amplify via voices |

### Budget rules

1. **Organic first, paid second**. Prove the message works organically before spending money to amplify it.
2. **Boost winners**: don't create new paid-only creative. Take your best-performing organic content and put budget behind it.
3. **Test budget**: 20% of paid budget = testing. 80% = scaling what works.
4. **Kill fast**: if a creative doesn't hit benchmark in 2-3 days (sufficient impressions), kill it. Don't "give it time."
5. **Daily budget > lifetime budget** for testing. Lifetime budget lets the algorithm back-load spend.

### Budget benchmarks *(directional, circa 2024-25 — verify current rates)*

| Metric | Poor | Acceptable | Good | Great |
|---|---|---|---|---|
| CPM (awareness) | >$15 | $8-15 | $4-8 | <$4 |
| CPC (consideration) | >$3 | $1-3 | $0.50-1 | <$0.50 |
| CPI (app/extension install) | >$5 | $2-5 | $1-2 | <$1 |
| CAC (paying customer) | Varies | Varies | <1/3 LTV | <1/5 LTV |

---

## §6 Creative Testing

### What to test (ranked by impact)

1. **Hook / first 3 seconds** (highest impact — test this first, always)
2. **Offer / CTA** (what you're asking them to do)
3. **Creative format** (video vs image vs carousel)
4. **Headline / primary text** (the words around the creative)
5. **Audience targeting** (who sees it)
6. **Landing page** (where they go after clicking)

### Testing methodology

1. **One variable at a time**. Testing hook AND CTA simultaneously = you learn nothing.
2. **Minimum sample**: 1,000 impressions OR 50 clicks per variant before declaring a winner.
3. **Statistical significance**: use a significance calculator. "It looks better" is not data.
4. **Winner criteria**: define BEFORE the test starts. "Winner = lowest CPA" or "Winner = highest CTR." Not both.
5. **Test duration**: 3-7 days minimum. Don't judge day 1 data — algorithms need learning time.

### Testing framework: The 3-2-1 method

For each campaign:
- **3 hooks** (different hook types from `copywriting.md §2`)
- **2 formats** (e.g., video + static image)
- **1 CTA** (keep constant while testing hooks/formats)

= 6 variants. Run for 5 days. Kill bottom 4. Scale top 2. Then test CTAs against the winning hook/format.

---

## §7 Measurement Benchmarks

*(Directional, circa 2024-25 — platform averages drift; verify before setting targets.)*

### Platform-specific benchmarks (organic)

| Platform | Metric | Poor | Average | Good | Great |
|---|---|---|---|---|---|
| X/Twitter | Engagement rate | <1% | 1-3% | 3-5% | >5% |
| X/Twitter | Link CTR | <0.5% | 0.5-1% | 1-2% | >2% |
| TikTok | Avg watch time (30s video) | <5s | 8-12s | 15-20s | >20s |
| TikTok | Share rate | <0.1% | 0.5-1% | 1-3% | >3% |
| Instagram | Save rate | <0.5% | 1-2% | 2-4% | >4% |
| Instagram | Share rate (DM) | <0.3% | 0.5-1% | 1-3% | >3% |
| YouTube | CTR (thumbnail) | <2% | 4-6% | 7-10% | >10% |
| YouTube | Avg view duration | <30% | 40-50% | 50-60% | >60% |
| LinkedIn | Engagement rate | <1% | 2-4% | 4-7% | >7% |
| Email | Open rate | <15% | 20-30% | 30-40% | >40% |
| Email | Click rate | <1% | 2-3% | 3-5% | >5% |

### Growth benchmarks (early-stage, organic-first)

| Metric | Month 1 | Month 2-3 | Month 4-6 | Month 7-12 |
|---|---|---|---|---|
| X followers | 50-100 | 200-500 | 500-1500 | 1500-5000 |
| IG followers | 30-80 | 100-300 | 300-800 | 800-2500 |
| TikTok followers | 50-200 | 200-1000 | 1000-5000 | 5000-20000 |
| Email subscribers | 20-50 | 50-200 | 200-500 | 500-2000 |

Note: niche categories run smaller than general audiences. Adjust follower expectations down 30-50% but engagement rates up 2-3x (niche = higher engagement per follower).

---

## §8 Diagnostic Patterns

When a campaign isn't working, diagnose in this order:

### Problem: Low reach / impressions

- **Check first**: posting frequency (too low?), posting time (off-peak?), platform suppression (external links?)
- **Check second**: content type (is the platform favoring video and you're posting images?)
- **Check third**: account health (shadowban? policy violation?)
- **Fix**: increase frequency, optimize timing, match platform-preferred format

### Problem: High reach, low engagement

- **Check first**: hook quality (are people seeing it but not caring?)
- **Check second**: audience match (reaching the wrong people?)
- **Check third**: content substance (all hook, no meat?)
- **Fix**: test different hooks, narrow targeting, add more value to content body

### Problem: High engagement, low conversion

- **Check first**: CTA clarity (do they know what to do?)
- **Check second**: friction (too many steps between content and conversion?)
- **Check third**: trust gap (engagement ≠ trust; are you proving enough?)
- **Fix**: simplify CTA, reduce friction, add social proof and receipts

### Problem: High conversion, low retention

- **Check first**: expectation mismatch (did the content promise something the product doesn't deliver?)
- **Check second**: onboarding (is the first experience good enough?)
- **Check third**: product-market fit (the hardest answer)
- **Fix**: align content promise with product reality, improve onboarding, collect user feedback

### Problem: Inconsistent results

- **Check first**: creative fatigue (same creative too long?)
- **Check second**: algorithm changes (platform-level shifts?)
- **Check third**: external factors (news cycle, competitor activity, seasonality?)
- **Fix**: refresh creative, diversify platforms, build owned channels (email) for stability

---

## How `prompt-craft` uses this file

1. **Campaign prompts**: require funnel stage declaration. Match creative approach from §2.
2. **Ad prompts**: inject funnel-appropriate CTA level and proof requirements.
3. **Budget discussions**: reference §5 benchmarks and allocation rules — user-context budget structure wins when defined.
4. **Testing prompts**: inject 3-2-1 method from §6 or specify testing variable.
5. **Measurement**: cite relevant benchmarks from §7 in prompt constraints, flagged as directional.
6. **Diagnostics**: when the user describes a campaign problem, follow §8 diagnostic flow.
7. **In rationale**: "campaigns.md §funnel-matching — awareness creative, no CTA, pattern interrupt hook."
