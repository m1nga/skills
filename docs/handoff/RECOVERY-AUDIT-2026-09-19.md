# 2026-09-19 recovery audit — execution and handoff

## Status

The deterministic fixes are merged and published. The live-model continuity and routing
pilots were prepared here and have since been **executed on Claude** on an authenticated
macOS host; see the executed-acceptance section at the end of this file and
`ops/skill-quality/live-pilot/RESULTS-2026-09-19.md`. The Codex side remains **blocked**
(runtime not installed). The executed results are a single small sample: they found
failures, and they are still not release-success or general productivity evidence.

- Source implementation: `2575e0c182c0a424177409e942696527ad6dd905`, merged through [PR #1](https://github.com/m1nga/skills/pull/1).
- Published TaskDock: `8da92274e8d84b9372333ae4921c97379da76e15` in `m1nga/taskdock`.
- Plugin version: `2026.9.20` (a patch-version increment, not a claim that execution happened on September 20).
- Published `SOURCE.json`: source commit `2575e0c182c0`, source tree `fd257986546a6172aed8fb1ee6824dca9692b2d0`.
- This handoff is outside the skill package; adding it does not change the published source tree.

## What actually changed

1. `day-close` remains a local-only decision. Its two tracked files were removed from current public distribution, not registered as a fourteenth public product. The orphan-product check remains enabled. Git history was not rewritten. No user-machine files or installations were changed.
2. TaskDock retains operation identity, recovery location, structured rollback arguments and a shell-specific command after failures occurring after planning. Partial execution no longer says nothing moved. Non-UTF-8 reference text is rejected before apply. No automatic rollback overwrites newer work.
3. Resume discovers pending or damaged operation records read-only, using the current task location after a move; it does not hash every completed historical preimage. Existing transaction locks, preimages, symlink/path restrictions and conflicting-edit checks remain.
4. POSIX and PowerShell rollback commands preserve literal path characters. Internal operation paths use portable POSIX notation. Platform-specific file modes are not presented as Windows POSIX guarantees.
5. Root-overlay exclusions are anchored so nested `evals/README.md` files are published. Metadata that already matches is not needlessly rewritten; real drift still requires repair.
6. Evaluation wording no longer infers an efficiency advantage from overlapping turn ranges. A neutral three-arm/two-stage continuity protocol and eight Chinese routing cases were added without fabricated outcomes. Other skill trigger descriptions and existing retirements were not rewritten.

## Executed acceptance

The final implementation commit passed [the main-branch filesystem matrix](https://github.com/m1nga/skills/actions/runs/35428259426). Linux Python 3.8 and 3.13, macOS Python 3.13, and Windows Python 3.13 all passed their applicable tests and an executable demo. CI uses `PYTHONUTF8=1`.

- 52 TaskDock tests collected (37 existing plus 15 regression cases), with platform-specific skips. Windows executes its actual PowerShell command test; POSIX executes its own shell tests. Skips are not extra passes.
- 21 existing publisher tests and 6 packaging/fixture integration tests passed.
- All 13 public product quality gates passed without suppressing the missing-product check.
- Design, release and research examples performed apply/rollback and verified visible-file byte restoration.

[The publication and installation run](https://github.com/m1nga/taskdock/actions/runs/35428296142) passed the existing `scripts/publish-skill taskdock` contract, its remote monitor and direct Skills CLI discovery. A fresh clone of the published repository passed the 52-test suite on Linux (one Windows-only skip). Claude Code 2.1.278 installed the actual GitHub plugin, listed `taskdock@taskdock` version `2026.9.20`, then uninstalled it and removed the test marketplace. No authenticated model session was used for that installation test.

The downloaded publication artifact was checksum-verified, then 47 tracked skill/overlay files were compared byte-for-byte with the accepted source. The root README is intentionally transformed by the publisher. Untracked local Python caches were excluded from this comparison, not treated as release files.

The initial content-push attempt was rejected because the Actions token cannot edit workflows. Workflow changes were submitted separately through the authorized GitHub connector; token permissions were not expanded. Temporary source transport files and workflows are absent from main.

## Local-only recovery

The conversation contains `day-close-local-backup.zip`, verified before source removal. Archive SHA-256: `eae84f65f01ef7a0558eb0edf3801facc5a3696e47a4fa2d795d91e399b89661`.

Independent recovery source: commit `cd4a5bd51ce49cf8bc8ee68cc98d0644e77a794e`, paths `day-close/SKILL.md` and `day-close/agents/openai.yaml`. Restore to a user-approved local/private location, not back into public distribution. Preserve any existing local customization; do not overwrite it blindly. A backup in this conversation is not confirmation of a Mac-local installation or backup.

## Remaining acceptance — as handed off on 2026-09-19 (historical, superseded below)

An authorized local executor should read `ops/skill-quality/live-pilot/README.md`, `trigger-cases.json`, and `taskdock/product-root/evals/continuity/README.md`.

- Run the three-arm continuity pilot in genuinely separate authenticated Claude/Codex sessions: plain host, short work agreement, full TaskDock. Stage A starts with raw materials, not prebuilt TaskDock records; stage B receives only persisted work plus controlled changes. Record per-run costs and actual outcomes, not TaskDock-specific filenames as wins.
- Run the eight Chinese routing cases with the real co-installed skill inventory in both hosts. Static predictions are not live selection results.
- Verify/refresh this user's Mac installations only from an executor that actually has access; preserve day-close locally before a pull could remove its source-backed installation.

The current ChatGPT container had no authenticated Claude/Codex execution environment or model-subagent interface. The remote plugin installation test does not remove that limitation. No model-evaluation spend or productivity advantage is claimed. Do not rerun broad skill rewrites, restore retired repositories, add telemetry, or change app designs while closing these specific checks.

## Remaining acceptance — executed on an authenticated macOS host, 2026-09-19

The Claude-side items above are now run. Full sanitized evidence, provenance, deviations
and cost are in `ops/skill-quality/live-pilot/RESULTS-2026-09-19.md`. The historical
statements above are retained as written at handoff time and are not edited.

### Host installation, verified

- `day-close` on that Mac was installed by symlink into the source repository working
  tree, which current `main` no longer contains — a pull would have removed it. Its two
  files were byte-identical to `cd4a5bd…` with no local customization. Contents were
  copied to a private local backup with per-file sha256 verification, the original link
  target was recorded, and the installation now points at an independent local copy.
  Nothing about it was added to public distribution.
- The host's TaskDock was the **pre-fix `cd4a5bd` build**, missing `recovery.py` and the
  two recovery test modules. It was backed up and refreshed in place by its existing
  install method; its payload is now byte-identical to the published accepted package.
  No duplicate plugin installation was added.
- `python3 -m unittest` on that host: **52 tests, OK, 1 platform skip**, on Python 3.9.6.
  CI passing on its own runners did not establish this.

### Live pilots

- Continuity, three conditions × two stages, one trial each: executed on Claude with
  verified per-arm skill inventories. All three conditions, including the plain host,
  identified the superseding decision and refused publication. No continuity advantage
  for the full skill was demonstrated on this fixture; it cost about 4.9× the plain arm.
- Trigger, eight Chinese cases on the real co-installed inventory: seven routed as
  expected and every prohibition held. One routing failure — the explicit file-organizing
  request with an executable-undo requirement did **not** select TaskDock.
- Independent semantic review was performed by a cold session given only the rubrics and
  the fact files, with no executor commentary.

### Product defects found by execution, not by inspection

1. The recorded one-line `rollback` refuses with `conflict` after the operation's own
   prescribed note updates, so the published recovery command fails at the moment a user
   would use it. Contributing details: preimage blobs restore mode `0600` while
   `rollback` also checks POSIX mode, and link repair touches `STATE.md`. The underlying
   safety behaviour is correct — a clean rollback restores bytes and modes exactly, and a
   rollback facing a newer edit refuses, preserves it and changes nothing.
2. `rollback_argv` embeds absolute paths, so the recorded command cannot be run against a
   copy without editing it. Two of three arms' supplied undo commands had this problem.

These are recorded for the repository's normal review and release process; no trigger
descriptions or retirements were rewritten as part of this acceptance run.

### Still not run

- Both Codex pilots: the `codex` executable is not installed on that host. **Blocked**,
  not failed. Nothing in these results transfers to Codex.
- Cross-engine cost comparison.
- Any claim of general speed, cost or reliability advantage: one trial per arm.
