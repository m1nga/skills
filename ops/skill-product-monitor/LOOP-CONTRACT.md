# Skill product monitor loop

## Objective

Keep each committed, release-marked skill in this registry synchronized with its own public
GitHub product repository, while preserving drafts and unrelated working-tree changes.

Each run succeeds when every product passes the deterministic registry, metadata, package, and
source-provenance checks, or when it records actionable findings without making an unsafe change.

## Trigger and readiness

There is no scheduled agent. A committed source-registry release invokes `scripts/publish-skill`,
which performs the remote write and then runs `scripts/monitor-products --skill <name>` plus the
named product's direct Skills CLI discovery check before it may report success. A skill is ready only when its
directory and `products.json` entry are both committed on the registry's upstream default branch.
Dirty or ambiguous skills are reported and left untouched.

## State and idempotency

Runtime state lives in the ignored `.skill-product-monitor/` directory. `RUN-STATE.json` stores the
last fully verified source commit and per-product tree hashes; `events.jsonl` is append-only. Writes
use temporary-file-and-rename, and the process lock prevents concurrent runs. The idempotency key
is the skill name plus committed source tree hash.

## Decisions and actions

The deterministic controller emits only: clean/no-op, new-ready, source-dirty, remote-drift,
metadata-drift, install-broken, or blocked. A release may use `publish-skill-product` to prepare or
repair a ready product, but must use `scripts/publish-skill` as the only remote publishing choke
point and verification trigger.

It may not rewrite a skill's purpose, owner story, evidence, readiness policy, or protected loop
contract without Ming's approval. It may not publish third-party or uncommitted work.

## Verification and recovery

After a release, a fresh scoped verifier run must re-read GitHub repository metadata, `SOURCE.json`,
the root README, and `skills/<name>/SKILL.md`, then prove direct Skills CLI discovery. Scoped release
checks do not advance the full-registry cursor. Full audits advance it only when every product passes;
failed runs preserve the last good cursor and report the exact blocker.

Stop invoking `scripts/publish-skill` and remove a stale runtime lock to kill an in-flight loop.
Retire the loop when the registry or standalone-product policy is replaced.
