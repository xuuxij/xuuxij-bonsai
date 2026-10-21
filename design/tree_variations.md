# Tree variations: more foliage, more bark and branches, more forms

Companion: `tree_variations.py` (runnable; prints a specimen of every foliage style over the
same twig, every bark style on the same trunk section, every branch profile, and the new
forms as `FORMS` dicts; `specimens_seed7.txt` is its output). Everything here is an
addition: the five forms, the two leaf sets, the one pad style, the one bark stay exactly as
they are and keep most of the draw.

## 0. Recommendation in one breath

Give every tree three independent draws instead of one: a **form** (the five, plus five
new ones: windswept, broom, clump, exposed-root, semi-cascade), a **foliage** (the present
cloud, plus pine tiers, juniper lozenges, fine elm leaves, weeping willow strands, sparse
literati tufts, an azalea in bloom, a fruiting tree) and a **bark** (the present smooth,
plus plated pine bark, twisted juniper grain, rough flaking bark, a hollow trunk), with
**deadwood** (a bleached shari strip and a jin or two) as an overlay on conifers. The three
draws are not independent in weight: each form carries a table of the foliage and bark
that suit it, so a literati comes out as a twisted juniper with tufts and a shari, a formal
upright as a plated black pine with heavy branches, a broom as a flaking elm with a haze of
small leaves; the plain "S-curve with mushroom caps" keeps 45 % of the moyogi draw and no
more. Every variation is drawn with the tree's own glyph rules (one character per leaf
cell, the ink core, the halo, buds, the autumn) and the tree's own slots; the one borrowed
tone is slot 7, the gravel's soft white, for bleached deadwood.

## 1. What the research gives us

**Pads.** Pine pads are built from three shoots per year's growth and "pruned to a half
circle on top, slightly sloping from the centre to the outskirts", the underside left flat
(RBGE). Juniper tips are "flattened into a lozenge-shape (when seen from the front)", with
"all downward and upward-growing foliage pruned back", and seven such small pads fanned out
form "one large foliage pad or cloud" that in time "almost merge with its neighbours"
(bonsai4me). So a pine pad is a dome in strata with a dark underside to each stratum; a
juniper pad is low, flat and lozenge-shaped, several overlapping; a broadleaf pad is the
rounded cloud we have. The broom's crown is "ball-shaped", the fine branches starting "about
a third of the way up" (Wikipedia, bonsaiempire); the zelkova's habit is "vase-shaped", "a
broad, round-topped head". The literati's foliage is "concentrated at the top", sparse, line
over mass. Weeping is a cultivar's habit, rare in bonsai, "branches grow up, then out, then
dramatically and pendulously down" (bonsainut), and on a willow the long strands are cut
back and wired into arcs.

**Species, for the glyphs.** Japanese black pine: bark "grey-black, fissured into plates",
thick on old trunks; needles in pairs 6-12 cm. White pine: needles in fives, 3-7 cm, a
"wide, dense, conical crown". Chinese juniper: scale-like adult foliage 1.5-3 mm, needle-like
juvenile; colour "steely-blue-greens to light greens"; bark "reddish-brown or
yellowish-brown"; "great for jin and shari". Chinese elm (lacebark): "a handsome, flaking
bark of mottled greys with tans and reds"; leaves 2-5 cm, "purplish-red autumn colour".
Zelkova: bark "exfoliating in patches to reveal orange inner bark"; autumn "yellows, oranges
and reds". Trident maple: bark grey, "scaly and flaky with age", the inner bark orange-brown
in patches; three-lobed leaves. Satsuki azalea: evergreen, 1-5 inch single flowers in white,
pink, red, purple, blooming May-June.

**Deadwood.** Jin: a branch (or the leader) stripped of bark, "long, with a pleasing shape
bent or carved into it, or short, like the dead remains of a branch broken off near the
trunk"; shari: "a barkless part of trunk", "usually a small vertical strip on the front",
begun narrow and widened over years, in the driftwood style beginning "where the roots
emerge" and growing "increasingly thinner as it continues up the trunk"; uro: "a hollow,
irregularly-shaped wound in the trunk", the deciduous tree's deadwood; sabamiki: the split
or hollowed trunk, lightning's work. The exposed wood is bleached with lime sulphur, "a
weathered, bleached look". Conifers only for jin and shari; uro and sabamiki for deciduous.

