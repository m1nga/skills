# Live validation still required — not simulated success

The September 19 recovery patch does not change trigger descriptions or claim new
model-effectiveness results. The execution environment used for that patch had no
Claude Code or Codex executable/authenticated agent session. `check-runtimes.py`
records that boundary without reading credentials or spending model budget. Presence
of a CLI is not proof that its child processes are authenticated.

An authorized local agent should read this file, run the preflight, then use the
existing scenario-probe live-fire method in fresh sessions. Do not remove installed
skills or alter the user's home merely to run a test. Use task-owned isolated host
configuration and verify the actual loaded skill inventory before accepting a run.
Keep authentication private; do not copy credentials into the repository or CI.

For the trigger pilot, use `trigger-cases.json` with all 13 public descriptions visible
and the real local-only skill inventory separately recorded. Supply temporary project
files for requests that need them. Record actual selected skills, tool calls, file
changes and final response per case and per engine. Never report reading SKILL.md as
proof of correct automatic routing. Semantic checking and safety outcomes need an
independent reader; do not let the executing agent mark itself passed.

For the continuity pilot, follow `taskdock/product-root/evals/continuity/README.md`.
Run three conditions (plain, short agreement, TaskDock), two fresh sessions each,
with equal budgets and raw inputs. Start with one trial per condition to check the
harness, then at most three if useful. Set an explicit total spend cap before actual
calls; stop on authentication failure or a missing safety/isolation guarantee. Reuse
existing host evaluation tools instead of building another evaluation service.

The adapter calls differ by host; consult the installed CLI help and current official
headless/noninteractive docs. Record actual versions, arguments, tool permissions,
source commit, session IDs and complete private traces. Do not guess flags, copy the
old reported model version as a current result, or count scripted fixtures as agents.
The exported results must separate fixture checks, actual routing, semantic outcomes,
bytes/mode restoration, turns/tokens/cost and missing data. No result is a pass until
its underlying run exists. Do not reroute the same inherited context into a nominal
"sub-agent" and describe it as a cold session.

Completion is intentionally split: the deterministic recovery patch can be released
after its acceptance tests; live trigger and continuity claims remain NOT RUN until
the authenticated host tests are executed. A missing runtime must not cause either
invented scores or an unbounded loop of installation/authentication attempts.
