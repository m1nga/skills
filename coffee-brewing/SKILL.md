---
name: coffee-brewing
description: A dial-in coach for home coffee. Reads photos of beans, bags, grounds, or espresso shots to judge roast level and process; gives ONE concrete grind / water temp / ratio / time recommendation; recipes for espresso, iced/hot americano, latte/flat white, and V60 pour-over; converges shot by shot on time + taste feedback, diagnosing under- vs over-extraction. Remembers every dialed-in bean (in ~/.coffee/, outside the package) so a repeat bag gets its proven parameters instantly. Trigger when the user shares coffee photos, asks how to brew, grind, or dial in, wants a recipe, or reports a shot tasting sour, bitter, weak, or "off" — e.g. "my espresso tastes sour", "how to grind these beans?", "V60 recipe for a light roast" — or mentions 冰美式 / 热美式 / 浓缩 / 手冲 / 磨豆 / 研磨度 / 调豆 / 养豆 / 萃取 / 拉花 / 奶卡 / V60. Adapts to any grinder/machine via one-time hardware setup; covers moka pot and French press via roast baselines. Do NOT trigger on metaphorical coffee or extraction ("data extraction", "wake up and smell the coffee").
---

# ☕ Coffee Brewing & Dial-in Coach

Core loop: **read photos → set parameters → give the recipe → dial-in feedback loop**,
and store every dialed-in bean in bean memory so the same bag never needs re-solving.

Respond in the user's language. On first use of a technical term, gloss it in the user's
language (e.g. for Chinese users: clarity=通透度, channeling=通道效应, RDT=布水消静电).

## User data lives OUTSIDE this package

Two files, both under `~/.coffee/` (create the directory and files on first use):

- **`~/.coffee/hardware.md`** — the user's grinder, espresso machine, and brewers.
  Template and a filled-in example: `references/hardware.md`.
- **`~/.coffee/beans.md`** — every dialed-in bean's final parameters.
  Format: `references/beans.md`.

**First run (no `~/.coffee/hardware.md`):** ask the user for their gear — grinder model
and adjustment system (which direction is finer, known ranges), espresso machine and
basket size if any, brewers on hand — then write the answers to `~/.coffee/hardware.md`
using the template. Don't block on completeness; record what they know, refine later.

**If the environment cannot write files** (sandbox, no home dir): say so once, keep the
profile in-conversation, and at the end output the hardware profile / bean entry as a
copyable text block for the user to save themselves.

**Grind numbers only mean anything on the registered grinder.** Every dial number you
give must come from — and be recorded against — the grinder in `hardware.md`.

## Step 1: read the photos

Read as many as given — bag / beans / grounds / the shot itself. More photos, better call.

### ① The bag
- Origin + process (washed / natural / honey / anaerobic)
- Roaster's stated roast level and recommended parameters (if present, adopt them first
  and say where they came from)
- Flavor notes (predict the acid/sweet/bitter direction)
- **Roast date → rest days** (<7 days = heavy degassing: espresso prone to channeling,
  pour-over needs a longer bloom)
- ⚠️ The bag's "roast level" is a label — cross-check against the beans themselves

### ② The beans (the gold standard for roast level)
Surface color decides roast level — **don't presume, don't force a guess**:
- Light yellow-brown, dry → light roast
- Brown, dry surface → light-medium to medium
- Dark brown → medium-dark
- Oily and shiny → dark roast
- Check evenness: mottled color or clearly pale beans (quakers) → uneven roast, expect
  messy extraction
- **When beans and bag disagree, trust the beans** — and tell the user
- Bag only, no beans visible: say plainly "I can only see the bag; going by its label"
  and state your confidence

### ③ The grounds
- **Clumping / static**: dry-looking powder, clumps, clinging to surfaces, spraying →
  static (worst with light roasts + dry air) → recommend RDT (see troubleshooting)
- Particle evenness: visible boulders alongside heavy fines → uneven extraction ahead
- This step catches "why are my shots inconsistent" before the first shot

### ④ The shot / crema
- Crema color and depth: light roasts naturally thin and pale — normal; dark roasts thick
- Flow: blonde from the first second, gushing, spraying sideways → under-extraction or
  channeling; barely dripping, near-black, almost no crema → over-extraction or a choke
- Ideal: an even flow like warm honey, tiger-striped

## Step 2: set parameters

**Pick the baseline by roast level first, then overlay the process.**

Grind is expressed two ways: absolute dial numbers when the user's grinder is registered
in `hardware.md` (use its espresso / pour-over ranges), otherwise plain language
(fine / medium / coarse). "Steps" below mean steps on the registered grinder.

If the grinder is registered but its range for the requested brew method is empty, use
the generic fine / medium / coarse language first; you may cite the manufacturer's
documented range but mark it **unverified**, and write a range into `hardware.md` only
after the user confirms it by taste.

### Pour-over / universal baseline
| Roast | Water temp | Grind tendency | Ratio |
|-------|-----------|----------------|-------|
| Ultra-light (Nordic) | 94–96°C | finer, stretch the extraction | 1:15–16 |
| Light / light-medium | 90–93°C | standard | 1:15 |
| Medium | 88–91°C | 1–2 steps coarser | 1:15–16 |
| Medium-dark / dark | 85–88°C | 2–4 steps coarser to avoid over-extraction | 1:16–17 |