**Forms.** Windswept (fukinagashi): a slanting or semi-cascade trunk, "branches lean away
from the wind", all on one side. Broom (hokidachi): "the trunk is straight and upright and
does not continue to the top of the tree", branching "at about 1/3 the height". Clump
(kabudachi): "three or more (odd number) trunks rising from one point", "the thickest and
most developed trunk forms the top", one crown. Exposed root (neagari): roots "extend above
the soil as extensions of the trunk", in the extreme "one-half to two-thirds the total tree
height"; the river eroded the bank. Semi-cascade (han-kengai): the trunk "grows upright for
a small distance and then bends downwards/sidewards", the apex "at the level of, or
beneath, the lip of the bonsai pot" and never "below the bottom of the pot"; the crown
above the rim; the trunk "should never touch the rim". Root-over-rock (sekijoju): roots wrap
a rock before entering the soil. Forest (yose-ue): several trees, odd in number, the
smallest at the back; it is not one tree and is left for another round (section 8).

**Text art.** cbonsai draws leaves as `&` and wood by direction (`/~` `\|` `/|\` `|/`,
shoots `\_` `_/`). The asciiart.eu bonsai (llizard) uses `#o#` foliage over `{}` bark; the
asciiart.website pine ("Pine Tree In The Wind") stacks tiers with `>` `<` and `%` needle
clusters, `;` `:` scattered needles; its "Old Tree" is bare `(` `)` `;` `:`; its broadleaf
"Tree" is a crown of `@`. Joan Stark's ramp `_,.-'"^` gives characters by their height in
the cell, which the willow's strands and the pine's seams use.

## 2. The three draws and the settings

| Setting | Default | What it does |
|---|---|---|
| `style`, `styles` | as now | the form; the new names join: `fukinagashi hokidachi kabudachi neagari hankengai`; default weights `moyogi:15 chokkan:10 shakan:30 bunjin:30 kengai:15 fukinagashi:8 hokidachi:8 kabudachi:6 neagari:5 hankengai:8` (the five classics keep 74 % of the draw) |
| `foliage` | `auto` | the foliage style: auto (drawn by the form's table, section 6), or `cloud pine juniper elm willow tuft azalea fruit` |
| `foliages` | `auto` | `name:weight ...`: when set, replaces every form's own foliage table |
| `bark` | `auto` | the bark and branch wood: auto (by the form's table), or `smooth plated twisted rough hollow` |
| `barks` | `auto` | `name:weight ...`: when set, replaces every form's own bark table |
| `deadwood` | `auto` | a shari and jins: auto (by the form's chance, conifers only), `yes` (always, on any foliage), `no` |
| `leaves`, `leaf_edge` | as now | when `leaves` is set it replaces the inside set of whichever foliage style is drawn (the shape stays the style's); `leaf_edge` likewise the edge set |
| `autumn_colors` | as now | a foliage style with its own autumn (pine, juniper, willow, tuft: gold only) uses it unless this setting was changed from the default |

A user form file (`docs/custom.md`) gains `foliage:`, `bark:`, `deadwood:` (a name, or
`name:weight ...`), the new `profile` values (`wind`, `droop`, `fan`) and `first side: with`,
and may take `fukinagashi`, `hokidachi`, `kabudachi` or `neagari` as `base:`. `hankengai`,
like `kengai`, is its own thing and no base.

The tree's report (and `render_review.py`'s numbers) gains `foliage`, `bark`, `deadwood`.

## 3. Foliage styles (A)

All share the present machinery: a family = members (twig, rx, ry, cy, cx), the pad = the
union of flat-bottomed domes (each cell by its nearest dome, `d` its normalised distance),
feathering for `d > edge_at` with edge characters, the family's own twigs covered, the
"no specks" rule, buds opening, one character per leaf cell. A style changes: the radii, the
character sets, where the lit band is, the underside, holes, accents, and (willow) a second
pass. Paint letters as in the specimens: `L` lit (bold green, slot 10), `l` shaded (slot 2),
`u` underside or seam (black foreground, the leaf glyph), `e` edge, `A` accent.

### cloud (the present pad; weight 40)
Unchanged: inside `&*` (75 %) or `*^` (25 %) per tree, edge `.,'`, `rx = 0.5 len + 4`,
`ry = rx/3.5 + 1`, feather from `d = 0.8`, lit top 40 % of each column, bottom row black.
Autumn as set. Suits every form.

### pine (needle tiers; weight 18)
- inside `^^*` (two `^` to one `*`), edge `'.`, seam `.^` in black.
- `rx` as now, `ry = max(4, rx/3.5 + 1)` so there are always two strata.
- **Shape rule**: the dome union as now, but the tone goes by the row's height `r` above the
  pad's bottom row (r = 0 the bottom): `r % 3 == 0` a **seam** (black fg, chars `.^`),
  `r % 3 == 1` shaded, `r % 3 == 2` lit; the top cell of every column is lit whatever its
  `r` (never a dark top); the bottom row is the underside as now. Each stratum reads lit /
  shaded / dark, the dark line being the shadow of the pad above: the layered pine of the
  references. Where a seam falls on the family's twig the leaf covers it as now.
- The secondary's pad (rx 9, ry 4) sits a row or two above the primary's, so the two
  domes' strata are offset: the mass steps.
- Branches: with the plated bark the branches are heavy (section 4); on chokkan 40 % of
  pines take the `droop` profile (old pines sag).
- Autumn: gold only (pines shed old needles yellow); then they fall as any leaf.
- Suits chokkan, shakan, bunjin, kengai, fukinagashi, hankengai; moyogi at a low weight.

### juniper (flat lozenge pads; weight 14)
- inside `%&`, edge `.,`; `rx` x 1.15, `ry = max(2, rx/5 + 1)`: wide and flat, lozenge
  from the front, flat below (bonsai4me).
- lit top 35 %, feather from `d = 0.78` (a tighter edge), bottom row black.
- **Two twigs per primary** (`twigs = 2`: the second at 0.35 of the primary, rising), each
  with a pad of rx 10, ry 3, the secondaries' pads one row above the primary's: three
  overlapping lozenges fanned into one mass with notches, the reference's "many small pads
  forming a larger one".
- Autumn: gold only (default), or `rosewood` if a plain-red word is added to the colour
  list (junipers bronze in winter; plain red is slot 1, #9c4a30, exactly that) - optional.
- Suits moyogi, shakan, bunjin, kengai, fukinagashi, hankengai. Pairs with twisted bark and
  deadwood.

### elm (fine small leaves; weight 8)
- inside `:;":;*` (six characters: `:` and `;` twice, `"` and `*` once; marks at three
  heights in the cell give the haze its grain), edge `.,`.
- `ry = rx/2.5 + 1` (a taller, rounder dome), lit top 40 %, holes: 5 % of inside cells
  left empty (light through the fine twigs), bottom row black.
- Autumn as set (elm goes yellow then purplish-red: the default list).
- Suits hokidachi (its native crown), moyogi, chokkan, kabudachi, neagari. Pairs with rough
  and hollow bark and knuckled branches.

### willow (weeping strands; weight 5)
- **Cap**: a dome over the branch's end (centre at 0.85 of the branch), `rx = 0.3 len + 3`,
  `ry = 3`, inside `&*`, edge `.,'`, lit top row of each column, no black underside (the
  strands hang from it).
- **Strands**: from every second cell of the branch from t = 0.25 of its length, a vertical
  run downward of `3 + 7 t` cells (+0 to 2 at random): the first two cells `|` lit, then
  `|` 60 % `;` 25 % `:` 15 % shaded, the last cell `,` or `'`. A strand under the cap
  starts on the row below the cap; a strand stops at wood, at the blocked area, and two rows
  above the soil (`B - 2`). Strands are exempt from the "no specks" rule (they are one cell
  a row by design) and the pad's box for the air rule (`near`) extends down by the longest
  strand, so no other family's pad crosses a curtain.
- No secondary twig (`twigs = 0`); the branch takes the `droop` profile (section 4) so the
  cap hangs at the branch's lowest point.
- Autumn: gold only (willows go yellow); the strands let go cell by cell like any leaf,
  so a curtain thins from random places, which looks right.
- Suits moyogi, shakan, kabudachi only (level or dipping branches with room below).

### tuft (sparse literati tufts; weight 6)
- inside `^^*'`, edge `'.`; `ry = min(ry, 3)`; feather from `d = 0.75`; 20 % of inside
  cells left as holes; lit = the top row of each column; no black underside (air under a
  tuft, not shadow).
- The form's small pads (bunjin: rx 8-12, ry 3-4) make these tufts; on a windswept the pads
  are the form's streaming ones.
- Autumn: gold only.
- Suits bunjin, fukinagashi, neagari, hankengai. Pairs with twisted bark and deadwood.

### azalea (the cloud in bloom; weight 5)
- The cloud exactly, inside `&*`, plus **accents**: among the non-edge, non-underside cells
  in the top 60 % of each column, 18 % become a bloom `@` in bold red (slot 9) and 5 % a bud
  `o` in rosewood (slot 1, plain red); at least three blooms per pad (add if the draw gave
  fewer). An accent cell is a leaf cell with a different attribute: it buds, it is counted
  with the leaves, it falls.
- Autumn: the blooms let go first (the fall's order puts accent cells at the front of the
  shuffle; they are red already so the turn leaves them), then the leaves turn and fall as
  set.
- Suits moyogi, shakan, kabudachi, neagari (azaleas are grown in all of them; neagari
  "especially with azaleas").

### fruit (a fruiting tree; weight 4)
- The cloud with 7 % of the non-edge, non-underside cells in the **lower 60 %** of each
  column as a fruit `o` in gold (slot 11, bold yellow): a persimmon or crab apple hanging
  under the leaves.
- Autumn: the leaves turn and fall as set; the fruit stays gold and goes last (the end of
  the shuffle), so for a while the bare tree holds its fruit, then that drops too.
- Suits moyogi, chokkan, shakan, kabudachi.

## 4. Bark and branch styles (B)

A bark style names the trunk's glyphs and the branches' wood together. The trunk stays a
row of `edge + core + edge` tapering by `w(t)`, the core on black as now (`k`), the edges
on the backdrop (`b`), nebari roots as now. Paint letters: `b` bark edge, `k` ink core,
`v` the hollow's void (a blank on black), `d` deadwood (slot 7 on black), `j` jin (slot 7
on the backdrop).

### smooth (the present bark; weight 45)
Unchanged: edges `|`, `/` `\` where the trunk moves; core `|`. Branches: the `line` style
as now (`~` level, `/` `\`, primaries two rows thick for their first 40 %).

### plated (old black pine; weight 15)
- Edges as smooth. Core in a **brick bond**: cell `k` of row `i` is `|` when
  `(k + i // 2) % 3 == 0`, else `_`: plates two rows tall and three cells wide, each row
  pair offset, the `_` the plate's lower edge on the black. Reads as the fissured plates of
  an old pine.
- Branches **heavy**: primaries two rows thick for 70 % of their length, secondaries two
  rows for their first 30 %.
- Suits chokkan, moyogi, shakan, hankengai; with pine, cloud (needle set) and tuft.

### twisted (juniper grain, literati; weight 15)
- Edges `(` `)` on straight rows (a round trunk), `/` `\` where it moves. Core: `|` with a
  `(` where `(k - i) % 4 == 0` - one grain line drifting a column a row, a spiral up the
  trunk; on a moving row the **whole core is the diagonal** (`\\\\\`): the grain turns with
  the movement.
- Branches: `line`.
- Suits bunjin, shakan, kengai, hankengai, fukinagashi; with juniper, pine, tuft. The
  natural bark for deadwood.

### rough (flaking elm, trident maple; weight 12)
- Edges `{` `}` on straight rows, `/` `\` moving. Core: `|` 78 %, `%` 12 %, `:` 10 % per
  cell (the mottled flakes on the dark core); one **knothole (uro)** `()` two cells wide in
  the core at 40-55 % of R, trunks 6 or wider.
- Branches **knuckled**: a jog of one row every 3 to 5 cells (up or down), and after a dip
  the next level cell is `_` so the branch sags into the jog (`~~~/___\_~~~`); the thick
  under-row as now.
- Suits moyogi, chokkan, hokidachi, kabudachi, neagari; with elm, cloud, azalea, fruit.

### hollow (sabamiki, the split trunk; weight 6)
- Edges as smooth. Where the trunk is 5 or wider, from 10 % to 45 % of R the core is
  `(` + blanks + `)`: the inner bark lines around a **black void** (blank cells on the black
  background; they are wood cells for the halo and the crumble and dust like the rest).
  The row above the void has `'` across the core (the ragged lip), the row below `.`.
- Branches knuckled.
- Suits moyogi, chokkan, kabudachi, hokidachi (old deciduous trees); with elm, cloud,
  fruit. Never with deadwood.

### deadwood (an overlay, not a bark)
- **Shari**: a strip of deadwood up the trunk on the outside of the first curve (the lean's
  outer side on shakan and fukinagashi): the edge plus two core cells at the base, the edge
  plus one from 20 % of R, the edge alone from 40 %, ending at 55-75 % of R. Its glyphs are
  the bark's own (`|`, the diagonals), painted `d`: slot 7 (#c9d0d6, the gravel's soft
  white, which the planter already uses) on the black core, and on the edge cell over the
  backdrop. The bleached strip of the references, widest at the roots.
- **Jin**: a dead branch of 3 to 6 cells, `-~-'`, the last cell one row up (the splintered
  tip), in slot 7, from the trunk at 55-70 % of R on the side with no live branch there; on
  a windswept, on the windward side. A stroke of kind `jin` (added to `BRANCH_KINDS` so it
  crumbles), no pad, drawn after the trunk. Chance per form (section 6).
- **Top jin** on bunjin and fukinagashi (50 % of their deadwood trees): the trunk's last
  three cells above the apex pad's base are kept (`apex_pad` currently removes them) and
  painted `j`: `|` `|` `'`, a dead leader through the tufts.
- Only with pine, juniper or tuft foliage, over smooth, twisted or plated bark. The `uro`
  of rough bark is the deciduous tree's deadwood and needs no overlay.
- A deadwood cell is wood: it is drawn with the tip, keeps the halo, crumbles to dust.

### The branch profiles (summary; specimens in the script)
| profile | rule | used by |
|---|---|---|
| curve, chokkan, shakan, fallb, twig | as now | as now |
| wind | level; lifts a row every 8 cells; one forced step down at 85 % (the tip drops) | fukinagashi |
| droop | level for 60 %, then a row down every 3 cells | willow; 40 % of pines on chokkan |
| fan | rises from its first cell; the fan's slopes 1 row per 0.6 columns (centre) to 1 per 2.2 (sides) | hokidachi |
| knuckled (a flag, not a profile) | a jog of a row every 3-5 cells, `_` after a dip | rough, hollow bark |
| heavy (a flag) | thick for 70 % instead of 40 %; secondaries thick for 30 % | plated bark |

## 5. New forms (B) - the numbers

The dicts are in `tree_variations.py` (`NEW_FORMS`), ready for the `FORMS` table; new keys
are marked there. In the table's own terms:

| | fukinagashi (windswept) | hokidachi (broom) | kabudachi (clump) | neagari (exposed root) | hankengai (semi-cascade) |
|---|---|---|---|---|---|
| height | 0.42-0.50 | 0.50-0.58 | 0.50-0.60 | 0.58-0.68 | its own planner: rise 10-14 rows, out 22-30 columns, drop 6-10 rows |
| spread | 0.65-0.80 | 0.60-0.72 | 0.70-0.85 | 0.40-0.55 | - |
| trunk_width | by_height 8.0, 6-8 | by_height 7.0, 7-9 | by_height 8.0, 6-8 (the others 0.70 and 0.55 of it) | drawn 4-6 | 5, tapering along rise + out |
| line | lean 1.0-1.4 (30-35 degrees from vertical, twice shakan's), bow 2-4 | straight, ending at `trunk_top` 0.30-0.38 of R | s-curve, movement 4-8, apex -3..3; two more trunks forking 1-2 rows up: (0.62-0.72 R, opposite the first curve, lean 8-12) and (0.42-0.52 R, the first curve's side, lean 10-14) | s-curve 6-10 above the legs; `roots: stilts`, `root_height` 0.25-0.35 of R, 3-4 legs 2 cells wide at the top and 1 at the soil, splayed to +-(w0 + 3) columns, one may cross another; the nebari row is replaced by the legs' feet `_/` `\_` | rises, arcs over the rim (the kengai's own rise), then runs out per column with an easing drop (shallow first, steeper at the end), never below the pot's body |
| movement/apex | the lean | 0 | small | 6-10 / -4..8 | - |
| branches | 3-4, first 0.35-0.45, `first_side: with` (the lee), `sides: lee` (no alternation) | 5-7 in a **fan** from the trunk's top, `fan_height` 0.55-0.65 of (R - top), each forking at 45 % and 70 % | 2-3 on the main trunk (first 0.45), 1-2 on each other trunk on its outer side | 2-3, first 0.55-0.62, length 10-16 | 2-3 along the run at 40 %, 75 % and the tip, pads above the trunk (rx 7-10, ry 2-3) |
| profile | wind | fan | curve | curve | fallb |
| twigs | 1 | 2 | 1 | 1 | 0 |
| pads | (9-13, 2-3): thin, streaming | `crown`: one dome over the whole fan, base at 0.55 of the fan's height, rx = half the fan's width + 2, ry = 0.5 (R - top); the lower fan shows bare under it | by_branch | by_branch | crown over the rise's inner branch (8-10, 3-4) as the kengai's; the run's pads |
| apex pad / back pad | 0.7 / no | 0 / no | 1.0 / no | 1.0 / no | the cap on the arc as the kengai's / no |
| planting | 0.30 away from the lean | 0.50 | 0.50 | 0.50 | 0.35 on the fall side |
| planter | oval (wide) | oval | oval | drum; `rock` 30 %: the legs clasp a boulder of `▒` in slot 8 on black (sekijoju) | hexagon on the **normal** stand (the drop 6-10 rows stays inside the pot's body, clamped to its rows - 1) |
| deadwood chance | 0.6, the jin on the windward side | 0 | 0 | 0 | 0.4 |
| weight | 8 | 8 | 6 | 5 | 8 |

Notes on each:
- **fukinagashi** needs `sides: lee` (every branch on the first side) and the `wind`
  profile; `length_taper` 0.10 keeps the upper branches long (they stream together). Width
  check at 135 columns: R ~ 48, lean 58 columns, first branch 32: ~98 of the 115 available.
  The pads are thin lenses (ry 2-3) so the foliage streams; tuft/pine/juniper only.
- **hokidachi** needs `trunk_top` (the trunk stroke ends there; `apex_pad` is 0 and the
  crown pad covers the fan's upper half, growing from the fan's centre outward). The fan's
  five to seven branches leave the trunk's top row spread across its width, slopes by their
  slot (the centre one near vertical). Elm or cloud foliage; rough, smooth or hollow bark;
  knuckled branches when rough or hollow.
- **kabudachi** generalises `plan_twin`: a `trunks` list instead of one twin; forks at 1-2
  rows (not 2-5); each extra trunk gets `trunk_branches` primaries on its outer side with
  pads; the air rule between families as the twin's; one canopy (the main trunk's apex pad
  is the top). The main trunk's own movement is small (4-8) so the three lines read together.
- **neagari** replaces the nebari row with legs: from the trunk's base row (at
  `root_height` R above the soil) 3-4 root strokes go down to the soil, each a thin trunk
  (`make_trunk` with w0 2 tapering to 1, the edge glyphs `|` `/` `\`), fanned so their feet
  spread +-(w0 + 3) columns; the ground shows between them (no ink core). With `rock`, the
  space between the legs from the soil to 70 % of the legs' height is a boulder: `▒` in
  slot 8 on black with a `'` `.` top line, the legs drawn over it.
- **hankengai** is `plan_kengai`'s sibling: the same rise and crown; then instead of the
  fall beside the stand, a run: sampled per column over `out` columns, `y` easing from the
  rim's row to rim + `drop` (y = rim + drop * (j/out)^1.8), three rows thick for the first
  50 % (top row `~`/`\`, middle row ink `|`, bottom row `_`), two rows to 80 %, one after;
  the trunk never touches the rim (it leaves two columns outside it as the kengai does).
  The hexagon sits on the normal stand, so the drop stays within the pot's body rows.

## 6. How they combine (C)

**The draw** (per tree, after the form): foliage from the form's table (below, or the new
form's own); bark from the form's table, **filtered** by the foliage (`BARK_BY_FOLIAGE`);
deadwood by the form's chance, only when the foliage is pine, juniper or tuft and the bark
is not rough or hollow. `foliages` / `barks` set by the user replace the form tables;
`foliage` / `bark` set by name win over everything.

| form | foliage weights | bark weights |
|---|---|---|
| moyogi | cloud 45, pine 15, juniper 10, elm 10, azalea 8, willow 6, fruit 6 | smooth 50, rough 20, plated 15, hollow 10, twisted 5 |
| chokkan | pine 40, cloud 35, elm 15, fruit 10 | smooth 45, plated 35, rough 15, hollow 5 |
| shakan | cloud 30, pine 25, juniper 25, azalea 10, willow 5, fruit 5 | smooth 45, twisted 30, plated 15, rough 10 |
| bunjin | pine 35, tuft 25, cloud 20, juniper 20 | twisted 50, smooth 40, plated 10 |
| kengai | juniper 40, pine 30, cloud 30 | smooth 45, twisted 45, plated 10 |
| fukinagashi | pine 45, juniper 30, tuft 25 | twisted 50, smooth 30, plated 20 |
| hokidachi | elm 55, cloud 45 | rough 50, smooth 35, hollow 15 |
| kabudachi | cloud 40, elm 25, pine 20, azalea 15 | smooth 50, rough 35, hollow 15 |
| neagari | azalea 30, elm 30, cloud 25, tuft 15 | smooth 60, rough 40 |
| hankengai | pine 35, juniper 35, cloud 20, tuft 10 | twisted 45, smooth 35, plated 20 |

Bark by foliage (a draw outside the list is redrawn): cloud: any; pine: smooth plated
twisted; juniper: smooth twisted; elm: smooth rough hollow; willow: smooth rough; tuft:
smooth twisted plated; azalea: smooth rough; fruit: smooth rough hollow.

Deadwood chance by form: bunjin 0.5, fukinagashi 0.6, kengai 0.4, hankengai 0.4, shakan
0.3, chokkan 0.15, moyogi 0.1, the rest 0.

What this does to the mix: over the default style weights, about a third of all trees are
the present look exactly (classic form, cloud foliage, smooth bark); the moyogi-with-domes
the owner tires of is 15 % x 45 % x 50 % ~ 3 % of trees; the literati and slanting trees,
which he likes, are 60 % of the classics and now come as twisted junipers with tufts and
shari, plated pines, windswept trees. Nothing already there is removed or re-weighted
except that each form's draw now spreads over its foliage and bark tables.

## 7. What to build, in order (so the first renders come soon)

1. The foliage styles in `fill_pad` (a `style` argument; the willow's strands as a second
   pass; radii in `pad_radii`; twigs by style in `plan_secondaries`), the `foliage` setting,
   the per-style autumn colours and the accent order in `fall`. Table-only forms need
   nothing else to render the foliage on every existing form.
2. The bark styles in `make_trunk` (edge/core glyphs; the hollow's void) with the wood
   cell's fourth element carrying a paint string (`b k v d j`) that the draw's `wood()` maps
   to attributes (`b` wood on the backdrop, `k` wood on black as `self.ink` does now, `v` a
   blank on black, `d` slot 7 on black, `j` slot 7 on the backdrop); the branch flags
   (heavy, knuckled) in `plan_branch`; the `bark` setting.
3. Deadwood: the shari paint in `make_trunk`, the `jin` stroke kind, the top jin in
   `apex_pad`; the `deadwood` setting.
4. Forms: fukinagashi and hokidachi (new keys in `plan`/`plan_primaries`/`plan_branch`, the
   crown pad), then kabudachi (`plan_twin` generalised), neagari (the legs, the rock), and
   hankengai (`plan_hankengai`). The loader (`load_user_form`) learns the new keys and bases.
5. Report fields, `render_review`, the gallery's new cards, README's settings rows,
   `docs/custom.md`, `docs/references.md` (section 10).

## 8. Not in this round, and why

- **Forest (yose-ue)** and the multi-tree groups: several separate trees in one tray is a
  different planning model (several `Tree` plans sharing a planter, the autumn over all of
  them, the clock). Worth its own round after the clump proves the multi-trunk air rules.
- **Raft (ikadabuki)** and **octopus (takozukuri)**: a raft is a clump on a horizontal
  trunk (buildable from kabudachi plus hankengai's run later); the octopus is a curiosity.
- **Half-blocks for finer needles** (`▀▄`): not in the font.
- A second green for juniper's blue-green or a brown for unbleached deadwood: no slots; the
  bronze autumn via plain red (slot 1) is the one offer, optional.

## 9. What I want to see in the first renders

Text via `tools/render_review.py` (the 100 % frame and the numbers), PNGs via
`tools/scene_review.py` for the three marked *, at 135x120 unless said.

1. **One tree, every foliage**: moyogi seed 1 with `foliage=` cloud, pine, juniper, elm,
   willow, azalea, fruit (seven renders of the same tree). I am checking: the pine's strata
   read as tiers and not as stripes; the juniper's three lozenges make one mass with
   notches; the elm's haze holds together on the lake (if it dissolves, the fix is `*` to
   two in six); the willow's curtains clear the pad below and the soil; the blooms count
   (3 to 8 a pad) and the fruit sits low. * the juniper.
2. **The literati**: bunjin seed 2 with tuft + twisted + deadwood, and the same seed with
   pine + smooth, no deadwood. Checking: the spiral `(` and the diagonal rows on a trunk 3-4
   wide (is there room for the grain, or does it need w >= 4?); the shari's grey on black
   beside the brown; the top jin through the tufts. *
3. **The formal upright**: chokkan seed 3 with pine + plated (heavy branches, 40 % droop),
   and with cloud + hollow. Checking: the brick bond at 8-10 wide; the void's size on the
   lake and whether the lips `'` `.` close it; heavy branches against the pads.
4. **The slanting tree**: shakan seed 4 with juniper + twisted + deadwood: the shari on the
   lean's outer side, a jin on the inner side.
5. **The new forms**, seeds 1 and 2 each, foliage and bark auto: fukinagashi, hokidachi,
   kabudachi, neagari (one with `rock`), hankengai. Checking: the windswept fits the width
   and its pads stream; the broom's crown is one mass with the bare fan under it (* seed 1);
   the clump's three lines read as one tree; the legs' feet and the ground between them;
   the semi-cascade's run stays inside the hexagon's body and its pads sit on the trunk.
6. **Autumn phases** (`phases`): the pine (gold only, then the needle fall) and the azalea
   (blooms first, then the turn) on moyogi seed 1.
7. **200x55**: hokidachi and fukinagashi, the two widest, to see the fan and the stream on
   the short screen.

If something in 1-4 fails on sight, the round-2 move is the numbers (radii, shares, the
character mix), never the shape rules; the rules are the design.

## 10. References (for docs/references.md)

Forms
- Bonsai styles (all the named styles; neagari's root share; han-kengai's apex rule;
  kabudachi; sabamiki, sharimiki). https://en.wikipedia.org/wiki/Bonsai_styles
- Bonsai styles with proportions (shakan 60-80 degrees, broom at a third, literati's round
  pots, kabudachi's crown, sharimiki thinning upward). https://www.bonsaiempire.com/basics/styles
- The Japanese names (fukinagashi, hokidachi, neagari, sabamiki, bankan, nazashi weeping,
  jukei silhouettes). https://magiminiland.org/BigPicture/JapaneseStyles.html
- Semi-cascade: apex at or below the rim, never below the base; the trunk never touches the
  rim. https://gardenerspath.com/how-to/pruning/grow-cascade-bonsai/
- Semi-cascade's trunk angle and the visual-mass rule. https://bonsailearningcenter.com/?p=55088
- Exposed root (neagari): the river-bank origin, azaleas. https://mail.bonsainut.com/threads/neagari-style.8146
  and https://www.bonsaiempire.com/forum/advanced-techniques/6717-neagari-chinese-elm
- Weeping bonsai: branches up, out, then pendulously down; the willow 'Rokkakudo'.
  https://www.bonsainut.com/threads/weeping-trees.14500 and
  https://issuu.com/internationalbonsai/docs/2021_4/s/14128100

Foliage pads
- Pine pads: three shoots a pad, a half circle on top, the underside flat.
  https://stories.rbge.org.uk/archives/29158
- Juniper pads: flattened, lozenge from the front, many small pads fanned into one.
  https://bonsai4me.com/styling-juniper-bonsai-branches-part-two-wiring-and-placement/
- Juniper foliage colours, bark, deadwood. https://www.bonsaiempire.com/tree-species/juniper

Deadwood
- Jin, shari, uro, sabamiki, tanuki; lime sulphur. https://en.wikipedia.org/wiki/Deadwood_bonsai_techniques
- Making jin and shari; evergreens only. https://www.bonsaiempire.com/basics/styling/deadwood

Species (bark and leaves)
- Japanese black pine: bark grey-black fissured into plates; needles in pairs.
  https://en.wikipedia.org/wiki/Pinus_thunbergii and
  https://hortflora.rbg.vic.gov.au/taxon/ad8b4424-5340-11e7-b82b-005056b0018f
- Japanese white pine: needles in fives, a dense conical crown. https://en.wikipedia.org/wiki/Pinus_parviflora
- Chinese juniper and shimpaku: scale and needle foliage. https://en.wikipedia.org/wiki/Juniperus_chinensis
- Chinese elm (lacebark): flaking bark of mottled greys, tans and reds; small leaves.
  https://en.wikipedia.org/wiki/Ulmus_parvifolia
- Zelkova: vase-shaped, bark exfoliating to orange, autumn yellows to reds.
  https://en.wikipedia.org/wiki/Zelkova_serrata
- Trident maple: three-lobed leaves; bark scaly and flaky with age, orange-brown beneath.
  https://en.wikipedia.org/wiki/Acer_buergerianum and https://mortonarb.org/?p=3107
- Satsuki azalea: evergreen, 1-5 inch flowers, May-June. https://en.wikipedia.org/wiki/Satsuki_azalea

Text art
- cbonsai: leaves `&`, trunk and shoot glyphs by direction. https://gitlab.com/jallbrit/cbonsai
- asciiart.eu bonsai (llizard: `#o#` foliage, `{}` bark). https://www.asciiart.eu/plants/bonsai-trees
- ASCII trees: "Pine Tree In The Wind" (tiers `> <`, needles `%` `;` `:`), "Old Tree"
  (`( ) ; :`), a crown of `@`. https://asciiart.website/index.php?art=plants/trees
- Joan Stark's tutorial: characters by their height in the cell.
  https://ludd.ltu.se/~vk/pics/ascii/junkyard/techstuff/tutorials/Joan_Stark.html
