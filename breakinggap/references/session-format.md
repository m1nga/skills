# Local helper contract (schema version 1)

Python 3.9+, standard library only. Run the installed `scripts/gap.py` by its absolute path from any working directory. All commands emit JSON; errors exit nonzero. `--root` selects the existing project directory, never the skill installation directory. Input/proposal/output filenames are interpreted relative to the shell's working directory. Source paths are interpreted relative to `--root`.

```sh
python3 /path/to/breakinggap/scripts/gap.py recommend --root /path/to/project --input /path/to/input.json --minutes 12 --intent any --out /path/to/proposal.json
python3 /path/to/breakinggap/scripts/gap.py start --root /path/to/project --proposal /path/to/proposal.json
python3 /path/to/breakinggap/scripts/gap.py checkpoint --root /path/to/project --state paused --note 'Saved draft paragraph' --next 'Read the final sentence, then continue'
python3 /path/to/breakinggap/scripts/gap.py resume --root /path/to/project
```

Use `python` on systems where it names Python 3.9+. `--out` is optional: recommendation otherwise reads only. Output paths must have an existing parent. Output is created exclusively: existing files (including sources and input JSON) are never overwritten. Paths inside `.breakinggap` are refused. Journal files are created with mode 0600 and the private directory uses 0700 on POSIX systems; Windows permissions follow its filesystem policies.

## Input

```json
{
  "schema_version": 1,
  "project": {"id": "report", "title": "Research report"},
  "current_work": {
    "title": "Build report preview",
    "return_to": "Review the preview when available",
    "agent_status": "running"
  },
  "candidates": [{
    "id": "draft-opening",
    "kind": "advance",
    "title": "Draft the opening paragraph",
    "action": "Write one paragraph in the existing notes",
    "done_when": "One paragraph is saved",
    "pause_after": "Stop after the paragraph",
    "resume_hint": "Read the last sentence before continuing",
    "project": "report",
    "source": {"path": "notes/plan.md", "sha256": "REPLACE_WITH_ACTUAL_FILE_SHA256"},
    "state": "ready",
    "owner": "human",
    "authorized": true,
    "interruptible": true,
    "conflict_check": "clear",
    "minutes": {"setup": 1, "work": 5, "wrap": 1}
  }]
}
```

The caller constructs candidates from real project evidence. `project` on a candidate is a project ID string. IDs must be unique. Text fields must be nonempty. `kind` is `advance`, `resume`, or `learn`; `--intent` defaults to `any` and otherwise matches exactly. `state` vocabulary is `ready|held|blocked|done|unknown`; owner vocabulary is `human|either|agent`. Only `ready`, `human|either`, explicit boolean authorization/interruptibility and `clear` conflict checks qualify. Minutes are nonnegative integers, with positive work time. Setup + work + wrap must fit the supplied budget minus a two-minute return reserve. Boolean values are not minutes.

Every candidate needs a current local regular file, relative to the selected root, without traversal or symlinks. SHA-256 must match the current bytes. Missing, changed, or unsafe sources exclude a candidate. The helper checks file identity, not the truth of its contents or assertions. It does not infer authorization from file presence, grant permissions, independently discover conflicts, watch agents, contact services, or execute recommended work.

Recommendation output includes `schema_version`, `status`, `project`, `current_work`, `budget_minutes`, `return_reserve_minutes`, `chosen` (candidate or null), `excluded` (IDs with reasons), and `limitations`. Current-project candidates rank first, followed by the shortest complete time and stable ID order. No eligible candidate produces `no_match`. A caller-reported `waiting_for_user` returns `needs_attention`; `finished` returns `ready_to_review`, both without a side activity. `unknown` relies on the user's declared gap; it is not monitoring evidence.

## Private journal and recovery

`start` revalidates schema, budget, status, eligibility and source freshness. It atomically writes `<root>/.breakinggap/session.json`, containing `schema_version: 1`, current `session`, and completed `history`. A session contains a UUID, UTC timestamps, state, the original proposal (including chosen activity and return point), and notes. Keep this private directory out of public releases and version control. No runtime journal is shipped in the skill.

Only one active or paused session is allowed. Repeating the identical proposal is idempotent. Another proposal cannot replace ongoing work. After a completed session, the next start retains the previous session in history. Checkpoints record exact note/next text plus a timestamp; an identical last checkpoint is idempotent. They do not mark any canonical task complete. `resume` reports stored state and current source warnings without restarting or executing anything; `done` stays done. A changed source must be reconciled by the caller before acting on old instructions.

Writers and resume reads use an exclusive `.breakinggap/session.lock`. A busy lock fails clearly and is never automatically removed. After a crash, verify that no writer is running before manually removing a stale lock. Corrupt/unsupported journals are refused and preserved; recover from a known backup or explicitly inspect and repair them. Atomic replacement prevents partial JSON writes; it does not claim protection against an adversarial process changing paths during file operations, network-filesystem locking failures, or disk/power failure guarantees.
