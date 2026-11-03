# First Principles — Finish the Real Task with Fewer Unnecessary Steps

A skill for people who keep asking their AI to stop adding process and finish the
actual job. It checks which steps are necessary, reuses existing work and follows
through to a result the user can use.

[Find First Principles on SideCourt](https://sidecourt.space/work/6123779e-5d92-42aa-9daf-62302822df8f/).
Publication of that page is controlled by its author. GitHub hosts the source and installation package.

## What it does

Turns a request into the simplest sufficient path through completion. It challenges
assumed dependencies, avoids repeated approvals and duplicate ownership, and checks
the outcome at the point of use. Necessary permissions, recovery and verification
remain part of the work.

## Who it's for

Use it when asking for first-principles execution, a simpler workflow, or fewer
unnecessary steps. It works for product changes, research, publishing and operational
work within the authority the user has actually given.

It does not force a thinking template onto every question, restart a working project,
resume paused tasks, or promise a globally optimal plan. An analysis-only request
remains analysis-only. It requires no account, API key or new service of its own.

## Install

```sh
npx skills add m1nga/first-principles
```

Then ask:

> Use $first-principles to finish this task with the fewest necessary steps. Reuse
> what we already have, preserve the full result and verify that I can actually use it.

## Example

**Request:** “The report is approved. Fix the broken download on the existing page
and give me the working link.”

**Expected behavior:** inspect the existing link and artifact, repair the relevant
path, verify an actual download, and return the link. If deployment is already
authorized, finish it. If a real permission is missing, prepare the fix and identify
that specific remaining action. No new portal, approval round or broad redesign.

**Boundary:** “Make the migration simpler, but keep the release paused.” Reuse the
existing state and prepare or test only permitted steps. Simplicity never lifts the
pause. A handoff must retain enough state for the recipient to execute correctly.

These examples are authored scenarios, not customer testimonials.

## Design notes

Ming repeatedly asked for complete outcomes with fewer detours. Historical reviews
showed an important distinction: shortening the visible instructions can still leave
more manual work, repeated decisions and incomplete execution underneath.

The skill therefore optimizes the whole route to a usable outcome. It is a compact
execution aid, not a new coordination system. It reads the user's current agreements
instead of embedding one person's model settings, task IDs or private history.

[Source comparisons](skills/first-principles/references/comparisons.md) explain what
was adapted and rejected. When authoring another skill, it searches relevant author
sources and records a concrete integration decision through the existing release
process rather than adding a second process.

## Validation

The release includes a maintainer walkthrough of normal, failure and routing cases,
explicitly labeled as simulations, plus actual package, metadata and publication
checks. It has not been independently user-tested, and no reduction in tokens,
execution time or rework is claimed yet. See the content-bound
[release evidence](https://github.com/m1nga/skills/blob/main/ops/skill-quality/reviews/first-principles.json).

## Author

Built by [Ming](https://github.com/m1nga). Source and installation are maintained on
GitHub; the product's primary discovery entry is on SideCourt.
