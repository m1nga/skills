---
type: llm
weight: 2
focus: files
---
You see the list of files the agent created. PASS only if:
1. Files were created under team-notes-research/ (not scattered elsewhere).
2. There is exactly one obvious entry point that tells a newcomer where to resume, a separate file or section holding current state, and a plan file.
FAIL if no files were created, if there is only a single loose plan file with no state or resume entry, or if files were created outside team-notes-research/.
