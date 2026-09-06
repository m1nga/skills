---
name: publish-skill-product
description: "Publish or repair a finished self-authored skill’s GitHub product page and install package. Use for skill releases and skill SEO/GEO experiments; preserve drafts, private context, and stable install names."
---

# Publish Skill Product

Make a finished skill easy to understand, install, and verify. Separate a working
release from evidence that people discovered or used it.

## Choose the relevant work

- **Release or repair:** read [release-workflow.md](references/release-workflow.md).
  Use the repository's existing publisher and committed source boundary. Existing
  authorization to fix published products covers the necessary verified repair.
- **Discovery or promotion:** read [growth-experiments.md](references/growth-experiments.md).
  Focus on products the owner uses or has selected, then improve a concrete example
  or discovery obstacle. Read [SEO/GEO criteria](references/seo-geo-criteria.md)
  when an external search claim or public-page change needs it.
- **Read-only audit:** inspect only the requested surfaces. Do not run the entire
  release sequence merely to give feedback.

## Keep authority and identity clear

The live registry instructions and repository remote establish the source path.
For Ming, the current registry is `/Users/m1nga/Desktop/🛠️ Skills工坊/ming-skills`.
Preserve dirty or ambiguous work. A conversation ending does not approve a release.
Never publish private task notes, invented results, or third-party source material.

Keep `name`, directory, and repository slug stable. Make display names and product
headings explain the actual task in plain language. A literal title formula is an
editorial starting point, not proof of clarity or search performance. Align README,
manifest, UI metadata, and implemented behavior. Retain existing install links.

## Evidence tools

- `scripts/audit_product_page.py <skill-dir> --product-manifest <path>` checks the
  package and product metadata. It cannot judge market demand or writing quality.
- `scripts/check_release_source.py <registry> <skill>` rejects dirty target source
  or metadata before publication while allowing unrelated local work.
- `scripts/discovery_snapshot.py <owner/repo> --query '<fixed query>' --out <file>`
  records live GitHub metadata and search results. Run `--help` for optional traffic
  and before/after comparison. Requires authenticated `gh`; uses no paid SEO service.
  Store private snapshots outside the public package.

Report changed behavior, validation, source and product commits, and observed
discovery separately. A passed release check or a search result is not an acquired
user. Reuse a successful release receipt instead of repeating the same install and
clone checks without new evidence of failure.
