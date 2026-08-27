# Skill product monitor loop

## Objective

Keep each committed, release-marked skill in this registry synchronized with its own public
GitHub product repository, while preserving drafts and unrelated working-tree changes.

Each run succeeds when every product passes the deterministic registry, metadata, package, and
source-provenance checks, or when it records actionable findings without making an unsafe change.

## Trigger and readiness

The scheduled agent runs daily. `scripts/monitor-products` performs the cheap deterministic pass
before any semantic repair. A skill is ready only when its directory and `products.json` entry are
both committed on the registry's upstream default branch. Dirty or ambiguous skills are reported
and left untouched.

## State and idempotency

Runtime state lives in the ignored `.skill-product-monitor/` directory. `RUN-STATE.json` stores the
last fully verified source commit and per-product tree hashes; `events.jsonl` is append-only. Writes
use temporary-file-and-rename, and the process lock prevents concurrent runs. The idempotency key
is the skill name plus committed source tree hash.

## Decisions and actions

The deterministic controller emits only: clean/no-op, new-ready, source-dirty, remote-drift,
metadata-drift, install-broken, or blocked. A Codex run may use `publish-skill-product` to repair a
ready product, but must use `scripts/publish-skill` as the only remote publishing choke point.

It may not rewrite a skill's purpose, owner story, evidence, readiness policy, or protected loop
contract without Ming's approval. It may not publish third-party or uncommitted work.

## Verification and recovery

After a repair, a fresh verifier run must re-read GitHub repository metadata, `SOURCE.json`, the
root README, and `skills/<name>/SKILL.md`. The cursor advances only if every product passes. Failed
runs preserve the last good cursor, write an event, and stop after two same-class attempts.

Disable the scheduled automation and remove a stale runtime lock to kill the loop. Retire the loop
when the registry or standalone-product policy is replaced.