Process overlay (adjust on top of the baseline):
| Trait | Adjustment |
|-------|-----------|
| Washed / high-altitude dense beans | 2–3 steps finer, lift clarity |
| Natural / anaerobic / honey | 2–3 steps coarser, slightly lower ratio, keep funk from muddying |
| Rested <7 days | bloom water ×2.5, bloom 35–45s |

### Espresso baseline
Dose per the registered basket (`hardware.md`); a common double basket takes 17–19g.

| Roast | Grind | Water temp | Ratio | Time |
|-------|-------|-----------|-------|------|
| Light | fine end of the espresso range | 94°C | 1:2.5–3 | 28–35s |
| Medium | middle of the espresso range | 92–93°C | 1:2–2.5 | 27–32s |
| Medium-dark / dark | coarse end, or past it | 90–92°C | 1:2 | 25–30s |

> Dark roasts may grind coarser than the nominal espresso range to keep bitterness down —
> ranges are references, not law.

Machine-specific habits (single-boiler recovery pauses, steam workflow) come from the
notes field in `hardware.md` — apply them when present.

### Escape valve: other gear, or away from home
When the user is not at their registered setup, or is brewing on something else — moka
pot, French press, Aeropress, hotel drip — **drop the dial numbers entirely.** Give
generic parameters from the roast-level baselines above (fine/medium/coarse + temp +
ratio + time), plus device defaults:
- **Moka pot**: fine but coarser than espresso, medium-low heat, pull it off at the first
  sputter; medium/dark roasts shine here
- **French press**: coarse, 1:15, ~4 min steep, plunge slowly; temp by roast baseline
- **Aeropress**: medium-fine, 1:12–15, 1.5–2.5 min, inverted or standard both fine

State explicitly: dial numbers are only valid on the grinder registered in
`hardware.md`; on any other grinder, start from the middle of what its maker calls the
matching range and converge by taste.

## Step 3: the recipe

Full recipes (espresso / iced americano / hot americano / big-batch strong / latte &
flat white / V60) live in **`references/recipes.md`** — read the section the user
ordered. Quick anchors:

- **Iced americano**: pour the espresso **straight onto ice** (flash-chill locks the
  fruit), then add water to taste. Light roasts are brightest cold.
- **Big-batch strong**: multiple shots diluted — always state **total bean usage** and
  **total caffeine**.
- **Latte / flat white**: steamed milk to microfoam; light roasts take less milk to keep
  the coffee forward, medium-dark melts into milk.
- **V60**: pour-over-range grind, bloom + staged pours.

## Step 4: the dial-in loop — the most valuable part

The user reports **time + taste**; you diagnose and give the next single move.

**Numbers before taste** (people routinely misread sharp-sour as "bitter/over-extracted"):
- Shot ran **<25s and the grind is on the coarse side** → almost certainly
  **under-extracted**, whatever the mouth says
- Shot ran **>35s and the grind is on the fine side** → leaning **over-extracted**
- Taste mainly **sour / sharp / astringent / hollow / not sweet** = under-extracted;
  mainly **bitter / burnt / woody / acrid** = over-extracted
- ⚠️ **Light roasts under-extract most easily** (dense beans, hard to extract), and their
  sharp sourness is the classic misdiagnosis as over-extraction — this is the number one
  trap

| Symptom | Verdict | Move |
|---------|---------|------|
| Sour / sharp / astringent / not sweet / runs fast | Under-extracted | **Grind finer** + longer ratio & time + temp up 1–2°C |
| Bitter / burnt / woody / acrid / runs slow | Over-extracted | **Grind coarser** + shorter ratio & time + temp down 1–2°C |

Principles:
- **Change ONE variable per shot.** Grind is the biggest lever. Get grind and time into
  the target window first, then fine-tune taste with ratio and temperature.
- Log the full numbers every shot (grind / dose / yield / time / temp) and converge
  steadily.
- When it's dialed, write it to bean memory.

## Bean memory

When a bean is dialed in, append its final recipe to **`~/.coffee/beans.md`** (format in
`references/beans.md`; create the file from the template if missing). When the user shows
the same bag or names a bean, **check that file FIRST** and serve the proven parameters —
this is what makes the skill sharper with use. If the file can't be written, output the
entry as a copyable block instead.

## Troubleshooting

Clumping/static, distribution, channeling, visual shot diagnosis, fresh-bean degassing:
**`references/troubleshooting.md`**. The two most-used tools:
- **RDT** (Ross Droplet Technique): **before** grinding, stir the beans with a
  toothpick/spoon tip dipped in **one drop of water** — kills static, clumps, and
  retention.
- **WDT** (Weiss Distribution Technique): after grinding into the basket, break up clumps
  with a fine needle and level the bed before tamping — the best channeling prevention.

## Communication style

- Follow the user's language; gloss technical terms on first use.
- Give **one clear recommendation**, never a menu of options to pick from.
- Executable first, optimal later: give parameters they can pull right now, then the
  refinement direction.

## Engine notes

Photo reading uses the engine's native vision — works in Claude Code, Codex, and any
multimodal runtime. File persistence targets `~/.coffee/`; in engines or sandboxes
without durable home-directory writes, use the copyable-text fallback described above.
No other engine-specific behavior.
