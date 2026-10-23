# Build Progress Posts — Turn Verified Changes into Clear Public Updates

Use verified changes, decisions, and setbacks to make a build-in-public post people can understand, with a useful visual or demo plan when needed.

## What it does

Keeps each update tied to a real event and a supported stage. It separates a readable draft from approval and from proof of publication, while keeping visuals faithful to supplied brand references.

## Install

```sh
npx skills add m1nga/build-in-public-content
```

## When it fires

Ask: “Use $build-in-public-content to turn these private-preview notes into a progress post. Keep the preview hold and use our supplied brand assets.” Provide source notes or their locations, current stage/version, relevant brand references, and existing publication records. The skill can produce text from sufficient notes without any platform connection. Missing visual assets or recording permissions become explicit checks, not invented assets or footage.

You receive copy, a visual or shot plan if useful, and an event record connecting claims to their evidence and publication state. It does not install a scheduler, operate an account, or grant permission to publish. Existing project permissions and holds continue to apply.

## Design notes

This workflow handles the gap between engineering records and public communication: a private implementation must not become a launch claim, and a brand reference must shape the finished asset rather than merely appear in its prompt. It borrows evidence-led visual review and fact-preserving editing ideas from the fixed sources in [research notes](https://github.com/m1nga/build-in-public-content/blob/main/skills/build-in-public-content/references/sources.md). It includes no third-party source text, runtime, or assets.

## Validation

The package passed the Codex skill structure validator and product-page audit in an isolated staging location. Source-to-draft and recovery scenarios were reviewed by the author using fictional inputs; these were simulated walkthroughs, not independent user tests or live publications. Visual rendering, video playback, and platform submission were not exercised by those checks.

## Author

Created by [Ming](https://github.com/m1nga).
