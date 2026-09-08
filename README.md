# Practical AI Agent Skills That Finish the Job

[![GitHub stars](https://img.shields.io/github/stars/m1nga/skills?style=social)](https://github.com/m1nga/skills/stargazers)
[![skills.sh](https://skills.sh/b/m1nga/skills)](https://skills.sh/m1nga/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

26 installable agent skills for turning ambiguous work into concrete, checkable results: plan a
product, recover a confused project, stress-test AI instructions, preserve your writing voice,
close an iteration, or make a playlist that actually imports.

Built from real solo-builder workflows for Codex, Claude Code, Cursor, and other tools that support
the open Agent Skills format.

## Built to evolve with AI

We follow advances in AI and adapt our skills when they improve real work. Changes
are checked against concrete tasks, with the scope and limits of validation made
public. A newer model is a reason to evaluate, not an automatic replacement.

我们持续跟进 AI 的进展，把经过具体任务验证的改进带进产品与技能。

[See the latest verified adaptations](docs/ai-adaptation.md).

## Start here

Choose one concrete result to try:

| Your current problem | First skill to try | See the result before installing |
|---|---|---|
| A task's files moved and the next action is buried in an old chat | [TaskDock](https://github.com/m1nga/taskdock) | [Run the move-and-recover demonstration](docs/try-taskdock.md) |
| An agent workflow needs explicit budgets and failure checks | [Agent Loop Builder](https://github.com/m1nga/loop-system-architect) | [Reproduce a rejected boolean budget](docs/try-loop-budget-check.md) |
| A product feature is missing retries, ownership or a complete user path | [Product System Mapper](https://github.com/m1nga/map-product-system) | [Read a complete import-and-retry example](https://github.com/m1nga/map-product-system/blob/main/skills/map-product-system/examples/import-retry.md) |

The first two demonstrations execute real code with fictional inputs. The product
map is an authored example. None is a customer testimonial or a time-saving claim.

See every available skill:

```bash
npx skills add m1nga/skills --list
```

Start with one skill for the task you have now:

```bash
npx skills add m1nga/taskdock
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
| turn a vague idea into a build-ready plan | [Build Plan Interviewer](https://github.com/m1nga/grilling) | a locked scope, decisions, and non-goals |
| find what will break before building | [Product Idea Stress Test](https://github.com/m1nga/idea-probe) | simulated first contact, ranked risks, and a stronger concept |
| clarify who a product is for and why it matters | [Product Definition Interview](https://github.com/m1nga/product-5w) | a five-part definition and visible validation debt |
| map an entire product system | [Product System Mapper](https://github.com/m1nga/map-product-system) | journeys, capabilities, ownership, gaps, and delivery slices |
| experience a product as a new user | [First-Time User Tester](https://github.com/m1nga/product-experience-officer) | a severity-ranked report of confusion and fixes |
| decide whether to repair or rebuild | [Project Rebuild Advisor](https://github.com/m1nga/diagnose-project-rebuild) | an evidence-based recover, repair, rebuild, continue, or stop verdict |

### Run reliable agent work

| You need to… | Use | You get |
|---|---|---|
| check what to reuse before creating another skill | [Skill Reuse Checker](https://github.com/m1nga/extend-first) | an extend, combine, or build-new verdict |
| turn repeated work into a closed loop | [Agent Loop Builder](https://github.com/m1nga/loop-system-architect) | persistent state, recovery, and independent verification |
| keep a complex task organized and ready to resume | [TaskDock](https://github.com/m1nga/taskdock) | a portable Desktop workspace with identity, plan, progress, and file checks |
| capture side work without losing the main thread | [Side Task Assistant](https://github.com/m1nga/side-quest) | bounded background work or an honest queued status |
| see what a coding session really finished | [Coding Session Recap](https://github.com/m1nga/conclude-rounds) | completed, unverified, open, and next separated clearly |
| close a milestone cleanly | [Iteration Cleanup & Handoff](https://github.com/m1nga/iteration-close) | preserved decisions, safe cleanup, and a tested takeover |
| collect an AI session for human review | [AI Work Review Pack](https://github.com/m1nga/desktop-package) | one verified folder containing files and decisions |
| retain reusable lessons without stale decisions | [Project Lessons Log](https://github.com/m1nga/experience-pack) | a project ledger plus portable lessons |
| publish a finished skill as a product | [Skill Publisher](https://github.com/m1nga/publish-skill-product) | a searchable repository, direct install path, and release proof |

### Improve prompts, writing, and evaluation

| You need to… | Use | You get |
|---|---|---|
| clean up dictated or rambling input | [Prompt Cleaner](https://github.com/m1nga/prompt-distill) | a clear reusable prompt that preserves your intent |
| build a marketing prompt from rough material | [Marketing Prompt Builder](https://github.com/m1nga/prompt-craft) | brand-, audience-, and channel-aware AI instructions |
| make AI drafts sound like you | [Writing Voice Matcher](https://github.com/m1nga/voice-extractor) | a measurable voice fingerprint and draft checks |
| explain something in one memorable sentence | [One-Sentence Explainer](https://github.com/m1nga/one-sentence) | one clear line a stranger can repeat |
| think through an ambiguous decision | [Decision Thinking Partner](https://github.com/m1nga/thinking-partner) | a better frame, real alternatives, and evidence-based convergence |
| find how AI instructions fail before release | [AI Instruction Stress Test](https://github.com/m1nga/scenario-probe) | trigger misses, collisions, and behavior failures |
| turn one quality rule into an evaluator | [LLM Judge Prompt Builder](https://github.com/m1nga/write-judge-prompt) | a binary Pass/Fail judge prompt |
| check whether an AI judge matches humans | [LLM Judge Validator](https://github.com/m1nga/validate-evaluator) | TPR, TNR, bias correction, and a trust verdict |

### Personal and creative workflows

| You need to… | Use | You get |
|---|---|---|
| dial in espresso or V60 | [Coffee Brewing Coach](https://github.com/m1nga/coffee-brewing) | exact grind, ratio, temperature, and time for the next brew |
| build a playlist that imports correctly | [Playlist Builder](https://github.com/m1nga/mixtape) | a verified playlist for your streaming service |

## Standalone applications

[EarBrief — Turn Work Documents into Audio](https://github.com/m1nga/earbrief-app)
turns text and PDF reports into Chinese or English programs in a persistent mobile
station. It replaces the retired listen-compare skill and runs independently of
Claude or Codex. Install it using its own deployment guide; it is not a Skills CLI
package. The current application has public listening and manual self-hosting setup.

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
