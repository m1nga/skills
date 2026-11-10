# Start in your own repository

Installation supplies review instructions and diagnostic helpers. It does not
install Ming's registry publisher or grant access to his GitHub account.

Try: `Use $publish-skill-product to review ./my-skill for YOUR_OWNER/my-skill.
Show the first-use and packaging gaps. Do not publish yet.` Replace owner and path
with your own. This first result needs no GitHub mutation.

Resolve the registry root from the selected checkout, the source repository from
its verified remote, the stable slug from the selected SKILL.md, and the public
target from the owner's request. Read that owner's release policy and documented
publisher. Do not copy Ming's identity, home path, referral policy or publication
authority into another project. A dirty target or mismatched remote stops release.

The bundled auditor works without a publisher:

```sh
python3 <installed-skill>/scripts/audit_product_page.py /absolute/path/my-skill
```

It checks structure, not successful first use. Missing manifest metadata remains
an explicit warning until real metadata is available. The fingerprint gate expects
`products.json`, `ops/skill-quality/baseline.json`, and
`ops/skill-quality/reviews/<skill>.json`; it is an optional integration for other
registries, not a universal installer. Reuse an existing compatible publisher.
If none exists, deliver the readiness review and adapt a release route only within
the owner's requested scope. Confirm license, committed packaging, remote content
and direct installation before claiming release success.
