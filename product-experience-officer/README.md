# product-experience-officer

A reviewer that experiences your unreleased product as a total stranger first — and only afterwards puts the expert hat on to tell you what broke, why it hurt, and what to fix first.

## What it does

Runs your product (or reads your screenshots) in two strictly separated phases. Phase 1: a zero-context first-time user who hasn't read your README, doesn't know your vision, and writes down every confusion the moment it happens — because confusion evaporates once understood and can't be re-felt. Phase 2: a product/UX expert who reads the code and docs to explain each confusion and prescribe a fix. The output is a single report: a one-paragraph verdict up top ("would a stranger come back tomorrow?"), a first-person experience log, severity-ranked findings with evidence, one recommended fix each, and effort estimates, plus an honest list of what this round couldn't verify.

## When it fires

- "Walk through my app as a first-time user."
- "Does this onboarding make sense?"
- "UX audit these screenshots."
- "Pretend you've never seen this and try it."
- "帮我从用户视角体验一下这个产品"
- "看看新用户会怎么想"

It does not fire for debugging a specific error from a screenshot, or for code review — it evaluates the experience, it doesn't repair the build.

## Install

```
npx skills add m1nga/skills@product-experience-officer
```

## Example

> **You:** I just finished the onboarding flow for my journaling app. Walk through it as a first-time user — here's the local dev command.
>
> **Claude:** launches the app cold, freezes on the first screen ("I see a text box and the word 'begin'. I don't know what this app is for yet"), wanders off the happy path, answers a prompt with "idk", pastes 2000 words, quits mid-flow and comes back. Then reads the code and reports: verdict first, then findings like — 🟠 Major: the first screen never says what the product does before asking for personal writing; evidence quoted verbatim; fix: one line of promise copy above the input; effort S.

## Works well with

- [`map-product-system`](../map-product-system/) — map what the product actually is before or after an experience run.
- [`diagnose-project-rebuild`](../diagnose-project-rebuild/) — when the report's Blockers point at structural rot rather than surface fixes.

## Design notes

The methodology is opinionated on purpose, and each rule comes from real reviews of solo-built products:

- **Two phases, never mixed.** A builder cannot un-know their product; neither can a reviewer who read the spec first. The stranger must run before the expert, because confusion is perishable evidence.
- **Verdict first.** A solo builder reading the report needs one decision ("is this ready, and what do I fix now?"), not a flat list of twenty items. Prioritization is the deliverable, not a garnish.
- **One recommended fix per finding.** Listing three options without a pick pushes the decision cost back onto the person who asked for help. The skill always recommends, with a reason, and labels taste as taste.
- **Treat the developer's data as production.** Live runs happen on the builder's own machine, next to their real files. The skill refuses writes that touch pre-existing user data and records the attempt as a finding — a rule written after runs where the product cheerfully offered to overwrite the builder's real archive.
- **Degrade honestly.** No browser? Copy and flow get reviewed; every visual claim moves to a to-verify checklist instead of being guessed from HTML. A smaller honest report beats a complete fabricated one.

## Field-tested

Probed 7 scenarios across 5 personas · 5 fired correctly · 2 correctly stayed quiet.

> **"Does this onboarding make sense? Here are three screenshots."** → Fired in Mode A — and an English-speaking user gets an English report. (An earlier probe caught this skill answering English builders in Chinese; that fix is now verified green.)

> **"Here's a screenshot of the error my app throws on login — what's wrong?"** → Correctly stayed quiet. A screenshot is not automatically a UX review: the description's NOT-clause sends debugging elsewhere, a boundary added after a real false-fire.

> **"Run my web app and review it as a first-time user"** — in an environment with no browser or screenshots → Fired, and degraded honestly: copy and flow reviewed from text, every visual dimension moved to an explicit To-verify checklist, and inferring "the spacing is probably fine" from CSS is banned as fabricated evidence.

Probe method: [scenario-probe](../scenario-probe/)
