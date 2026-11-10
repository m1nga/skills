# Try a portfolio brief with fictional evidence

Every security, figure, release and date in this example is invented. The
snapshot command runs offline. The research judgment below is an example of
how to connect supplied evidence to a decision.

## Inputs

- **Positions:** two shares of EXAMPLE at an $80 average cost and $50 of cash.
  The synthetic price is $100 per share.
- **Prior decision:** hold through the next two earnings releases. Revisit the
  thesis if operating margin falls below 15% for two consecutive quarters on
  the same accounting basis.
- **Evidence A:** fictional quarter ended March 31, released May 6.
  Reported operating margin was 14%.
- **Evidence B:** fictional quarter ended June 30, released August 5.
  The issuer reported adjusted operating margin of 14%. Comparable reported
  operating margin is absent from the supplied fixture.
- **Constraint:** any new purchase must be in whole shares. Compare it with
  holding cash and a diversified benchmark before sizing.

## Reproduce the snapshot

Set `SKILL_DIR` to the absolute directory containing this skill's `SKILL.md`.
Run these commands in a disposable directory. The quote timestamp is set
relative to the run so an old demo does not accidentally test quote staleness.

```sh
printf 'ticker,shares,avg_cost\nEXAMPLE,2,80\n' > demo-positions.csv
python3 - <<'PY'
import datetime as dt
import json
from pathlib import Path

observed = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)
quotes = {
    "EXAMPLE": {
        "price": 100,
        "currency": "USD",
        "observed_at": observed.isoformat(),
        "source": "https://example.org/fictional-quote",
        "session": "fictional",
    }
}
Path("demo-quotes.json").write_text(json.dumps(quotes))
PY
python3 "$SKILL_DIR/scripts/snapshot.py" --positions demo-positions.csv \
  --quotes demo-quotes.json --cash 50 --output demo-snapshot.json
```

The snapshot records $200 in securities, $250 net assets, $40 unrealized
gain and an 80% account weight. The thesis remains `unreviewed` in the
snapshot. It is evaluated separately in the brief.

## Example brief

**Decision:** wait for comparable evidence before adding. The supplied record
does not establish the two-quarter trigger. The March figure is reported and
the June figure is adjusted. On these inputs the prior holding stays under
review and the trigger is **unknown**.

**Strongest opposing evidence:** both provided margin figures are below 15%.
If the June reported margin also comes in below 15%, the original review
trigger is met. The 80% position weight makes this gap material.

**Alternatives and limits:** keeping the $50 unallocated preserves flexibility.
One extra share at the synthetic price would require $100. A diversified
benchmark would reduce exposure to this issuer, but its price, holdings and
fit are absent from the fixture. No switch or position size is supported here.

**Next review:** obtain the June reported margin on the same basis as March.
Record whether that evidence triggers a thesis review. The available facts
support no valuation target.

## See the incomplete cases

- Repeat without `--cash` and use a new `--output` path. The security value and
  gain stay available. Account NAV, weight and buying power remain unknown.
- Use a separate quotes file containing only `{}` and a new output path. The
  quote is missing and the holding value, gain, NAV and weight remain unknown.
