# Can a boolean pass your agent's turn-budget check?

A Python type check can accept `True` as an integer. Our loop contract linter once
accepted boolean budgets and some non-finite costs. The corrected linter rejects
these inputs. Here is a small reproduction using the actual shipped code.

```bash
git clone https://github.com/m1nga/skills.git ming-skills
cd ming-skills
python3 examples/loop-budget-check.py
```

Expected output, verified on September 7, 2026:

```text
PASS: valid integer budget accepted.
PASS: boolean budget rejected.
This checks contract inputs. It does not start a scheduler or prove runtime recovery.
```

The script modifies a disposable copy of the example contract in the current
directory, then removes that copy. It does not edit your real agent configuration.
The [fix](https://github.com/m1nga/skills/commit/aa780b0df82f5002c9ec364f55202af3c8b95436)
also handles malformed role lists and non-finite costs; this short demo exercises
only the integer-versus-boolean case.

Use [loop-system-architect](https://github.com/m1nga/loop-system-architect) when
designing the goal, triggers, state, authority and verification of repeated agent
work. Start with this demonstration if you want to inspect one concrete check first.

```bash
npx skills add m1nga/loop-system-architect
```

If a real workflow exposes another counterexample, [report the smallest safe
reproduction](https://github.com/m1nga/loop-system-architect/issues/new). Include the
command and actual error with credentials and private data removed. A voluntary
star is welcome if the skill proves useful.
