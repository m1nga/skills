# Xiaohongshu source connector

RedBot calls an isolated process of [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp), pinned to `7797fd375aba02dcd33afe143f6bee13e5870859`. The upstream project is Apache-2.0 licensed. It is an unofficial browser connector, not an official consumer favorites OAuth API.

`patches/favorites-checkpoint.patch` adds progressive favorite scanning and a private, per-account checkpoint. There is no fixed card-count or scroll-count cap. The normal logged-in page requests its own pages; RedBot observes its successful `note/collect/page` responses (`note_id`), with compatibility for the `user/collect/page` / `id` variant. Complete coverage requires a response chain starting at the empty cursor, each subsequent request matching the source-provided cursor, an explicit `has_more: false`, and every observed note ID present in the collected list. Unknown response shapes, source errors, a 45-second lack of new cards, or the 30-minute request deadline remain **partial**, never complete. The current `note/collect/page` wire shape was observed in a read-only account trial on 2026-11-03; endpoint compatibility needs rechecking after an upstream change.

The host merges and persists new checkpoints during the request, so the UI can display cards before the scan finishes. `GET /api/connection` and `GET /api/library` expose a monotonically increasing `revision`; `scan` exposes `running`, `seen`, `complete`, `coverage`, `endReason` and `interrupted`. `POST /api/cancel-sync` stops only that visitor's isolated process and preserves arrived saves. After a service restart an unfinished scan is marked `service_restarted`; retry starts from the beginning and deduplicates. No cookies, source tokens or pagination cursors are sent to the browser.

Replacing an unchanged checkpoint does not bump the library revision or rewrite the library. Start and terminal state changes remain observable. Private checkpoint diagnostics include only collection endpoint paths, response field names/types, counts and pagination booleans; they exclude headers, source text, IDs and cursor values and are not returned by the public service.

An HTTP/JSON success envelope with missing or unusable pagination fields is not an empty final page. v8 stops that scan with `source_response_incomplete` and retains arrived saves, instead of repeatedly triggering the same page for 45 seconds. A later explicit sync can retry from the beginning and deduplicate; no complete-coverage claim is made unless the source provides a valid final response. Scroll actions finish at the actual document bottom after positioning the last card, avoiding a masonry layout pulling the viewport back above its loading boundary.

QR readiness now waits for the login QR element instead of unrelated feed images or a fixed two-second delay. Identity checks use only the explore page's signed-in user state, not the favorites list. These changes do not bypass authentication, CAPTCHA, a paywall, or source throttling, and cannot guarantee a fixed login time.

Login restoration must wait for a non-guest user ID, not merely a sidebar element or an initial QR: both can appear before account state hydrates. If the ID never becomes ready, only an explicit guest state plus a QR after the wait confirms sign-out; unavailable state remains a source error. The v4 adapter fixes the v3 early-read regression without reverting fast QR readiness.

The v7 adapter allows 25 seconds for identity hydration within a 45-second page deadline. On failure, private diagnostics contain only page-state booleans and types. `POST /api/verify` retries the existing session read-only and automatically begins scanning after successful identity verification. Connection status exposes `canRetryVerification` when an idle session still has cookies but needs verification. Reconnecting with existing cookies tries identity first; a network timeout does not replace the session with a QR flow. Only confirmed sign-out proceeds to QR acquisition.

Do not connect this web service to an existing personal MCP endpoint. `service.py` launches its own loopback process, random backend token and private `COOKIES_PATH` for each visitor. Raw cookies, source tokens and checkpoints stay on the host. The public adapter exposes only login, saved-card scanning and selected-post text reads; write tools are not forwarded.

The shared invitation code opens a test slot. It is not the security boundary for anyone’s data: each session has a separate random bearer, account identity check and seven-day expiry.

Build with Go 1.24+ from a new dependency directory (replace the absolute patch path with this checkout's path):

~~~sh
git init xhs-source
git -C xhs-source remote add origin https://github.com/xpzouying/xiaohongshu-mcp.git
git -C xhs-source fetch --depth=1 origin 7797fd375aba02dcd33afe143f6bee13e5870859
git -C xhs-source checkout --detach FETCH_HEAD
git -C xhs-source apply /absolute/path/to/connector/patches/favorites-checkpoint.patch
cd xhs-source
go build -o redbot-xhs .
~~~

Use this newly built binary with service.py. Its browser dependency must be available on the host. Keep [UPSTREAM-LICENSE](UPSTREAM-LICENSE) with any redistributed connector or binary. The web distribution does not include a binary or browser. Do not modify a separately running personal connector to build this test dependency.

Validation after applying the patch:

~~~sh
go test ./xiaohongshu ./cookies ./browser -run 'TestRedbot|TestParseProfileTab|TestMakeUserProfileURL|TestGetCookiesFilePath|Test.*Cookie|TestMaskProxy' -count=1
node /absolute/path/to/connector/tests/pagination-observer.test.cjs /absolute/path/to/xhs-source/xiaohongshu/redbot_scan.go
node /absolute/path/to/connector/tests/login-identity.test.cjs /absolute/path/to/xhs-source/xiaohongshu/login.go
python3 -m unittest discover -s tests -p test_connector.py
~~~

The Python command runs from the RedBot repository. Fixtures validate more than 2,000 records, progressive visibility and persistence, partial recovery, cancellation, explicit completion evidence, account isolation and restart recovery. They do not prove completeness or timing for any real user's account.

The v9 QR adapter retains one anonymous page for up to 90 seconds: a 2026-11-04 cold-page trial returned a real QR data image after 31.7 seconds, beyond v8's 30-second deadline. If the hydrated page exposes a normal `button.login-btn` without a login modal, it invokes that control once. QR readiness and signed-in readiness are distinct; a sidebar alone never reports authenticated success. Source network failures or a missing QR still return an error at the bounded deadline. This does not promise a fixed login time or bypass source verification.
