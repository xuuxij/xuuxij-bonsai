# Your own planters and forms

You can add planters and tree forms without touching the program: a planter is a
drawing in a text file, a form is a short list of numbers written over one of the
built-in forms. The program reads them when it starts.

| What | Where the file goes | How to pick it |
|---|---|---|
| A planter | `~/.config/xuuxij-bonsai/pots/NAME.txt` | `pot = NAME` in the settings |
| A form | `~/.config/xuuxij-bonsai/styles/NAME.txt` | `style = NAME`, or leave `style = auto` and it joins the draw with its weight |

The name is the file's name without `.txt`, in lower case. It must not be one of the
built-in names. A file with a mistake is reported when the program starts
(`xuuxij-bonsai: planter file skipped: ...`, with the line) and left out; the rest
still run.

To see one without waiting for the screensaver:

```sh
xuuxij-bonsai --pot carved-box --once          # one tree in your planter, then exit
xuuxij-bonsai --style windswept --seed 3 --once
```

The two examples below are in [examples/](examples/), ready to copy into those folders.

## A planter

Draw it in a `rows:` block. The rules:

1. **Row 1 is the far rim**, the back edge of the pot seen over the soil. The trunk is
   drawn in front of it.
2. **Row 2 is the soil.** The trunk stands on this row. On it, `.` and `:` are drawn
   as gravel (white) and `,` and `'` as moss (green); anything else is the body colour.
   The trunk's base flares over the gravel, so leave the middle plain.
3. The rest is the pot: as many rows as you like (one to ten is usual), at least 9
   columns wide. The planter is used exactly as drawn, at that width; it is not
   stretched. Lines are padded with spaces to the widest one.
4. **A last row made only of dashes** is the shadow on the table, drawn dark grey.
5. `body:` and `trim:` name the colours (black, red, green, yellow, blue, magenta,
   cyan, white). Without a `paint:` block everything but the gravel, moss and shadow is
   the body colour. The console's "yellow" is brown unless bold; bold is the lighter
   tone of each colour.

```
body: cyan
trim: yellow

rows:
      ___.-------------------------------.___
    .' . : , . : . , : . ,,' : . , . : . , . `.
   (===========================================)
    \   o   o   o   o   o   o   o   o   o   o /
     \_______________________________________/
        (__)                           (__)
      -------------------------------------
```

For more colour, add a `paint:` block of exactly the same shape, one letter per cell:

| Letter | Drawn as |
|---|---|
| `b` | body colour |
| `B` | body colour, bold (a lit lip, a sheen) |
| `t` | trim colour |
| `T` | trim colour, bold (gold bands, white studs) |
| `g` | gravel (white) |
| `m` | moss (green) |
| `s` | shadow (dark grey) |
| space | nothing drawn there |

```
rows:
  _________________________________________
 | . : , . : . , : . ,,' : . , . : . , . : |
|___________________________________________|
 |=========================================|
 |  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\   |
 |_________________________________________|
   (_o)                                 (o_)
  ------------------------------------------

paint:
  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
 b ggggggggggggggggggmmmgggggggggggggggggg b
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
 bBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBb
 b  TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT   b
 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
   bbbb                                 bbbb
  ssssssssssssssssssssssssssssssssssssssssss
```

Your planter can stand on the rosewood stand like any other (`stand = yes`), and the
fallen leaves heap on it, roll off its edges and pile against its feet by the same
rules. A tree is planted in it off-centre as its form asks; the tree keeps its own size,
so a small planter under a wide tree looks like a wide tree in a small planter.

## A form

A form file names a `base:` form and the numbers to change. Everything you leave out
stays as the base has it.

```
base: shakan
weight: 20
height: 0.5 to 0.6
spread: 0.6 to 0.7
lean: 0.55 to 0.75
bow: 2 to 4
branches: 3 to 4
first branch: 0.45
leaves: *^
planter: oval
```

A number is either fixed (`0.45`) or a range drawn fresh for every tree
(`0.5 to 0.7`). The bases are `moyogi` (informal upright, an S-curve trunk), `chokkan`
(formal upright, straight), `shakan` (slanting) and `bunjin` (literati). The cascade
cannot be a base. What can be set:

| Setting | Meaning | moyogi | chokkan | shakan | bunjin |
|---|---|---|---|---|---|
| `height` | share of the rows above the soil the tree reaches | 0.55 to 0.65 | 0.60 | 0.55 | 0.75 |
| `spread` | share of the width budget the branches may use | 0.60 to 0.80 | 0.65 to 0.75 | 0.55 to 0.65 | 0.30 to 0.40 |
| `trunk width` | cells wide at the base, e.g. `5` or `4 to 6` | by height, 6 to 9 | by height, 8 to 9 | by height, 6 to 7 | 3 to 4 |
| `movement` | columns the trunk swings (S-curve and literati trunks) | 8 to 14 | none | none | 12 to 20 |
| `apex` | columns the apex ends from the base (S-curve and literati) | -6 to 6 | 0 | by the lean | -10 to 16 |
| `lean` | the slant, as a share of the height (leaning trunks) | none | none | 0.35 to 0.55 | none |
| `bow` | columns the leaning trunk bows against its lean | none | none | 3 to 6 | none |
| `branches` | how many main branches | 3 to 5 | 4 to 6 | 3 to 4 | 2 to 3 |
| `first branch` | share of the height where the first branch leaves | 0.40 | 0.33 | 0.38 | 0.62 to 0.70 |
| `first side` | `outside` the first curve, `away` from the lean, or `either` | outside | either | away | outside |
| `profile` | the branch's line: `curve` (dip then rise), `chokkan` (level, rising at the end), `shakan` (level) | curve | chokkan | shakan | curve |
| `branch length` | columns, e.g. `8 to 14`; left out, lengths follow the spread | by spread | by spread | by spread | 8 to 14 |
| `twigs` | a twig inside each pad: `1` or `0` | 1 | 1 | 1 | 0 |
| `apex pad` | chance of a pad on the apex, 0 to 1 | 1 | 1 | 1 | 0.6 |
| `back pad` | a pad behind the trunk: `yes` or `no` | yes | yes | yes | no |
| `planting` | how far in from the pot's edge the base stands, as a share of the pot's width | 0.43 | 0.48 | 0.38 | 0.35 to 0.40 |
| `planter` | `wide` (the run's usual choice) or a planter's name, yours included | wide | wide | wide | wide |
| `leaves` | the characters inside the pads, e.g. `&*` or `*^` | drawn | drawn | drawn | drawn |
| `weight` | how often it appears when `style = auto` | 10 | 10 | 10 | 10 |

The trunk's line shape comes with the base: an S-curve with three movements tightening
upward (moyogi), straight (chokkan), a lean with a bow against it (shakan), or the
literati's four reversals (bunjin); `movement`, `apex`, `lean` and `bow` set how far it
moves. Twin trunks grow only on the built-in informal upright.

## Checking your work

`xuuxij-bonsai --print-config` shows the settings a run would use; a form or planter
name that is not accepted means its file was skipped (the reason is printed just
before). `xuuxij-bonsai --style NAME --seed 1 --once` grows the same tree every time,
so you can change a number and compare. The tools in `tools/` render off-screen in a
moment: `python3 tools/render_review.py out 1 2 3 style=NAME` writes the trees and
their numbers to `out/`, and `python3 tools/render_review.py out 1 pot=NAME` shows a
planter under a tree.
