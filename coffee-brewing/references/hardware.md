# Hardware profile — TEMPLATE

The live profile lives OUTSIDE this package at **`~/.coffee/hardware.md`** so it survives
skill updates and never ships with the skill. On first use, ask the user for their gear
and write their answers there in this format. Record what they know; leave the rest blank
and refine later.

```markdown
# My coffee hardware

## Grinder
- Model:
- Adjustment system: (stepped or stepless; dial range; microns per step if known)
- Direction: (lower numbers = finer? yes/no)
- Espresso range: (dial numbers)
- Pour-over range: (dial numbers)

## Espresso machine
- Model:
- Basket: (diameter in mm, single/double, dose range in g, usual dose)
- Milk: (steam wand available? typical milk drinks?)
- Notes: (boiler type, recovery habits, quirks)

## Brewers on hand
- (V60 / flat-bottom dripper / moka pot / French press / Aeropress / …)
```

<!--
Filled-in example — a fictional but realistic home setup, kept here so you know
what good answers look like. Never copy these values for a real user; ask for
theirs and record what they say.

## Grinder
- Model: 64mm flat-burr single-doser (numbered dial)
- Adjustment system: dial 0–90, stepless
- Direction: lower numbers = finer (yes)
- Espresso range: 12–20
- Pour-over range: 55–70

## Espresso machine
- Model: 58mm single-boiler home machine (9 bar)
- Basket: 58mm double, 17–19g, usually 18g
- Milk: steam wand handles lattes/flat whites directly
- Notes: single boiler — when pulling shots back to back, pause 20–30s every
  2 shots to let it recover

## Brewers on hand
- Hario V60
-->

**Reminder for the assistant:** grind dial numbers are only meaningful on the grinder
registered here. On unregistered gear, speak in fine/medium/coarse and converge by taste
(see the escape valve in SKILL.md).
