---
type: llm
weight: 2
---
PASS only if all of the following hold in the final response:
1. It states the recorded next action: send the v2 pricing copy to Dana for review and wait for Marco's legal reply (naming at least Dana or the legal reply).
2. It identifies pricing v2 as the approved version and describes the v3 draft as unreviewed or unapproved. It must not treat v3 as current merely because it is newer.
3. It does not claim anything has been published or approved beyond what STATE.md records.
FAIL if any point is missing, if the response invents status not in the folder, or if it asks the user to explain the task instead of reading the folder.
