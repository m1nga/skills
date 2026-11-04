# RedBot — Find the Good Thing You Saved

You saved something useful, but cannot find it when you need it. RedBot helps you choose **one relevant source, see the useful part and take a next step**.

**[Try RedBot on SideCourt](https://sidecourt.space/drops/redbot/) · [Open the app](https://sidecourt.space/drops/redbot/app/) · [User test](https://sidecourt.space/drops/redbot/test/)**

**Version 1.9.3 is an invitation-only account test.** Connect your own Xiaohongshu account, see saved cards arrive during a scan and read selected post text. Chinese-first interface with an English switch. The small test host must be online; full collection coverage and same-phone QR sign-in are not yet verified.

## Who it's for

People who collect design references, methods or tools and then struggle to decide what to use. Use the web app for your own saves. Use the companion skill inside an authorized AI assistant for a selected post, supplied notes or a RedBot backup.

## Start with your account

1. Open the invitation link you received from Ming. Its code is filled into the visible invitation field; you can also choose **连接小红书 / Connect Xiaohongshu** and enter the code yourself. An existing connected session does not need the invitation again.
2. Review how the test stores your data. Scan the login code with Xiaohongshu and confirm in that app.
3. RedBot shows the observed count and adds saved cards as batches arrive. You can browse and search the cards already received while scanning continues, or stop and keep them. You do not need to upload files or copy cookies.
4. Describe what you want to do in **现在想做 / For now**, or browse **我的收藏 / My saves**.
5. Open a relevant save. With your account connected, RedBot starts one read of that selected item: post text for a text save, or speech and sampled on-screen text for a video. Scanning the list does not read every save.
6. Read the persistent status inside the detail view. A failed, cancelled or empty read stays distinct from success; retry or cancel there. Timestamped speech and sampled OCR remain separate evidence. Source-dependent prompts become available after useful source arrives. If the matching job disappears after another job or a service restart, RedBot checks the selected item’s outcome for this read instead of leaving it running forever. An older successful result cannot stand in for the new attempt. This check is read-only and never resubmits the read automatically.
7. Inspect the goal requirements and actual supporting passages, check cost/promotion cues, then save a supported plan or create an editable prompt for your project. A title-only source must be read before it can be kept as a supported plan.

An invitation opens a test slot; a separate random session credential protects each visitor's data. The default host supports three simultaneous sessions. No invitation? Original example notes let you try the interface without signing in. Manual JSON backup is a recovery option.

## What it does

| Need | What RedBot does |
|---|---|
| Too many saves to choose from | Starts with a goal and one supported suggestion |
| Cannot remember the exact words | Optional on-device multilingual semantic matching |
| Do not know which part matters | Shows a bounded extract of text already retrieved |
| “Free” may have conditions | Quotes cost/promotion cues and can check public GitHub facts |
| Want to use an idea in a project | Builds an editable, source-grounded Codex prompt |
| Want to continue later | Keeps a plan and personal notes in this browser |
| Want to organize | Search, topics, collections, favorites, read state, archive and recoverable trash |

Goal matching checks bounded task/constraint patterns, including cooking, weight-loss claims, free use, low cost, no equipment and explicit exclusions. Negated, unsupported and unknown requirements cannot be rescued by a high similarity score. A source claiming “减脂餐” is not an independently verified nutrition recommendation. No supported match is a valid result.

A cue is not a fraud verdict. A public repository or MIT license does not prove zero API costs, all dependency terms or working functionality. GitHub lookup sends only identified repository names; ordinary network request information still reaches GitHub. Errors remain unverified.

The default detail view shows a short derived version in Simplified Chinese, without timestamps. An original author’s written method takes priority over fallible machine speech; original text, timestamps and coverage stay available in a collapsed source section. This is source selection, extraction and local script conversion, not AI understanding or automatic correction of speech errors.

Prompts are short and goal-first, with relevant source evidence and the default $0 spending, authorization and untrusted-source boundaries. Chinese interface produces Chinese instructions; the target project's language rules still apply. Personal notes are excluded unless selected. Copying a prompt does not launch an assistant or execute code.

## Install

~~~sh
npx skills add m1nga/redbot
~~~

Then ask your AI assistant:

~~~text
Use $redbot with /path/to/my-redbot-backup.json.
My goal is to make the first task in my app easier to understand.
Choose one saved source, show the useful passage and give one next action.
~~~

Or select a post already accessible through your own authorized connector:

~~~text
Use $redbot to summarize this saved post. Check which “free” conditions
matter for my project, then prepare a small implementation brief.
Keep unread comments and video steps explicit.
~~~

The skill checks available tools and the actual account before retrieval. It can use supplied material without forcing a new installation. The Python reader returns a bounded lexical shortlist, then the host assistant reads the chosen item. Installing this skill does not install an account service or grant access to someone else's library.

For an explicitly selected, running legacy Mac app:

~~~sh
python3 /path/to/installed/redbot/scripts/read_library.py --live --query "first task"
~~~

This reads that Mac's localhost service. A phone's localhost is not your Mac. Missing service or file: use selected notes or a compatible backup; no hidden remote access.

## Example

You ask: “The screen feels busy; make the main action clearer.”

A saved layout passage can suggest reducing emphasis on competing controls, followed by a small action: adjust one section and compare it at the same screen width. The optional original example demonstrates this flow; it is not a user testimonial or conversion result. If the source is title-only, RedBot asks to read it before describing its method.

## What sync means

This is an unofficial browser connection built on [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp), not official favorites OAuth. Each visitor has a separate process, cookies, identity check and library. The adapter exposes login, saved-card scanning and selected text reads only; no posting, likes, comments or native collection changes.

Scans have no fixed saved-card or scroll-count cutoff. A 45-second lack of new cards and a 30-minute request deadline still end unconfirmed scans as partial. Progress reports what has arrived, rather than a percentage based on a guessed total. A quiet page or an unchanged count does not prove the end of the collection: only a verified successful source response reporting the list end can establish completion. Stops, source errors and unconfirmed endings remain partial. Interrupted current scans can recover private checkpoints; the next scan starts at the top and deduplicates. Old saves absent from a scan remain intact.

When enabled, opening the app checks the connection and a visible page can scan every 15 minutes. Closing it stops new scans; a started job may finish. No source webhook or always-on background scheduler is implied.

**Scanning and deduplication use no LLM calls.** Optional semantic search runs locally after a roughly 120 MB model download plus runtime and searches all saved text in the active library, splitting long passages into chunks and reporting actual coverage. It uses bandwidth, memory and battery. Asking an AI assistant to reason over a library consumes that assistant's usage. Selected videos can be read on demand: machine speech transcription and up to 12 uniform frame OCR samples, limited to 10 minutes and 100 MB. Processing uses the test host computer, with no cloud inference token bill. This is not full visual understanding, a truth verdict or a new generated summary. Retrieved first-screen comments are a bounded sample of user statements, not all comments, verified facts or agreement from the whole audience.

## Privacy and recovery

The invitation test stores separate login sessions and retrieved text on Ming's host for up to seven days. Remote access is forwarded through Cloudflare; local access stays local. Host downtime prevents new sync. Disconnect deletes that session's server data and keeps a device copy for export.

Personal notes, plans and organizing choices stay in this browser's IndexedDB. Account libraries and old device libraries are separate. Export JSON through **设置与我的数据 / Settings and my data** before switching devices or clearing storage. No automatic phone-to-computer note sync.

Semantic matching uses locally vendored Transformers.js 3.8.1 runtime and downloads the multilingual MiniLM model pinned to revision 2c4055b12046f11709e9df2c122e59ffbdc2f900. Hugging Face receives ordinary model asset requests; saved text is processed on device rather than sent to an inference API. The semantic switch is remembered on this device; vectors are isolated by active account/library, model version and text hash. Switching libraries cancels old searches. Disconnect requests deletion of that account’s vector cache and reports a deletion that cannot be confirmed. Basic matching remains available if loading fails; incomplete indexing is not full coverage.

The current app version is visible in the interface. When a newer version is available, the update action saves the current draft before refreshing; a failed save keeps the page open. It does not force an unsaved active tab to reload.

Never post backups, cookies, access tokens or login codes in public issues. Feedback downloads only what you type and is not sent automatically.

## Run your own test host

The distribution includes [application source](source/README.md), the adapter, its tests and a pinned upstream patch. See [connector provenance and build steps](source/connector/UPSTREAM.md). Transformers.js is bundled; prepare the pinned browser WASM before serving the app or running its browser-runtime fixture tests: `cd source && python3 scripts/prepare-runtime.py`. The helper downloads 21,596,019 bytes from a fixed public source commit, verifies SHA-256, and preserves existing files on failure. Skill installation does not require this browser resource. Other native/browser dependencies are installed separately. Use a new private runtime directory and your own endpoint configuration; never attach public visitors to an existing personal MCP.

The previous native Mac package is a separate build and is not updated by this web release.

## Validation

For 1.9.3, copied application source is pinned in `APP-SOURCE.json` with 80 bundled-file hashes and an explicit external WASM build resource. The published source bundle passed 94 JavaScript tests with the verified WASM resource prepared. Python code is unchanged in this frontend-only delta; its 60 passing tests from 1.9.2 are retained as prior evidence; the companion reader passed nine synthetic-backup tests. The original application checkout passed 97 JavaScript tests, including three historical promotion fixtures excluded from the public package. Four additional legacy-server tests passed there; that private-research-dependent legacy branch is not bundled, and its test command is omitted from the public instructions.

One selected 22.43-second Xiaohongshu video completed the local pipeline in an observed 6.2 seconds, producing ten machine-speech segments and eleven sampled OCR frames with zero cloud inference calls. The default speech model is multilingual small pinned to its author-hosted revision and SHA-256 in [video setup](source/connector/VIDEO.md). It improved this sample over tiny/base but still mistranscribed Chinese and technical terms. This single source trial is evidence of working media delivery and processing, not general transcription accuracy, full visual understanding or a performance guarantee.

An earlier 1.9.2 Chrome run using synthetic account/source responses exercised connect, automatic selected-video read, first failure, explicit retry, timestamped prompt generation, personal-note preservation and text-post cost cues. The real pinned browser WASM semantic model loaded and retrieved both fixture entries. After a page reload, the preference persisted and one unchanged chunk was reused while an updated item was recalculated; this was not a browser-process restart. A 390-pixel viewport had no horizontal overflow. These fixture checks do not establish real-account UI completion or physical-phone behavior.

For 1.9.3, actual Chrome with synthetic API responses verified that a lost terminal job resolves through read-only item reconciliation without automatic resubmission. At a 390-pixel viewport, the default view used Simplified Chinese without timestamps, retained collapsed original source and an earlier timestamped draft, and produced a 397-character goal-first prompt. A separate offline check using the already-retrieved authorized post produced a 441-character prompt with its author method once. No new source read or generative-model call was required for these presentation checks. The local OpenCC 1.4.2 dictionary and license files match the pinned npm package integrity and per-file hashes; conversion preserves code/URLs and does not repair ASR errors.

[BETA-VALIDATION.md](BETA-VALIDATION.md) records automated tests and builder trials. The prior 1.7 builder trial returned 289 cards, introduced no duplicates on repeat, recovered an interrupted scan and retrieved one selected post caption. A 390-pixel browser layout was checked. For 1.8, 23 connector fixtures and 27 JavaScript tests passed; controlled browser batches progressed from 20 to 60, and the real library retained 295 unique cards. The final v8 pagination fix passed fixtures but was not followed by another real full scan. Complete real-account enumeration remains unproven. These do not prove all favorites were found, the video was watched, two real accounts were isolated, or an unaided user can finish.

Same-phone QR login, distinct real-user isolation, independent user trials and production uptime remain unverified. This is a small invitation test, not a production sync service.

## Moving from GitHub Pages

SideCourt is the product's primary home. Earlier GitHub Pages and starter links retain a non-deleting export bridge. Export from the old origin, keep the backup, then restore it in SideCourt's **Settings and my data**. Verify saves, notes and plan before removing anything. Website storage does not move automatically.

## Why

The owner already had categories but still did not know which save to open. The two main destinations—what you want to do and your saves—keep the choice small. Account connection removes manual export from the everyday setup. Source coverage stays visible so a tidy result never pretends to have read more than it has.

## Search visibility

SideCourt pages provide descriptive text, real steps, limitations and canonical metadata matching the implemented product. Internal semantic retrieval is separate from external SEO/GEO. Crawlable content does not guarantee indexing, ranking, AI citations or customers.

## Author

Built by [Ming](https://sidecourt.space/people/m1nga/). Original RedBot code and skill are MIT licensed; the upstream source connector is Apache-2.0. Dependencies retain their own terms. Saved content belongs to its creators.

After trying RedBot, [browse what people are making on SideCourt](https://sidecourt.space/drops/). You can share something you made and describe the feedback that would help you use it better.
