# Round 3: the tree and planter brought forward (the landscape fixed)

What the reference frames show (scene2\m1\0170, scene2\c6\0780, scene\b3\0175): the tree is
drawn as thin glyphs in mid tones over a pale, luminous ground. A moyogi trunk nine cells wide
reads as a hatch of tan hairlines; the pads as a green stipple of the same weight as the lake's
dither; the Teizan and stand as red wire on black. "Prominent" = the tree is the darkest mass
in the picture and its silhouette is closed: a bonsai against a bright sky is a dark trunk, dark
pads with a lit crown, a solid pot. Three levers, in order of effect: value (the tree's slots
darker and more saturated), mass (the trunk's core and the pots' bodies filled), and a clean
margin (the halo). Nothing in the backdrop moves.

## (a) Palette: the tree's slots (the landscape's untouched)

| slot | old | new | why |
|---|---|---|---|
| 3 trunk, branches, Teizan trim | #784c20 | #4f3014 | bark in shade, near-ink but warm: on the lake (#a8c4db) and mist the strokes become dark lines, not tan ones; on black the core (b) carries the base |
| 2 leaves shaded, buds, moss | #2f8f3e | #1f6d2b | the pads' body is the darkest green on screen: L 50 → 38 against the lake's 77; still a living green; on the navy hills it differs by hue |
| 10 leaves lit (the cap band), opening buds | #52c95a | #3db04a | the light stays clearly lighter than the body but loses the pastel that merged with pale water; saturated |
| 11 growing tip, autumn yellow, bold trim (key-fret) | #f2d33c | #d9a51a | a deeper gold: the old yellow sat at the lake's own value (L 84 vs 77) and lived on hue alone; gold on black is gilt on the Teizan |
| 9 autumn red, bold body (lit rim) | #e0452b | #d33a1e | a touch deeper; holds on mist and on black; the rim's bright edge |
| 1 rosewood stand, Teizan body | #8a3324 | #9c4a30 | the lines on black brighten a step; at ▒ (50 %) over black it is #4e2518, a dark clay body |

No shared slot moves (4/12 oval, 6/14 celadon, 7 gravel, 8 shadow stay the landscape's).

## (b) Glyphs and strokes

**Trunk** (make_trunk): keep the glyphs (`|` columns, `/` `\` at the moving edges, the nebari
`__/` `\__`). New: where the trunk is 3 or more wide, its **interior cells** (the `|`s between
the two edge glyphs) are drawn on a **black background** (bg slot 0) in slot 3; the two edge
cells keep the backdrop's bg. The trunk becomes an ink mass with bark lines, edged by the warm
strokes; where it is 1-2 wide (the upper trunk, all branches) nothing changes. On the table
rows the bg is black already, so the base looks as now. (If the renders say the core is too
heavy, the fallback is the same cells with glyph `▒` in slot 3 on the backdrop's bg, no black.)

**Branches**: glyphs unchanged (`~` level, `/` `\` rising/falling). Weight: a **primary's first
40 %** of its length is drawn two rows thick: for a cell with glyph g at (y, x), also (y+1, x)
gets `_` if g is `~`, else g itself, unless that cell is already wood or leaf. Secondaries stay
single.

**Leaves** (fill_pad): sets `&*` 65 % → 75 %, `*^` 35 % → 25 % (the needle set is lighter).
Edge ring `.,'` unchanged. Cap band (the top 40 % of each column, bold = slot 10) unchanged.
New: the **pad's bottom row** (y = cy+1, the flat base, where the cell is not an edge cell) is
drawn in **black** (fg slot 0) with the leaf glyph: the shaded underside. Three tones per pad,
lit top / green body / dark belly, and every pad closes with a dark line. In autumn these cells
turn with the rest (the turn recolours leaf cells).

**Bold**: leaves lit bold (slot 10) as now; the tip bold (slot 11) as now; the trunk never bold
(its bold is the gold).

## (c) Weight (FORMS)

- moyogi `trunk_width ("by_height", 8.0, 6, 9)` → `(7.0, 7, 10)`; chokkan `(7.5, 8, 9)` →
  `(7.0, 8, 10)`; shakan `(9.0, 6, 7)` → `(8.0, 7, 8)`; bunjin `("drawn", 3, 4)` unchanged (the
  literati is thin by definition; its weight comes from (a), the core where it is 3 wide, the
  black bellies and the halo).
- taper `w = 1 + (w0-1)(1-t)^1.3` → exponent `1.15` (the trunk keeps its width a little longer
  into the middle: at t=0.5, 5 cells instead of 4 from a base of 9).
- `leafiness` default 1.0 → 1.1 (pads a tenth bigger; no more, the tree must stay a bonsai).
- Primaries two rows thick for their first 40 % (b).

## (d) The planter and stand

The outlines stay; the bodies fill. Rule: inside a pot's silhouette, every blank cell of a
**body row** (not the soil row, not the feet row, not the shadow) becomes `▒` in `b` (the body
colour: Teizan slot 1, oval slot 4, celadon slot 6). Exact rows:

Teizan (pot_teizan), rows 5-7, the key-fret units with per-character paint:
```
row 5  unit "▒___▒▒"  paint "bTTTbb"   filler "▒" / "b"
row 6  unit "|▒▒_|▒"  paint "TbbTTb"
row 7  unit "|_|▒▒▒"  paint "TTTbbb"
```
(`row()` already takes a paint string of the unit's length; `run()` takes the filler.) Rows
0-4 and 8 unchanged (the `=` mouldings are dense already; row 0 and 3 stay bold B = the lit
rim). Row 9 (feet) stays open. Row 10 (shadow): `-` → `▒` in `s` (a soft cast shadow).

Oval (pot_oval): rows 3-4 (the wave scroll on blanks) blanks → `▒` in `b`, the scroll stays
`B`; `=` rows unchanged; shadow `-` → `▒` in `s`. Celadon, drum, hexagon, bunjin pot: the same
rule (blanks in body rows → `▒` b; shadow → `▒` s).

Stand (stand_rows): rows 2-3 (the apron: `  ___ ` and `_/   \`) blanks → `░` in `b` (a lighter
fill, so the openwork still reads as carved); the leg rows stay open; the feet row unchanged;
shadow `-` → `▒` in `s`. The top board (rows 0-1) is already solid lines.

## (e) The halo

Yes. For every tree cell drawn (wood, leaf, bud, tip; not the planter, not fallen leaves or
dust, not leaves in the air), each of its **8 neighbours, 1 cell**, that holds no tree or
planter cell becomes a **blank in its own backdrop bg** — but only if that backdrop cell is a
texture or a light stroke (char in `░ ▒ / \ ' . - _ ~ ^` with fg not `k`). A `█` cell and any
`k`-foreground cell (pines, shore, tree tops) stay. Keep a count per halo cell of the tree
cells touching it; when it drops to 0 (a leaf fell, the crumble) the backdrop cell comes back.
On flat lake (`p on p`) the halo changes nothing; in the lake's lower dither band, the mist and
the hills it gives the ink a clean margin of paper.

## (f) Round-3 renders

1. scene2 m1 seed 1: the moyogi finished (the core, the pads' three tones, the primaries'
   weight, the Teizan filled with its gilt band, the stand's apron), and its fall (the black
   bellies turning, the halo restoring).
2. b3 bunjin: the thin trunk in the new brown on mist and lake, its pads over the hills band
   with the halo.
3. c6 shakan with the filled oval; and the second tree in the kept pot.
4. w2 200x55.
5. If cheap: m1 once more with the trunk core as `▒` in slot 3 (the fallback) beside the black
   core, so the owner can choose on the real screen.
