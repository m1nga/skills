# Ming's skill source registry

This repository is the source of truth for Ming's agent skills. It is not the
storefront: every released skill is published as its own standalone GitHub
repository, with its own product page, search intent, metadata, install command,
and release history.

## Find a skill by the problem you have

[Browse the standalone skill products](https://github.com/m1nga?tab=repositories&q=topic%3Am1nga-skill)

For example:

- [Diagnose a confused project before rebuilding it](https://github.com/m1nga/diagnose-project-rebuild)
- [Map a product end to end](https://github.com/m1nga/map-product-system)

Install directly from a product repository:

```bash
npx skills add m1nga/<skill-name>
```

## How releases work

Each directory in this registry contains one skill. The product metadata lives
in [`products.json`](products.json), and `scripts/publish-skill` publishes that
directory to `github.com/m1nga/<skill-name>`.

```bash
scripts/verify-products
scripts/publish-skill diagnose-project-rebuild
```

New skills are not considered released until both the source registry and the
standalone product repository have been updated and verified.

## Author and method

Built by [Ming](https://github.com/m1nga) from real solo-builder workflows. The
reasoning behind each skill belongs on that skill's own product page, under its
design notes, rather than on a collection homepage.

MIT licensed.
