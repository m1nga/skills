# Iteration Cleanup & Handoff — Preserve Decisions and Remove Dead Work

Close an iteration so nothing is lost and nothing dead survives — and prove, with an actual test, that a stranger could take the repo over.

## What it does

Runs a five-phase close at the end of an iteration, sprint, or milestone. It distills chat-born
decisions into the repo's own record, then deletes superseded files — after showing you the full
deletion list and getting your yes (untracked files go to a quarantine directory, never straight
to `rm`, because git history can't recover what was never committed). It verifies upload and
knowledge-completeness as two separate channels, including a cold-start probe: a fresh agent
reads the repo with zero context and must answer four questions correctly, or the docs get fixed
and it runs again. Then it rehearses the one-command bootstrap on a fresh clone, tags the
iteration, and hands you a paste-ready kickoff prompt for the next one. If all you want is the
cleanup, it runs that phase alone.

## When it fires

- "Let's close out this iteration."
- "Wrap up this sprint and clear out the dead files."
- "We shipped the slice — could a fresh machine pick this up tomorrow?"
- "Clean the superseded files out of the repo."
- 「这个迭代做完了，收口」
- 「甩包袱，清旧账」

It stays quiet on a casual "calling it a day" and on questions about how to publish a package —
those aren't iteration closes.

## Install

```
npx skills add m1nga/iteration-close
```

## Example

> **You:** slice 3 is approved — close the iteration.
>
> **Claude:** reads the repo's entry doc, banks four chat decisions into `DECISIONS.md`, then
> shows a 12-line deletion inventory (`path | why dead | what supersedes it`) and waits. You
> strike two lines and approve the rest. Ten tracked files go via `git rm` in themed commits; one
> untracked scratch dir moves to `.iteration-quarantine/`. A fresh subagent reads the repo cold
> and scores 4/4 on the takeover probe — after one doc fix and a re-run. A scratch clone
> bootstraps green with zero manual steps. `iter-3-payments` gets tagged, and you get a kickoff
> prompt for slice 4.

## Works well with

- [`conclude-rounds`](https://github.com/m1nga/conclude-rounds) — recap the recent conversation first, so Phase 1 has a clean list of decisions to bank.
- [`diagnose-project-rebuild`](https://github.com/m1nga/diagnose-project-rebuild) — when the repo is too tangled to close, diagnose it first; close later.
- [`map-product-system`](https://github.com/m1nga/map-product-system) — the architecture note Phase 1 keeps current pairs naturally with a full product-system map.

## Design notes

This skill exists because of two real losses in a solo builder's history: a working pipeline that
lived only in a scratchpad and died with the session, and a deprecated directory that sat around
for weeks until the docs told two different truths. Each opinionated rule traces back to a scar:

- **Distill before delete.** Nothing is removed until its lesson is banked in a tracked file. The
  phase order is the safety mechanism, not a style preference.
- **Git history is the only archive.** `_archive/` dirs and `.bak` files rot into second truths.
  Recovery for tracked files is one `git revert` away — so tracked files may die cleanly.
- **Untracked files get quarantined, not deleted.** Git can't resurrect what was never committed.
  That asymmetry is the data-safety line, and the skill refuses to cross it.
- **The agent never presses irreversible buttons.** The complete deletion list is shown, and
  nothing runs without an explicit yes. Partial approval works — it deletes only what you approved.
- **"Anyone could take over" is tested, not hoped.** A context-free reader either scores 4/4 on
  the takeover probe, or every miss is treated as a documentation bug and fixed before re-running.

## Field-tested

Probed 9 scenarios across 5 personas · 5 fired correctly · 2 correctly stayed quiet · 2 flagged (one degraded-world path, one coin-flip; fixes queued).

> **"今天收工了，明天见" ("calling it a day — see you tomorrow")**
> → Correctly stayed quiet. An end-of-day sign-off is not an iteration close; the description now excludes it by name.

> **"清旧账，把没用的旧文件清一清" ("clear out the old junk files")**
> → Fired in shed-only mode: built the full deletion inventory, waited for an explicit yes before removing anything, and moved untracked files to quarantine instead of `rm` — git history can't resurrect what was never committed.

> **"how do I publish an npm package?"**
> → Correctly stayed quiet. Publish-a-package questions are explicitly excluded — this skill closes iterations, it doesn't teach packaging.

Probe method: [scenario-probe](https://github.com/m1nga/scenario-probe/)
