# Xiaohongshu source connector

RedBot calls an isolated process of [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp), pinned to `7797fd375aba02dcd33afe143f6bee13e5870859`. The upstream project is Apache-2.0 licensed. It is an unofficial browser connector, not an official consumer favorites OAuth API.

`patches/favorites-checkpoint.patch` adds bounded favorite scrolling and a private, per-account recovery checkpoint. It does not bypass authentication, CAPTCHA, or a paywall. Maximum 2,000 observed cards / 100 scroll steps / 150-second page timeout. A stopped or stalled list is always labeled partial; no fabricated completion or pagination cursor. Checkpoint recovery keeps observed cards on an interrupted request; a later scan starts at the beginning and deduplicates.

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
