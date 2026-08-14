---
name: desktop-package
description: Package this session's outcome into ONE new folder on the user's Desktop for human review — distilled standalone docs plus copies of files produced, organized so a cold reader gets task, conclusion, and open items without the conversation. Two modes — end-of-task packaging, and task-start filing where outputs accumulate during the task. Trigger on "put this in a desktop folder", "package this up so I can review it later", "leave a copy on my desktop", "save this somewhere I can find it"; Chinese — 整理到桌面 / 桌面开个文件夹 / 打包到桌面 / 放到桌面我要查收 / 桌面上给我留一份. Fires even when the ask is the last sentence of a long setup. NOT for AI-session handoff (use conversation-package), NOT a desktop cleaner ("clean up my desktop" / 整理桌面 is a different job) — it only ADDS one new folder (or, after asking, uses an existing same-topic folder) and never reorganizes existing Desktop items. For closing an iteration, run iteration-close first, then package the outputs here. Verifies delivery; degrades to a tar handoff when remote/sandboxed.
---

# desktop-package — package this task into a Desktop folder for human pickup

The user's Desktop is their pickup counter. When a task's outcome matters to them
personally, they want ONE new folder on `~/Desktop` holding everything, organized well
enough to review cold. This skill turns "everything we just did" into that folder.

The bar: two weeks from now, the user — or anyone they drag the folder to — understands
the task, the conclusion, and what's still open WITHOUT this conversation. If the folder
only makes sense next to the chat, it failed (built for the requester, not the reader —
rebuild).

Handles dictated, messy, mixed-language requests: the ask often arrives as the last
sentence after a long setup, in whatever language the user thinks in. All output follows
the user's language (templates below have EN and ZH branches).

## What goes in (reconstruct, then distill)

Walk back over the session and collect three kinds of content:

1. **Files produced this session** — wherever they live (repo, scratchpad, Downloads).
   COPY them in; never move anything out of a git repo — the repo stays the source of
   truth. Record each file's original path in the entry file.
2. **Content that only exists in the conversation** — analysis, decisions, comparisons,
   recommendations, drafts, findings. DISTILL each into a clean standalone document in
   the user's language. Distill means distill, not dump: no transcripts, no Q/A
   back-and-forth, no chat formatting. One document per coherent thing, written as if it
   were always a document.
3. **Anything the user explicitly names** ("grab those screenshots too"). An explicit
   gather instruction may MOVE files already loose on the Desktop into the folder — that
   tidying is exactly what they asked for. Everything else defaults to copy.

If the session genuinely has almost nothing worth packaging, say so instead of
manufacturing filler documents. An honest "there's not much worth packaging" beats a
padded folder.

## Same-topic folder already on the Desktop? Ask first

Before creating anything, check whether the Desktop already has a folder on the same
topic (same or near-same name, or an obviously matching subject). If it does, ask ONE
question: **merge into the existing folder, or start a new one?**

- **Merge** = ADD only. Drop new files in (numbered/dated so they sort after existing
  content), append a dated section to the entry file if one exists (or add your own entry
  file without displacing theirs). Never rename, reorder, or restructure what is already
  there.
- **New** = create a sibling folder with a date suffix. Never touch the existing one.

## Folder conventions (follow the user's habits, not a house style)

**Naming: follow the user's existing Desktop naming habits.** On first use, look at what
is already on their Desktop (`ls ~/Desktop`) and match the pattern you see — or ask.
When there are no clues, use this default:

- **One new folder per task, directly on `~/Desktop`.** Never nest inside existing
  folders.
- **Default folder name = one emoji + space + short topic name** (2–8 words / 2–8 字).
  Pick the emoji for the task's nature (⚡ urgent, 📦 packing, 🔥 active project,
  🧰 tools, 📄 docs, ✅ done — inventing a fitting one is encouraged). No dates in the
  name; dates live inside the entry file. If the name already exists, see the merge
  question above.
- **Entry file, always the same name: `START-HERE.md`** (for Chinese-language users:
  `📖 先看这个.md`). A fixed, obvious entry point beats per-package cleverness. Template
  below.
