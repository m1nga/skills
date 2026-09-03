# Repository operating rules

This repository is a source registry, not the public storefront. Every released
skill must also exist as its own public repository at
`https://github.com/m1nga/<skill-name>`.

## Release contract

When a conversation produces a new skill or a material skill update and the user
has indicated that it is finished, ready, approved, or should be published:

1. Finish and validate the skill in its directory in this repository.
2. Add or update its entry in `products.json` with a problem-led title,
   search-oriented description, and focused GitHub topics.
3. Run `scripts/verify-products`.
4. Commit and push the relevant source-registry changes.
5. Run `scripts/publish-skill <skill-name>`.
6. Let `scripts/publish-skill` run the post-publish named-product monitor and the
   named skill's direct Skills CLI discovery check before saying the release is
   complete.

Do not silently publish an idea that is still exploratory, unvalidated, or not
ready for public representation. A chat ending is not itself a release signal.
Do not report a skill as published when only local files or the source registry
were updated.

## Product-page rules

- One skill equals one standalone repository and one primary search intent.
- Treat the skill name, directory, and repository slug as stable machine identifiers. Keep them
  unchanged unless the user explicitly approves a migration.
- Use `Functional identity — Concrete outcome` for the product title and README H1.
- Give every skill a two-to-five-word plain-language `agents/openai.yaml` display name and a
  25–64 character short description that says what it does or produces.
- A stranger who sees only the display name and short description should understand the use case
  and expected result within three seconds; internal metaphors alone do not pass.
- Lead with the user's problem and outcome, not with Ming's collection or skill
  taxonomy.
- The repository owner and a short author section establish who made it; the
  product explanation remains primary.
- Keep the reason for the design in the individual README's design notes.
- Use `npx skills add m1nga/<skill-name>` as the canonical install command.
- Related-skill links must point to the related standalone repository.

## Publish-time monitor contract

- A committed `products.json` entry plus the matching committed skill directory is the explicit
  release marker used by the automated monitor.
- `scripts/publish-skill` runs `scripts/monitor-products --skill <skill-name>` after every
  publication for deterministic drift detection, then checks the named standalone repository
  through the Skills CLI. Runtime state is local and ignored under `.skill-product-monitor/`; the
  canonical contract is
  `ops/skill-product-monitor/loop.contract.json`.
- There is no scheduled polling job. A release must report and skip dirty, unregistered, private,
  third-party, or ambiguous skills.
- The monitor cannot alter a product's purpose, owner story, evidence, or release policy without
  explicit approval.
