# Small skill discovery experiments

Use this for an individual's skill portfolio. A useful outcome is that a relevant
person understands, tries, and benefits from a skill. Maintenance commits are not
acquisition. Do not build an enterprise SEO stack unless missing data justifies it.

## Pick one question

Prioritize skills the owner uses, explicitly chooses, or that match evidenced work.
Audit/search appearances are not confirmed usage; record that distinction. Keep a
small active set. Preserve other products without automatically deleting, renaming,
or rewriting them. Stable slugs preserve installation links; plain display names,
README openings, and descriptions can improve understanding without migrations.

Choose a primary audience and task, then one hypothesis, such as:
"A runnable before/after example will explain what this prompt skill preserves."
Name the affected surface, the baseline, the change, and the observation date.
Do not manufacture query-volume numbers. Treat candidate search phrases as hypotheses.

Before choosing copy or comparing discoverability, use the
[search-intent workflow](search-intent.md). Keep name, function, problem and pain
queries separate; inspect actual results and retain useful failed-query evidence.

## Use a small persistent work folder

Keep private operations outside the public source registry, for example:

```text
skill-discovery/
  STATE.md             active products, next action, current blockers
  experiments.json     hypotheses, fixed queries, status, next review date
  observations/        timestamped raw snapshots
  drafts/              unsent demonstrations or distribution copy
  LESSONS.md           observation → tentative lesson → next test
```

Read STATE.md first and only the current experiment. Update after a meaningful
action or result, not after every tool call. Keep source code in its repository.
An older observation cannot establish current ranking or approval. The next worker
must be able to resume from the current files without reading all conversations.

## Improve something a visitor can use

Prefer an accurate first-screen explanation, a concrete input/output demonstration,
an install-and-invoke example, or a broken workflow fix over repeated synonyms.
Label authored illustrations and agent simulations honestly. Only claim measured
time savings when a relevant baseline and timing actually exist.

Use scripts/discovery_snapshot.py from this skill for fixed GitHub queries. Record
exact-name, primary problem, and optionally adjacent intent using the same query and
search order before/after. Metadata and ranks may be unchanged immediately; record
that, then choose a later review interval. A default seven-day observation window is
an experiment choice, not a claim about search-engine indexing latency. Do not keep
rewriting a product while its experiment is waiting for evidence.

General-web indexing and AI-answer citations need their own source URLs and dated
observations; GitHub search does not prove either. No synthetic user counts. Views
may include internal activity. Install-counter deltas remain unattributed unless
external use is evidenced. Clones include automated verification and are diagnostic.
API failures are unknown values, never zero. Do not infer causation from one before/
after result without accounting for other changes and the small sample.

## Distribution and learning

Retain the event ID, exact skill version, intended reader, one concrete task, demo
artifact and evidence type, destination, publication state and actual URL. In the
existing private record, track visits, installs, first completed task, repeat use,
feedback, stars and SideCourt visits separately. Give each a dated source and
observation window; unavailable values stay unknown. Do not sum these into users.
A referral link alone proves neither a visit nor a contribution.

Prioritize a demonstrated first-use obstacle over cosmetic work. The first screen
should let a specific reader recognize a task, see its result and find one next
step. Label fictional inputs, offline checks and missing platform verification.

Research applied on 2026-11-10: adapt [kpab's outsider audit](https://github.com/kpab/github-star-growth/blob/main/SKILL.md)
to first-use evidence, [content-strategy](https://github.com/coreyhaines31/marketingskills/blob/main/skills/content-strategy/SKILL.md)
to one audience and information gain, and [launch](https://github.com/coreyhaines31/marketingskills/blob/main/skills/launch/SKILL.md)
to readiness and feedback. Reject fixed star forecasts, mandatory calendar ratios
and launching every skill on every channel. These are design influences, not
evidence that this portfolio has gained users.

A stronger page is a useful asset, but it may receive no audience on its own. Prepare
one specific demonstration for a channel where the target user already asks that
question. External posting or outreach requires the user's authorization identifying
the destination and purpose; a generic promotion goal is not a blanket send command.
Keep unapproved copy in drafts and report it as unsent.

For repeated work, handle one actionable experiment per run. If none is due and
there is no confirmed defect, record a cheap no-op. Notify only a meaningful change,
completed improvement, failure, or required user action unless periodic reports were
requested. Update the existing scheduler instead of adding overlapping monitors.

Revisit a lesson when the next observation contradicts it. Persisting examples,
outcomes, and user corrections improves this workflow; it does not retrain model
weights or prove a universal SEO rule.
