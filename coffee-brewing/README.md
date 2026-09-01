# Dial In Espresso and V60 Pour-Over Coffee

**An AI home-barista skill that reads your shot's numbers before it believes your tongue.**

## What it does

Show it your coffee — the bag, the beans, the grounds, or the shot pulling — and it
judges roast level and process, then hands you one concrete set of parameters:
grind, water temperature, ratio, time. Report back with shot time and taste, and it
diagnoses under- vs over-extraction and gives you exactly one variable to change.
Repeat until dialed; the final recipe is saved to `~/.coffee/beans.md`, so the next
bag of the same bean skips the whole process. Covers espresso, iced and hot
americano, latte/flat white, V60 — plus roast-level fallbacks for moka pot and
French press when you're away from your gear.

## When it fires

- "my espresso tastes sour — what do I change?"
- "how should I grind these beans?" (with a photo of the bag)
- "help me dial in this new bag"
- "V60 recipe for a light roast"
- 这豆子怎么冲？/ 冰美式怎么做好喝？

It stays quiet on metaphorical coffee — "data extraction" or "wake up and smell the
coffee" won't trigger it.

## Quick answers

### Can AI help me dial in espresso?

Yes. Give the skill your dose, yield, shot time, taste, and grinder setting. It checks
the numbers before interpreting words like “sour” or “bitter,” then recommends one
change at a time so the next shot produces useful evidence instead of a new guess.

### Why does a fast espresso shot taste sour?

A shot that runs in under 25 seconds on a coarse setting is usually under-extracted,
especially with a light roast. The skill starts by grinding finer, then uses the next
shot’s time and taste to decide whether ratio or temperature needs attention.

### Can it make a V60 recipe from a coffee-bag photo?

Yes. It reads the visible roast level, origin, processing method, roast date, and
roaster guidance, cross-checks those clues against photos of the beans when available,
and returns one grind, water temperature, ratio, bloom, and pour schedule.

### Does it remember my grinder and beans?

Yes. Your grinder and brewer ranges live in `~/.coffee/hardware.md`; proven recipes live
in `~/.coffee/beans.md`. Both stay outside the installed skill, so an update cannot
overwrite your setup or dial-in history.

## Install

```
npx skills add m1nga/coffee-brewing
```

First run, it asks what grinder/machine/brewers you have and saves that to
`~/.coffee/hardware.md` — after that, every grind recommendation is a dial number
on *your* grinder, not a vague "medium-fine".

## Example

> **You:** (photo of a light-roast washed Pacamara bag) new beans, first shot ran
> 20s and tastes really sharp — over-extracted?
>
> **Claude:** 20s on a light roast is the classic trap — that sharpness is
> *under*-extraction, not over. Grind 3 steps finer (24 → 21 on your grinder), keep
> 19g in, target 48g out at 94°C. Expect ~27s. Report time + taste and we'll adjust
> one variable at a time.

## Works well with

- **desktop-package** — when a bean is finally dialed, package the tasting log and
  final recipe into a Desktop folder to share with whoever you brew for.
- **conversation-package** — a long multi-day dial-in session can be handed to a
  fresh session without losing which variables were already ruled out.

## Design notes

The core rule — check time and grind setting before trusting the taste report —
exists because of a real misdiagnosis: a dense light roast pulling sharp at 20s was
read as "bitter, over-extracted" and adjusted coarser, making it worse. Every part
of the method guards against that class of error: one variable per shot, grind as
the primary lever, numbers as tiebreaker over tongue. The skill also refuses to
give menu-style answers ("you could try A, B, or C…") — you get one recommendation
and a feedback loop, because that's what converges. Your hardware profile and bean
history live outside the package in `~/.coffee/`, so updating the skill never
touches your data.

## Field-tested

Probed 7 scenarios across 6 personas · 5 fired correctly · 2 correctly stayed quiet.

> **"First shot ran 20 seconds and tastes sharp — over-extracted, right?"**
> → Fired, and pushed back: 20s on a coarse grind is the classic *under*-extraction trap. Numbers overruled the tongue; the fix was 3 steps finer, not coarser.

> **"I have a DF64 grinder and a Breville — help me dial in this medium roast."**
> → Fired, ran the one-time hardware interview, and never quoted a dial number from someone else's grinder. Every number it gives is anchored to *your* registered gear in `~/.coffee/hardware.md`.

> **"帮我写篇增长帖子，把用户留存比作咖啡萃取"** *(write a growth post using coffee extraction as a metaphor)*
> → Correctly stayed quiet. Metaphorical coffee doesn't wake the barista.

> **"Save this bean to memory"** *(in a sandbox with no writable home directory)*
> → No fake "saved!": it says so once, keeps the profile in-conversation, and hands you the finished entry as a copyable block.

Probe method: [scenario-probe](../scenario-probe/)
