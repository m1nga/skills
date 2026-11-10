# Practical AI Agent Skills That Finish the Job

[![GitHub stars](https://img.shields.io/github/stars/m1nga/skills?style=social)](https://github.com/m1nga/skills/stargazers)
[![skills.sh](https://skills.sh/b/m1nga/skills)](https://skills.sh/m1nga/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Try one skill on the task you have now: compare changed research sources, make an
importable playlist, find a product's first-use obstacle, test AI instructions,
or organize a task with a recovery path. Each standalone repository shows its
requirements, an example, and the limits of its evidence.

Built from real solo-builder workflows for Codex, Claude Code, Cursor, and other tools that support
the open Agent Skills format.

## Built to evolve with AI

We follow advances in AI and adapt our skills when they improve real work, and we retire skills
when the hosts do the job natively. Changes are checked against concrete tasks, with the scope and
limits of validation made public. A newer model is a reason to evaluate, not an automatic replacement.

[See the latest verified adaptations](docs/ai-adaptation.md).

## Start here

Choose one concrete result to try:

| Your current problem | First skill to try | See the result before installing |
|---|---|---|
| An agent keeps rereading the same source library | [Context Budget](https://github.com/m1nga/context-budget) | A reproducible source-difference example; bytes and provider tokens kept separate |
| A playlist recommendation is hard to get into a music service | [Mixtape](https://github.com/m1nga/mixtape) | Selection, catalog matching and actual destination import reported separately |
| You need to find where a new user gets stuck | [First-Time User Tester](https://github.com/m1nga/product-experience-officer) | A maintainer-run CLI failure and recovery, with an executable report generator |
| An instruction might miss a trigger or collide with another skill | [Scenario Probe](https://github.com/m1nga/scenario-probe) | A before/after illustration and an actual-run evidence protocol |
| You need to organize files without losing later edits | [TaskDock](https://github.com/m1nga/taskdock) | [Run the move-and-recover demonstration](docs/try-taskdock.md) |

Examples label executable fixtures, authored illustrations and live platform checks
separately. They are not customer testimonials or universal time-saving claims.

[Choose among the full portfolio by task](docs/choose-a-skill.md), including memory,
handoff, publishing, saved posts and optional reasoning workflows.

See every available skill:

```bash
npx skills add m1nga/skills --list
```

Start with one skill for the task you have now:

```bash
npx skills add m1nga/taskdock
```

Claude Code users can also install TaskDock as a plugin:

```bash
claude plugin marketplace add m1nga/taskdock
claude plugin install taskdock@taskdock
```

Then ask your agent: `Use $taskdock to organize this task and record its next action.`
Choose another skill from the task tables below when you need it. You do not need
all these skills loaded for an ordinary task.

If a skill helps a real task, star that skill's own repository or share a small
reproduction of what failed. You can also [star this collection](https://github.com/m1nga/skills)
to find the full catalog again.

## Pick the result you need

### Define, test, and build products

| You need to… | Use | You get |
|---|---|---|
| turn visual references into a scoped design and usable interface | [Design Agent](https://github.com/m1nga/design-agent) | reference analysis, design decisions and checked implementation |
| simplify cluttered layouts and repetitive UI copy | [Clear Interface](https://github.com/m1nga/clear-interface) | focused hierarchy and wording with important consequences preserved |
| map an entire product system | [Product System Mapper](https://github.com/m1nga/map-product-system) | journeys, capabilities, ownership, gaps, and delivery slices |
| experience a product as a new user | [First-Time User Tester](https://github.com/m1nga/product-experience-officer) | a severity-ranked report of confusion and fixes |
| think through an ambiguous decision, or get grilled before building | [Decision Thinking Partner](https://github.com/m1nga/thinking-partner) | a better frame, real alternatives, and on request a locked, scoped plan |
| decide whether to repair or rebuild | [Project Rebuild Advisor](https://github.com/m1nga/diagnose-project-rebuild) | an evidence-based recover, repair, rebuild, continue, or stop verdict |

### Run reliable agent work

| You need to… | Use | You get |
|---|---|---|
| carry an instruction through existing owners to a verified result | [Task Execution Coordinator](https://github.com/m1nga/major-tom) | scoped work, selected evidence and verified outcomes |
| recover current decisions and learn from observed outcomes | [Work Memory](https://github.com/m1nga/work-memory) | bounded project context, exact evidence and a selective learning trail |
| keep a task resumable across sessions, agents and machines | [TaskDock](https://github.com/m1nga/taskdock) | one portable task folder with identity, state, plan, and reversible organization |
| close a milestone cleanly | [Iteration Cleanup & Handoff](https://github.com/m1nga/iteration-close) | preserved decisions, safe cleanup, and a tested takeover |
| retain reusable lessons without stale decisions | [Project Lessons Log](https://github.com/m1nga/experience-pack) | a project ledger plus portable lessons |
| publish a finished skill as a product | [Skill Publisher](https://github.com/m1nga/publish-skill-product) | a searchable repository, direct install path, and release proof |

### Improve prompts and instructions

| You need to… | Use | You get |
|---|---|---|
| clean up dictated or rambling input | [Prompt Cleaner](https://github.com/m1nga/prompt-distill) | a clear reusable prompt that preserves your intent |
| find how AI instructions fail before release | [AI Instruction Stress Test](https://github.com/m1nga/scenario-probe) | trigger misses, collisions, and behavior failures |

### Personal workflows

| You need to… | Use | You get |
|---|---|---|
| build a playlist and check its import | [Playlist Builder](https://github.com/m1nga/mixtape) | catalog-checked recordings, an import link and a separate destination status |
| review a US stock portfolio with sources | [Stock Portfolio Brief](https://github.com/m1nga/daily-brief) | a hold, buy, trim, switch or wait brief with explicit data gaps; never trades |

## Standalone applications

- [EarBrief — Turn Work Documents into Audio](https://github.com/m1nga/earbrief-app) turns text and
  PDF reports into Chinese or English programs in a persistent mobile station. It replaced the
  listen-compare and earbrief skills and runs independently of Claude or Codex.
- [Daycup](https://sidecourt.space/drops/daycup/) is an offline coffee companion: equipment and
  beans, a starting recipe, timing and taste notes, one variable changed per brew. It replaced the
  coffee-brewing skill.

## Retired on 2026-09-19

Fourteen skills were archived after a usage audit: their repositories are read-only, their links
still resolve, and their source stays in this repository's history before this date. They are not
listed by the Skills CLI anymore.

| Skill | Why it was retired |
|---|---|
| extend-first, side-quest, loop-system-architect | Claude Code and Codex now search and suggest skills, run background subagents, and schedule loops natively |
| conclude-rounds, one-sentence | The hosts recap a session and answer one-line requests on their own |
| desktop-package | TaskDock's task folder covers the review-pack need |
| grilling | Merged into thinking-partner as its interview mode |
| idea-probe, product-5w | Not used; pre-build and definition questions go to thinking-partner |
| write-judge-prompt, validate-evaluator | Not used; `claude plugin eval` ships LLM graders |
| prompt-craft | Knowledge base stale; prompt-distill covers the need |
| voice-extractor | Not used |
| coffee-brewing | Replaced by the Daycup application |

## More ways to put a skill to work

| Your current need | Skill and install entry | What to expect |
|---|---|---|
| Find something useful in saved Xiaohongshu research | [RedBot](https://github.com/m1nga/redbot) | Read selected source material and prepare an editable coding prompt; account access is an invitation beta. |
| Remove unnecessary steps from a task | [First Principles](https://github.com/m1nga/first-principles) | Reuse existing work, preserve constraints and verify the requested result. |
| Take a short thinking break while an AI agent works | [BreakingGap](https://github.com/m1nga/breakinggap) | A three-minute reflection in your conversation; it does not monitor agents or run reminders. |

Use `npx skills add m1nga/<skill-name>` with the repository name shown on the
individual product page. Each guide describes its requirements and validation limits.
These links point to already published products; installing one does not start a service.

## Why these skills are different

- Each skill solves one recognizable problem and produces a named result.
- Destructive actions, uncertain claims, and unverified completion are called out explicitly.
- Every released skill has its own product page, source package, direct install command, and release
  provenance.
- Names stay plain for users while stable repository slugs keep existing installs working.

## Local-only boundary

`day-close` is not a public product and is excluded from the current source distribution.
Its earlier generic instructions remain recoverable from Git history; this is not a
claim that previously public history became private. Existing personal installations
and journals are not managed by the public publisher.

## Source and releases

This repository is the source registry. Each directory contains one skill; `products.json` holds
its public title, description, and GitHub topics; `scripts/publish-skill` releases committed source
to `github.com/m1nga/<skill-name>` and verifies direct discovery through the Skills CLI.

```bash
scripts/verify-products
scripts/publish-skill diagnose-project-rebuild
```

Built by [Ming](https://github.com/m1nga). MIT licensed.

<!-- sidecourt-referral:start -->
## Explore SideCourt

These skills support the work behind a project. [Browse SideCourt](https://sidecourt.space/drops/?utm_source=github&utm_medium=readme&utm_campaign=tools&utm_content=skills) to see what people are making, try something that interests you, or share your own work.
<!-- sidecourt-referral:end -->
