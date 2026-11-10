# Compare source snapshots

Prefer Git diff, a database query or the project's existing source index when it already covers the job. The bundled helper is useful for repeated lists of saved posts, documents, cases or other local records.

Project only stable fields relevant to the job. Use a stable ID and a source version or content digest. Include a retrievable reference. Include material status, authority and relevant text changes in the version projection. Exclude rotating access tokens, irrelevant counters and capture timestamps. Keep source bodies and credentials in their original protected storage. Record the scope and whether the provider returned complete, partial or unknown coverage.

```json
{
  "scope": "saved-design-notes",
  "coverage": "partial",
  "records": [
    {"id": "note-42", "revision": "r3", "ref": "notes/42.html"}
  ]
}
```

Use the same scope and projection for both manifests. From any directory, run the script using its path in the installed skill:

```sh
python3 /path/to/context-budget/scripts/source_delta.py previous.json current.json --limit 20
```

The result contains total counts and one page of added, changed and not-seen references. When `next_offset` is present, pass that value as `--offset` to continue. Read every relevant page if the requested coverage needs it. The command reads the manifests and prints JSON. It creates no file and does not fetch any reference.

Duplicate copies of the same record are counted and collapsed. Conflicting copies of an ID or differing scope names stop comparison and identify the conflict. A changed reference is included because the previous pointer may be stale. `not_seen` only says the ID was absent from the current snapshot. Reconcile availability or deletion using the source's real state.

Use a previous reviewed version when skipping semantic review. For a metadata-only or first-seen record, inspect the body if the task requires it. Do not advance an accepted baseline until the intended work and coverage are recorded in the owning task.

For a reproducible walkthrough, run [the snapshot demo](../examples/snapshot_demo.py) from any directory. It follows every delta page, checks the same findings as a full manifest read and separates measured metadata bytes from provider usage.
