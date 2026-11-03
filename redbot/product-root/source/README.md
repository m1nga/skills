# RedBot application source

The public entry is [RedBot on SideCourt](https://sidecourt.space/drops/redbot/). This folder contains the exact browser app and invitation-test adapter, without private runtime, an upstream binary or browser dependencies.

Build the pinned dependency using [connector/UPSTREAM.md](connector/UPSTREAM.md), then from this directory run:

~~~sh
python3 connector/service.py --binary /absolute/path/redbot-xhs --data-dir /absolute/private/runtime --port 8776
~~~

Open http://127.0.0.1:8776/. The private runtime operator.json contains a newly generated invitation. Set your own invitation there while the service is stopped. Do not commit this runtime.

For remote use, replace app/connection.json with your own HTTPS API endpoint and allow only your frontend origin through the service's --origin option. The checked-in endpoint is the author's temporary test host, not infrastructure for your deployment. Cookies and bearers must never appear in that file. Use an HTTPS proxy that forwards Host as 127.0.0.1:8776; the service binds to loopback.

Verify locally:

~~~sh
node --test core.test.cjs semantic.test.cjs promotion.test.cjs check.test.cjs
python3 -m unittest discover -s tests -v
~~~

The upstream patch is deliberately a textual diff: its context whitespace must remain intact. The original application source commit is recorded in ../APP-SOURCE.json. The root migration/export bridge is preserved for earlier GitHub Pages users.
