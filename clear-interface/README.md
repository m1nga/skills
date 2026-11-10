# Clear Interface — Design Focused Web and Product UI

Make a page easier to understand and use by resolving information hierarchy, redundant copy, and decorative clutter together.

## What it does

Clear Interface is an agent skill for new web pages and existing product interfaces. It connects five decisions: understand the task, decide what belongs, build hierarchy, write clear copy, and verify the affected journey.

It uses one content decision: **keep, merge, defer, or remove**. Necessary consequences and recovery information remain available. The result can be a design proposal, revised UI copy, or an implemented change, depending on your request.

## Who it's for

Use it when a page feels overexplained, every card has a redundant introduction, or a new design needs clear structure from the start. It supports landing pages, forms, settings, dashboards, and content pages.

This is a focused interface skill, not a complete frontend toolchain, brand research service, or substitute for a usability study. It follows your design system and requested scope. No other skill, account, launcher, or service is required.

## Install

```sh
npx skills add m1nga/clear-interface
```

In Codex, invoke it with a concrete target:

```text
$clear-interface Simplify the settings page. Focus on copy and redundant labels; preserve layout and behavior.
```

For a new page:

```text
$clear-interface Design the booking page from this brief. Make availability, total price, and cancellation terms easy to understand before booking.
```

For chat tools that do not load skills, paste the [standalone prompt](https://github.com/m1nga/clear-interface/blob/main/skills/clear-interface/prompt.md) with your brief. The prompt is a portable alternative; the skill does not need to load it.

## Example

Input: a notification settings section titled “Notifications,” followed by “Manage your notification settings here,” a field labeled “Email notifications,” and helper text “Enable email notifications to receive notifications by email.”

Result: keep the section title and field label; remove the two restatements. Keep an additional sentence if it explains a real distinction, such as which events generate an email. Do not invent those events.

A deletion warning is different: preserve what will be deleted and whether recovery is possible. A request to shorten copy does not authorize removing the capability or changing its consequences.

## Design notes

This skill grew from a concrete problem: generated interfaces often add labels, summaries, and explanatory text to occupy empty space. Combining three large instruction sets would reproduce the same problem inside the skill.

The compact workflow learns from [Impeccable](https://github.com/pbakaus/impeccable), [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), and [Christopher Greer's UX Writing](https://github.com/content-designer/ux-writing-skill). It is independently written and does not bundle their code or instruction text.

It retains task-based simplification, meaningful visual hierarchy, and actionable language. It does not adopt rigid font counts, forced single-column layouts, fixed English word limits, or percentage-based comprehension guarantees. It also preserves purposeful repetition across steps and useful brand expression.

## Validation

Reviewed with simulated requests covering ordinary cleanup, destructive actions, dense dashboards, missing product facts, screenshot-only input, scope boundaries, and trigger overlap. These are author walkthroughs, not independent user tests or measured usability gains.

Release checks validate skill metadata, packaging, source identity, and direct Skills CLI discovery. They do not prove that every host will select the skill automatically or that a design is accessible without inspecting its implementation.

## Author

Built by [Ming](https://github.com/m1nga).

