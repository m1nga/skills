---
type: llm
---
PASS if the response answers the question directly (a symlink is a separate file holding a path that can dangle and can point to directories; a hard link is another directory entry for the same inode, same filesystem, files only) and does not propose creating a folder, plan or workspace. FAIL if it sets up any task structure or asks unrelated clarifying questions.
