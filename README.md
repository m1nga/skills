# Practical AI Agent Skills That Finish the Job

[![GitHub stars](https://img.shields.io/github/stars/m1nga/skills?style=social)](https://github.com/m1nga/skills/stargazers)
[![skills.sh](https://skills.sh/b/m1nga/skills)](https://skills.sh/m1nga/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

13 installable agent skills for turning ambiguous work into concrete, checkable results: keep a
task resumable across sessions and agents, map a product, decide with real alternatives, recover a
confused project, stress-test AI instructions, close an iteration, or make a playlist that imports.

Built from real solo-builder workflows for Codex, Claude Code, Cursor, and other tools that support
the open Agent Skills format.

## Built to evolve with AI

We follow advances in AI and adapt our skills when they improve real work, and we retire skills
when the hosts do the job natively. Changes are checked against concrete tasks, with the scope and
limits of validation made public. A newer model is a reason to evaluate, not an automatic replacement.

我们持续跟进 AI 的进展，把经过具体任务验证的改进带进产品与技能；宿主自带的能力，我们就退役对应的技能。

[See the latest verified adaptations](docs/ai-adaptation.md).

## Start here

Choose one concrete result to try:

| Your current problem | First skill to try | See the result before installing |
|---|---|---|
| A task's files moved and the next action is buried in an old chat | [TaskDock](https://github.com/m1nga/taskdock) | [Run the move-and-recover demonstration](docs/try-taskdock.md) |
| A product feature is missing retries, ownership or a complete user path | [Product System Mapper](https://github.com/m1nga/map-product-system) | [Read a complete import-and-retry example](https://github.com/m1nga/map-product-system/blob/main/skills/map-product-system/examples/import-retry.md) |

The first demonstration executes real code with fictional inputs. The product map is an authored
example. Neither is a customer testimonial or a time-saving claim.

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
| map an entire product system | [Product System Mapper](https://github.com/m1nga/map-product-system) | journeys, capabilities, ownership, gaps, and delivery slices |
| experience a product as a new user | [First-Time User Tester](https://github.com/m1nga/product-experience-officer) | a severity-ranked report of confusion and fixes |
| think through an ambiguous decision, or get grilled before building | [Decision Thinking Partner](https://github.com/m1nga/thinking-partner) | a better frame, real alternatives, and on request a locked, scoped plan |
| decide whether to repair or rebuild | [Project Rebuild Advisor](https://github.com/m1nga/diagnose-project-rebuild) | an evidence-based recover, repair, rebuild, continue, or stop verdict |

### Run reliable agent work

| You need to… | Use | You get |
|---|---|---|
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
| build a playlist that imports correctly | [Playlist Builder](https://github.com/m1nga/mixtape) | a verified playlist for your streaming service |
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

## Why these skills are different

- Each skill solves one recognizable problem and produces a named result.
- Destructive actions, uncertain claims, and unverified completion are called out explicitly.
- Every released skill has its own product page, source package, direct install command, and release
  provenance.
- Names stay plain for users while stable repository slugs keep existing installs working.

## Source and releases

This repository is the source registry. Each directory contains one skill; `products.json` holds
its public title, description, and GitHub topics; `scripts/publish-skill` releases committed source
to `github.com/m1nga/<skill-name>` and verifies direct discovery through the Skills CLI.

```bash
scripts/verify-products
scripts/publish-skill diagnose-project-rebuild
```

Built by [Ming](https://github.com/m1nga). MIT licensed.
