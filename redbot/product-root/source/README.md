# RedBot — Put your saved ideas to use

[Open RedBot on SideCourt](https://sidecourt.space/drops/redbot/) to connect your own Xiaohongshu account in the invitation-only test, find a relevant save, read its useful text and turn it into a next step. Chinese-first web interface with an English switch.

This is the application source. The [companion skill](https://github.com/m1nga/redbot) lets an authorized AI assistant reason over selected material. Browse [SideCourt](https://sidecourt.space/) for other makers’ work and share what you are making when it is useful.

## Account test (1.9.6)

Enter an invitation, review data handling and scan the sign-in code in Xiaohongshu. Invitation links visibly prefill the code; an existing verified device session does not ask for it again. Each visitor gets a separate browser process, cookie file, library and random bearer. The invitation cannot read another visitor’s data. Sessions expire after seven days, and disconnect removes server data. There is no default three-account quota; operators can set an explicit `--capacity` if needed. Removing an account quota does not increase the test host’s processing capacity: video inference still runs one job at a time.

This is an unofficial browser connection, not official favorites OAuth. Login, saved-card scanning, selected-post text, already-returned first-page comments and local video transcription/sampled-frame OCR are exposed. No publishing, likes, comment posting or native collection edits. The operator must keep the host running; temporary HTTPS forwarding has no uptime guarantee. Same-phone QR recognition and two distinct real-account isolation are not yet field-verified.

Saves appear as each batch arrives; the list stays usable during a scan. There is no fixed card or scroll-count limit. A scan is complete only when a continuous source pagination chain reports its end and all observed IDs have arrived. Stalls, cancellation and a 30-minute fault deadline leave a clearly partial result. Stop for now retains arrived saves; checking again starts from the top and deduplicates, preserving older saves and notes. Opening the app checks the connection; while visible it can scan every 15 minutes. Closing the page stops new scans, but an already-started job can finish.

Opening an unread save automatically reads that selected post, or its video speech and sampled screen text. This does not bulk-read the library. Progress, cancellation, failure and explicit retry remain visible in the detail panel, and unsaved notes survive polling. Empty or mismatched source responses cannot unlock an invented summary. Already-returned first-page comments are labeled as author/reader statements, never complete coverage or verified facts; no additional full-comment crawl is started. Updates show a visible version and an explicit save-and-reload action.

Scanning, deduplication and wording checks make no LLM calls. Optional on-device semantic matching covers the full active library, including imported text, notes and available video transcripts/OCR, with token-based chunks rather than a 300-entry or character limit. It reports coverage, processes bounded batches and keeps account-scoped local vector caches so completed work can be reused after cancellation. Model similarity ranks candidates; source evidence and supported goal constraints still determine whether RedBot can offer a next step. A high similarity score alone is not proof of applicability.

The semantic model runs on the visitor’s device; its JavaScript/WASM runtime is served from pinned local application assets and public model weights download from a fixed Hugging Face revision on first use. No save text is sent to a paid embedding API. CPU, memory, initial download and browser storage are real costs; model/cache eviction can require downloads or computation again. See [DEPENDENCIES.md](DEPENDENCIES.md).

Reading an eligible selected video requires separately installed local tools on the connector host. It transcribes speech with timestamps and samples up to 12 frames for Chinese/English OCR. It does not understand scenes, gestures, objects or complete visual instructions. Recognition can be wrong, video access can fail and limits/errors remain visible. Computation and temporary media use the operator’s CPU, memory, disk and bandwidth, with one video pipeline at a time. See [video setup and limits](connector/VIDEO.md). List scanning itself does not read every saved post, comment, image or video. An AI assistant’s later reasoning or API use has its own cost.

## Use and run

The public frontend lives on SideCourt. app/connection.json selects the running test API; it must contain no invitation, bearer or cookie. Never point it to a developer’s existing personal MCP service.

Build the pinned upstream dependency using [connector/UPSTREAM.md](connector/UPSTREAM.md), then run:

~~~sh
python3 scripts/prepare-runtime.py
python3 connector/service.py --binary /absolute/path/redbot-xhs --data-dir /absolute/private/runtime --port 8776
~~~

The preparation command reconstructs the 21,596,019-byte browser WASM asset from a fixed public source commit and verifies its size and SHA256 before installation. An already verified local file skips the download. Use `python3 scripts/prepare-runtime.py --repair` to replace a damaged file; failed downloads or checks preserve the previous file. The large WASM is excluded from source tracking, while its pin manifest and licenses remain included. The prepared file must be included when deploying the frontend; browser self-hosting remains unchanged.

Open http://127.0.0.1:8776/. The generated private operator.json contains the invitation. Remote hosting requires an explicitly configured HTTPS proxy with the loopback Host header and an allowed frontend origin. Runtime stays outside Git; do not publish account files, logs or recovery checkpoints.

## Data and recovery

Device notes, plans, collections, read state and recoverable trash live in IndexedDB. Account and old device libraries use separate keys. Disconnect keeps a local offline copy for export; reconnect uses a separate library. Backup/restore currently uses RedBot JSON. A link is a reference, not proof that its source was read. No automatic phone-to-computer note sync.

The legacy Mac package and its original local data in ~/Library/Application Support/Shelf remain a separate prior build. This web release does not rebuild it. Do not use the old private packaging script for a public release.

## Checks

~~~sh
node --test core.test.cjs semantic.test.cjs check.test.cjs tests/*.test.cjs
python3 -m unittest discover -s tests -v
~~~

The 1.7 builder trial observed 289 cards and one selected-post caption. The 1.8 trials retain 295 unique cards and the earlier selected-post text. The latest real scan observed 80 before the source returned success without pagination data; this is partial, not proof of full-account coverage. First 20 arrived about 6 seconds after scan start. The final adapter stops on that incomplete response and offers a later retry. Synthetic UI tests verify batches appearing before completion, stopping without data loss, and preservation of a search and unsaved note. A single fresh QR trial took 3.77 seconds; this is not a latency guarantee. See the distribution’s validation record for the final source-end result. No independent-human, two-real-account or physical-phone acceptance is claimed.

The 1.9 semantic checks used the actual pinned multilingual model in Node with native CPU inference on synthetic material: all 351 rows and 369 chunks were covered, the relevant long-text tail ranked first for Chinese and English queries, and the second pass reused all cached chunks. IndexedDB API tests used fake-indexeddb; these are not browser persistence tests. Real browser worker/WASM execution, cache persistence across a browser restart and two-account live isolation remain separate acceptance checks. Local synthetic video verification used real Whisper and Apple Vision, not a private Xiaohongshu video. Neither test proves full-library source reading or complete video understanding.

The 1.9.2 follow-up reproduced the user's selected real post: normal identity and caption succeeded; current EF4/EF5 MP4 labels caused the old video selector to reject it. After repair, the actual 22.43-second video completed local ASR and 11 OCR samples. The small speech model improved over tiny but retained observable errors; automatic transcripts require checking. In actual Chrome, a synthetic library passed normal connection, selected-read progress/failure/retry, preserved drafts, fee-cue display and timestamped build-brief output. The pinned browser WASM model loaded and retrieved both synthetic entries with reported coverage. These checks do not establish physical-phone behavior, two-real-account isolation or flawless source understanding.

In 1.9.3, a missing/replaced job triggers read-only reconciliation against that specific read attempt. Old successful content cannot masquerade as a new completion; uncertainty exits the spinner and allows an explicit retry without automatic resubmission. The default detail view and copyable brief prioritize an author's written method, followed by other useful text, deduplicated screen text and finally speech. They use concise Simplified Chinese without timestamps; original source and reading coverage remain expandable. This is source selection and extraction, not generative reasoning or automatic speech-error correction. Briefs are goal-first and carry only relevant source material, with spending, authorization and source-trust boundaries retained.

In 1.9.4, **Read all content** adds every unread save to an account-local queue with no item-count cutoff. Progress survives page closure; pause finishes the current item, resume continues the remaining items, and failures can be retried without rereading successful items. Three consecutive source failures or an expired sign-in pause the queue. A host restart preserves the queue and requires an explicit Continue. Post captions become available before media finishes. Video audio is processed in five-minute chunks without the former ten-minute/100 MiB cutoff; actual host storage, network availability and a duration-scaled deadline still constrain processing. Sampled OCR is not full visual understanding.

In 1.9.6, library snapshots are sent outside the account lock, so a slow download cannot block connection status or completed reads. After the first download, each browser receives only changed posts; an unknown or expired sync cursor safely falls back to a full snapshot. Recently verified identity is reused for at most five minutes only while the exact credential file is unchanged. Explicit reconnect, changed credentials, service restart or a source failure requires a fresh check. The cached application opens before network responses; connection status and new data still come from the live service. These changes remove measured overhead; they do not guarantee Xiaohongshu response time or test-host availability.

“Sign-in session” means the credentials left after a QR login, not a new password requested by RedBot. “Server reading results” means already extracted post text, comments and video text. In the current test both are kept separately on the operator’s computer, with a copy of received content and personal notes in the visitor’s browser. The phone uses its own browser storage; it does not run the source connector.
