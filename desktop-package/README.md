# desktop-package

**Turns a finished chat into one reviewable folder on your Desktop — and runs five checks to prove every file actually landed.**

## What it does

You finish a working session and want the outcome somewhere you'll actually look:
one new folder on your Desktop. This skill walks back over the session, copies in
every file that was produced, and distills the parts that only exist in the chat
(decisions, comparisons, findings) into standalone documents — no transcripts, no
Q/A dumps. A fixed entry file (`START-HERE.md`) states the conclusion, lists every
file, and names what's still open. The bar it holds itself to: a cold reader — you
in two weeks, or whoever you drag the folder to — gets the whole picture without
the conversation.

## When it fires

- "put this in a desktop folder for me"
- "package this up so I can review it later"
- "make a folder for this task — I'll look at it tonight"
- "save all of this somewhere I can find it"
- 整理到桌面 / 桌面开个文件夹放着我要查收

It will not fire on "clean up my desktop" — it only ever adds one folder and never
touches your existing Desktop items.

## Install

```
npx skills add ming4uk/skills@desktop-package
```

## Example

> **You:** (after a long session comparing three CRM options) ok package this up so I can review it tonight
>
> **Claude:** creates `📦 CRM decision/` on your Desktop containing `START-HERE.md`
> (conclusion: option B, two open questions), `01_comparison-table.md`,
> `02_pricing-notes.md`, and a copy of the vendor PDF with its original path noted —
> then verifies the manifest matches the files, none are empty or broken, copies
> match their originals, and this is really your Desktop (not a sandbox) before
> opening the folder in Finder.

## Works well with

- **conversation-package** — same reconstruct-the-session muscle, opposite audience:
  that one packages for a *future AI session* to resume the work; this one packages
  for *human* pickup. End of a big task, you often want both.
- **iteration-close** — closing a product iteration is its own ritual; use that for
  the repo-side wrap-up and this for the copy you want on your Desktop.

## Design notes

Two failure modes shaped this skill, both from real solo-builder sessions. First:
packages that read fine in the chat but were incomprehensible a week later —
hence the cold-reader bar and the rule that conversation content gets rewritten as
documents, never pasted as transcript. Second: packages that *claimed* delivery but
shipped empty files, broken symlinks, or landed inside a sandbox the user could
never see — hence the five delivery checks (manifest↔files both directions,
broken-link scan, empty-shell scan, byte-compare on copies, and an explicit "is
this actually the user's Desktop?" confirmation that falls back to a tarball with
retrieval instructions). "Done" is demonstrated, not asserted.

## Field-tested

Probed 7 scenarios across 6 personas · 5 fired correctly · 2 correctly stayed quiet.

> **"……行，就这样定了，整理到桌面，我晚上查收"** — the real ask buried in the last sentence after three paragraphs of setup → Fired on the exact phrase, distilled the session into one folder with a `📖 先看这个.md` entry file, and ran all five delivery checks before saying "done."

> **"打包到桌面给我"** — but the session was running inside a remote container, where `~/Desktop` is not the user's desktop → It said so explicitly, packaged a tarball instead, and handed over retrieval instructions rather than claiming a delivery that never landed.

> **"Clean up my desktop, it's a mess"** → Stayed quiet. One character separates 整理**到**桌面 (package to desktop — fires) from 整理桌面 (tidy my desktop — never fires); the skill only ever *adds* one folder and never reorganizes what's already there.

Probe method: [scenario-probe](../scenario-probe/)
