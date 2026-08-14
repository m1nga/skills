# Bean memory — FORMAT SPEC (ships empty)

Dialed-in beans live OUTSIDE this package at **`~/.coffee/beans.md`** so the user's data
survives skill updates and never ships with the skill. Create that file on first dial-in
if it doesn't exist. When the user shows a known bag or names a known bean, **check
`~/.coffee/beans.md` FIRST** and serve the proven parameters directly.

If the environment cannot write files, output the finished entry as a copyable text block
and tell the user to save it wherever they keep notes.

Append one entry per dialed-in bean, in the user's language:

```markdown
## Bean name (roaster + bean)
- Origin / process / roast:
- Flavor notes:
- ✅ Espresso: __g in → __g out, __s, grind __, __°C (1:__)
- ✅ Pour-over: __g coffee : __g water, grind __, __°C, total time __
- Notes: (traps hit while dialing in — misread sourness, static, RDT needed, …)
- Dialed-in date: YYYY-MM-DD
```

The Notes line matters: record *how* the dial-in went wrong before it went right (e.g. "a
light dense bean read as bitter but was under-extracted; fixed by grinding 3 steps
finer"). That's the part that saves the next bag.

Grind numbers in entries refer to the grinder registered in `~/.coffee/hardware.md` at
the time of dial-in; note the grinder if it ever changes.