- **File names are self-explaining, in the user's language.** Emoji prefixes where they
  aid scanning, numeric prefixes (`01_`, `02_`) when reading order matters.
- **Up to ~8 items stay flat; more get numbered subfolders** (`00_materials` /
  `10_results` / `20_reference`, or the user's own filing pattern if you've seen one).
- Documents are `.md`; produced artifacts keep their original formats.

### Entry file template (EN)

```markdown
# [Task name]

- **What this is**: one line on what this package is for
- **Date / source**: YYYY-MM-DD, which session or task it came from

## Conclusion / current state
[2–5 lines, most important information first]

## What's inside
- filename — one-line description (files copied from disk note their original path)
- …one line per file

## Open items / waiting on the user
[write "none" if none]
```

### Entry file template (ZH — for Chinese-language users)

```markdown
# [任务名]

- **这是什么**：一句话说明这个包是干嘛的
- **日期 / 来源**：YYYY-MM-DD，来自哪个会话或任务

## 结论 / 当前状态
[2–5 行，最重要的信息放最前面]

## 包里有什么
- 📄 文件名 —— 一行说明（来自磁盘的文件注明原路径）
- …每个文件一行

## 还没完的 / 等用户拍板的
[没有就写「无」]
```

## Two modes

**Mode A — end-of-task packaging (default).** The user asks at or after the end of the
work: reconstruct, build the folder in one pass, deliver.

**Mode B — task-start filing.** The user declares at the START ("make a desktop folder
for this task" / 这个任务单独开个桌面文件夹): create the folder and entry file
immediately, drop outputs in as they are produced, and make the LAST act of the task
updating the entry file so its conclusion and manifest are true. For code tasks the repo
remains the only source of truth — the desktop folder holds copies, exports, and
explanations, never the only version of anything.

## The delivery moment — five checks, then hand over

Done is demonstrated, not asserted. Run all five checks before reporting:

**a. Manifest ↔ reality, both directions.** Every file listed in the entry file exists
and is non-empty (`test -s` each one), and every file actually in the folder appears in
the manifest. Fix whichever side is lying.

**b. Broken links.** `find "$PKG" -type l ! -exec test -e {} \; -print` must output
nothing. A broken symlink is a file the user cannot open.

**c. Empty shells.** `find "$PKG" -type f -size 0` must be empty. Additionally, open any
`.md` under ~200 bytes and confirm it is intentionally short — a headline with no body is
not a document; finish it or drop it from the manifest.

**d. Copy integrity.** For every file copied from disk, `cmp -s <original> <copy>`. A
failed compare means re-copy — or the original changed mid-task, in which case say so and
state which version the package holds.

**e. Environment confirmation.** Confirm the folder landed on the user's OWN Desktop. In
a remote, sandboxed, or container environment, `~/Desktop` is NOT the user's desktop —
say so explicitly, build a tarball instead
(`tar -czf <topic>.tar.gz -C "$HOME/Desktop" "<folder>"`), and tell the user exactly how
to retrieve it (download link, scp path, or host path).

Then hand over:

1. Reveal the folder if a GUI is present — `open "$PKG"` on macOS, `xdg-open "$PKG"` on
   Linux desktops, `explorer.exe` on Windows/WSL. Skip silently when headless (check e
   already told the user where things really are).
2. Report in chat: folder name + one line per file + anything that did NOT make it in and
   why.

## Boundaries

- ADDS only. Never reorganizes, renames, or deletes existing Desktop items — tidying the
  whole Desktop is a different job this skill must not drift into. Merging into an
  existing folder (after asking) still only adds.
- Copy by default. Move only what the user explicitly told it to gather, and never out of
  a repo.
- No secrets: keys, tokens, credentials, client-confidential material stay out. Desktop
  folders get screenshotted, AirDropped, and forwarded.
- For continuing work in a new AI session use `conversation-package` (if installed); this
  folder is for human eyes, not for feeding an agent.

## Engine notes

Everything above is plain shell + file writes and works the same under Claude Code,
Codex, or any agent runtime with a shell. The only engine-sensitive step is the reveal
(`open`/`xdg-open`) — optional, skipped when unavailable. Check e covers the sandbox
case for every engine.
