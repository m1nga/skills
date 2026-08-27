# Publish a Finished Skill as Its Own Searchable Product

Turn one finished agent skill into one independent GitHub product: its own repository, problem-led
page, real origin story, direct install command, SEO/GEO metadata, and verified release evidence.

## What it does

`publish-skill-product` takes over after skill development is genuinely finished. It audits the
skill and its public story, writes or repairs the individual product metadata, uses the repository's
confirmed publisher, and verifies that the remote repository contains both a human product page and
a complete installable package. Its monitor mode also repairs committed products that drift out of
sync without touching drafts or unrelated work.

## When it fires

- “This skill is finished — publish it as its own GitHub product.”
- “Check whether every skill page has a real story and can be found independently.”
- “Monitor my skills repo and fix new products that missed SEO/GEO or standalone publishing.”
- 「这个 skill 定稿了，自动上传并做成单独产品页」
- 「检查新发的 skills 有没有独立仓库、介绍、故事和搜索入口」

It does not create the skill itself — use `skill-creator` for that. It does not publish exploratory
ideas, private context, third-party skills, ordinary code packages, or arbitrary git changes.

## Install

```bash
npx skills add m1nga/publish-skill-product
```

## Example

> **User:** `map-product-system` is ready. Publish it, and make sure someone searching for a way to
> understand their whole product can find the skill rather than a Ming skills collection page.
>
> **Agent:** Validates the skill and product story, updates the problem-led repository metadata,
> commits only the named source changes, publishes `m1nga/map-product-system`, proves the remote
> `skills/map-product-system/SKILL.md` package is complete, runs the direct CLI discovery check, and
> reports search/index evidence separately from release success.

## Works well with

- [`skill-creator`](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) — builds
  the skill; this skill owns the public product release after approval.
- [`scenario-probe`](https://github.com/m1nga/scenario-probe) — stress-tests the public trigger and
  body before release.
- [`loop-system-architect`](https://github.com/m1nga/loop-system-architect) — defines the persistent
  monitoring contract, cursor, recovery, and verification loop.

## Design notes

This exists because a repository can truthfully say “every skill has a README” while still behaving
like one collection page. The first release of Ming's skills did exactly that: every skill lived in
one repository, so search engines and strangers met the collection before they met the problem each
skill solved. Splitting repositories fixed the URL boundary, but the release logic still lived in a
shell script and one global instruction. That meant it could publish code without independently
checking the product story, install package, discovery state, or future drift. This skill makes that
last mile an explicit, testable product contract.

## Field-tested

The release workflow has published and remotely verified 23 standalone skill repositories. The
deterministic monitor completed a full 23/23 source, metadata, README, and package audit, and its
daily local Codex automation is active. Search indexing remains a separately observed status, not a
release claim.
