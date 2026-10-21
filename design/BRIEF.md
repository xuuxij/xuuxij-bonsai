# The brief a design round starts from

What a design reviewer needs to know before designing anything for this program, written
down after the tree-variations round so the next round starts here instead of rediscovering
it. Give the reviewer this file, the owner's words for the round, and the sources in this
folder that the round touches.

## The screen

- A Linux text console, TERM=linux, 135 columns by 120 rows, portrait, one laptop whose
  only job is this program. Resources are not a limit; the console is.
- Colours: 8 foreground slots plus bold for 8 more, 8 background slots, 64 colour pairs.
  The program sets the palette slot by slot to exact RGB (the landscape's blues, the
  clouds' greys, the tree's green, gold, red, brown) and makes pairs on demand. Every slot
  is spoken for; a new tone must take an existing slot.
- The display is dim by the owner's choice: the landscape at lightness 0.26 and chroma
  1.0, the clouds at 0.41 (`LANDSCAPE_L`, `LANDSCAPE_CHROMA`, `CLOUD_L` in the program).
  Slot 7 ("white") is #252521 on screen, slot 13 (the clouds' white) #494947: the
  brightest greys that exist. A design that needs "white" means slot 13. The tree's own
  slots are undimmed: green 2/10, gold 3/11, red 1/9.
- The font is Uni2-Fixed16: it has ░ ▒ █ and the box-drawing set, not ▀ ▄ ▓. Half
  blocks are not available.
- Phone photos of the screen auto-expose and lie about brightness; the framebuffer dump
  (`/dev/fb0`) is the truth, and the harness PNGs match it.

## The program's model

- One Python file, curses. A tree is planned in full (strokes of cells, each cell
  (row, column, text, paint)), then drawn one stroke after another with a moving tip,
  then goes through its autumn. Everything new is a rule in `plan` and a draw in
  `draw`; a stroke kind decides how it crumbles.
- Foliage is a pad per branch family: `fill_pad` fills the union of flat-bottomed domes
  with characters, lit along the top, feathered at the edge, dark on the bottom row, and
  covers the wood of its own twigs. A foliage style is a set of rules inside that one
  function (characters, where the lit band is, holes, accents, the pad's radii), not a
  new drawing path.
- The trunk is `make_trunk`: a row per cell list, tapering, with edge glyphs and an
  inside drawn on black. A bark is a glyph rule per row inside it, carried as a paint
  string so the draw can colour cells one by one.
- Over the landscape every tree stroke keeps a one-cell halo of plain ground; the trunk's
  inside is black. Nothing of the tree may be drawn inside the planter's outline.
- The planter is the run's, not the tree's: the wide Teizan rectangle or the glazed oval,
  on a stand half the time, kept for the whole run (the owner, 2026-10-20). A form may not
  bring its own pot except the cascade, whose hexagon on the cascade stand is the one
  exception. Design forms to live in a wide tray.

## What has been ruled and stays

- The tree is the one thing in colour; the landscape is a quiet blue print; the clouds
  are grey masses at three depths. Nothing bright behind the tree.
- All assets are retained: a new look is added beside the old, never replaces it, and the
  old look stays in the draw ("don't delete them from the asset list").
- Numbers are the owner's dials: anything a person might want more or less of becomes a
  setting with a documented default (`clouds_far`, `leafiness`, `foliages`).
- The settings' defaults are the design; the owner's own `.conf` on the laptop sets his
  taste (bunjin 0, kengai 0, `clouds_far` 3, trunk brown via the console palette).

## How to render (the check)

In the repository clone on DevPC (`C:\Users\UM-pc\xuuxij-bonsai`), after copying the
program over:

- `python tools/scene_review.py OUT SEED 1 key=value ... AT=170` draws the whole screen
  as PNG at 170 s, the tree just grown (growth takes a quarter of the ten-minute cycle;
  the leaves turn from 195 s, fall from 265 s). `AT=240,300` shows the autumn.
- `python tools/render_review.py OUT SEED key=value ... [phases]` writes the tree as text
  at 20, 50, 80 and 100 % of its growth, a map of what each cell is (w wood, L/l leaf,
  d deadwood, p planter), and the numbers from the tree's report; `phases` adds the
  autumn frames. This is where the counts come from (turned colours, blooms, jins).
- `SIZE=200x55` for the landscape terminal. Any setting goes as `key=value`
  (`style=`, `foliage=`, `bark=`, `deadwood=yes`, `pot=`, `clouds_far=`).
- A crop of the tree out of the full PNG (`crop_tree.py` in the session's scratchpad: the
  lower middle of the frame) is enough to judge a tree; the full frame is for the scene.

## The deliverable that worked (tree variations, 2026-10-21)

The reviewer sent two files, and both were used as written:

1. A design note (`tree_variations.md`) with, in this order: the recommendation in one
   breath; what the research gives (with the references, later copied into
   `docs/references.md`); the draws and settings as a table (name, default, meaning);
   one section per piece with its rules in the program's own terms (character mixes as
   strings, shares as numbers, "where the lit band is", what stays as is); the numbers
   for new forms as a table in the `FORMS` dict's own keys, new keys marked; the
   combination tables (which bark a foliage allows, deadwood chances); the build order;
   what is out of the round and why; and the first-render list, each item saying what
   it checks and which renders are wanted as PNG.
2. A specimen script (`tree_variations.py`) that prints each piece as text from the same
   rules, with the dicts ready to paste. The program's code was written by hand from the
   note; the script settled every "what exactly does this look like" without a round trip.

What made it fast: rules in the program's vocabulary (`fill_pad`, `make_trunk`,
`plan_branch`, `FORMS` keys), a build order that renders something after step 1, and a
first-render list with seeds, so round 2 is a folder of files at known paths.

## The round, in steps

1. The owner's words for the round, this brief, and the sources it touches go to the
   reviewer. The reviewer researches (web references, ASCII art) and sends the design
   note and, where it helps, a specimen script. Round 1 ends there; nothing is built
   from a conversation.
2. The build follows the note's order. Rendering starts after the first piece. Anything
   changed from the note is listed with its reason, and anything unreadable on the real
   palette is fixed and reported (the deadwood's slot, the planter ruling).
3. Round 2 is renders: the first-render list at paths the reviewer can read, the counts
   the note asked for, "what I changed and why", and questions lettered a, b, c, each one
   decision. The reviewer answers with numbers only, as `key: old -> new`, unless
   something is broken on sight; shape rules do not move in round 2.
4. The numbers are applied, the same seeds rendered again, the round closed. The owner
   sees the installed result on the laptop, not the PNGs, and rules in his own words;
   his rulings go into `LOG.md`.

## Known traps

- Prose and dict disagreeing (the windswept's lean: "30-35 degrees" in the text, 1.0-1.4
  in the dict, which is 45-55): ask, do not guess.
- A per-form pot, a new colour slot, a brighter background: all ruled out above; a design
  that needs one should say so up front and offer the fallback.
- `wood()` in the draw colours a whole row with one attribute unless the cells carry a
  paint string; any new per-cell colour needs the paint.
- The harness's `plain_attrs` and `colour_attrs` (tools/common.py) must know every new
  attribute name or `render_review.py` fails with a KeyError.
- The `bud` attribute already exists (the opening leaf); accent names must not collide.
