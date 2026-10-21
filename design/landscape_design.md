# The mountain landscape behind the bonsai: round 1 design

Companion files: `landscape_shapes.py` (the generator, runnable; the shapes it hands over are
in it), review renders in `landrev/` (`s1d.png`, `s3d.png` portrait 135x120; `w2.png` 200x55;
`t1.png` 80x24; `s1_evening.png`, `s1_night.png` the same cells under other palettes).

## Recommendation in one breath

A blue print behind a coloured tree. The whole backdrop is painted in blues and greys only, the
way the Edo *aizuri-e* were printed in Prussian blue, so the bonsai (brown, green, red, yellow)
is the one thing in colour and reads at a glance. The scene is a *sansui* in three distances:
snowy peaks high up against a sky that deepens toward the zenith, a far range dissolving in
haze, wooded hills at the sides; a band of spear mist (suyari-gasumi) hides the mountains' feet;
below it a still, pale lake fills the middle of the screen, the tree's own ground; two black
pines frame the edges; a dark shore and the black table at the bottom keep the planter on what
it was designed for. Made by "paint, halftone, ink": the scene is painted in RGB, halftoned
into the console's ░ ▒ █ over four background slots, then drawn over with ASCII strokes
(ridge lines, hatching, tree tops, pines). No font switch. Procedural from the seed: one
landscape per run, the same place for every tree.

## What the research gives us

**ASCII mountain art** (asciiart.eu, ascii.co.uk, Joan Stark's pieces): ridges are `/ \ ^`
with `_ . - '` for gentle slopes (Stark's slope ramp `_,.-'"^`: characters sit at the bottom,
middle or top of the cell, so a gentle line steps through `_ . - '` between the `/`s);
snow is blank or `'`; shade faces are hatched with `/` and `\` runs along the fall line;
forests are `^` rows; lakes are `~ - =` and `:` fields; distant tone comes from density
ramps. Stark's 1998 piece shows all of it in one (`/\` peaks, `^` snow, `=~-` water).
The tone-vs-structure distinction of Xu, Zhang and Wong ("Structure-based ASCII Art",
SIGGRAPH 2010): tone-based art maps brightness to character density; structure-based art
matches the *lines* of the picture with character shapes. Hand artists do both at once.
His image 1 is tone-based (a halftone of dots and bars); image 2 is a block picture with
greyscale gradation and black silhouettes.

**Image-to-text halftoning** (Paul Bourke's ramps ` .:-=+*#%@` and the 70-step one; ordered
dithering, Bayer 2/4/8; Floyd-Steinberg error diffusion; libcaca's study): a cell shows one
mean tone; dithering spreads the error so a gradation is smooth; ordered dither gives a
regular, calm pattern fixed to the grid (better for a static backdrop than error diffusion,
which looks organic but noisy). Text mode adds a trick ANSI/teletext artists use: a cell can
show *two* colours at once (foreground glyph over background), and ░ ▒ █ mix them at 25, 50
and 100 %, so with n background colours and m foreground colours there are far more than
n+m tones. Half-block pixels (▀ ▄) are the other classic (two square pixels per cell), used
by PETSCII, teletext and the 16colo.rs scene.

**Sansui / suiboku.** Guo Xi's three distances (high: looking up at a mountain from below;
deep: past the front mountain to the ranges behind; level: out over low hills), extended by
Han Zhuo with the mist distances where "thick mists interrupt streams and plains". Kasumi
(mist) runs in horizontal bands; from the 13th century the spear mist (suyarigasumi) with
straight edges and a cleanly rounded head, dividing near from far. Yohaku, the unpainted
space, weighs as much as the painted. Sesshū: a single strong stroke outlines the cliffs,
flat overlapping mountains and far peaks drawn against the grey sky with one line, mist wash
dividing solid from void. Tōhaku's Pine Trees: near pines in dense ink, far ones pale,
dissolving in mist. Hokusai's Red Fuji: a sky of three deepening blues, the summit's snow,
the dark forest at the foot; the *aizuri-e* of the 1830s, landscapes printed in blue alone.

**Physics.** Aerial perspective: with distance contrast falls, saturation drops, hue shifts
toward the sky's blue, detail goes. The sky is deepest blue at the zenith and paler, whiter,
toward the horizon (longer path, more scattering by haze). A still lake mirrors the pale
horizon sky far off and the deeper overhead sky near the viewer; snow in shadow is lit by
the sky and goes blue.

## The composition on his screen (135 columns x 120 rows, portrait)

Rows from the top; the tree and planter are drawn over all of it.

| rows | share | what | how it looks |
|---|---|---|---|
| 0-6 | 0-0.06 | open sky | deep blue, dithering to mid blue |
| 7 | 0.06 | the main summit | a `^` on the crest, white |
| 7-41 | 0.06-0.35 | the mountains | the main range (crest the whole width, 5-8 summits, the main one off centre at 0.33-0.39 or 0.61-0.67 of the width, a second across the centre, lesser ones between, saddles); the far range in haze seen through the saddles (crests 0.12-0.2); the wooded hills from each edge (crests at 0.22) falling toward the centre; snow above the snowline (0.42-0.58 of the main height), hatched shade faces, gullies, forest at the feet outside the centre |
| 30-41 | 0.25-0.35 | the spear mist's spears | straight-edged pale bands over the mountains' feet, the longest and highest two in the centre band (they reach row 30), three shorter ones elsewhere |
| 42-53 | 0.35-0.45 | the mist's core | a pale band the full width, its top softened over 3 rows; the hills' and the range's feet vanish into it |
| 54-95 | 0.45-0.80 | the lake | flat pale blue-grey; faint reflections of the hills at the sides only (rows 54-68, cols 0-30 and 105-134); a few `-` ripples at the sides and in the last 5 rows; from row 75 it deepens toward mid blue |
| 96-102 | 0.80-0.86 | the near shore | a dark band, tufts `" ' , .` on its top row; the pines' feet |
| 103-119 | 0.86-1 | the table | black, as the planter was designed on |

Columns: the **centre band** is cols 45-89 (0.34-0.66). Above the crown, from row 30 down,
it holds only haze and mist (the "mist valley": the range's forest is 65 % thinner there, the
hills end before it, the two highest spears are in it). The **margins** are cols 0-9 and
125-134 (the tree's MARGIN rule, `max(2, W // 13)`): the framing pines stand there, feet on
row 96, a tall one (36 rows) cut by one edge with a small one at its foot, a mid one (22 rows)
inset on the other edge; never alike on both sides.

**The quiet zone** for the tree: measured on the round-8 review frames, a moyogi fills rows
49-109 and cols 18-115; a bunjin rows 31-106, cols 56-89; a cascade rows 65-113, cols 33-90.
So: rows 54-95 are flat pale water with no dither in cols 10-124 (the dither amplitude is cut
to 35 % there) and no strokes in cols 25-110 except the last 5 rows; rows 42-53 are mist, pale
and nearly blank; rows 30-41 in the centre band are haze and spear mist. A bunjin's tip stands
against pale mist, a moyogi's crown against pale water, the trunk against pale water: dark on
light, as ink on paper. Nothing in the backdrop is green, brown, red or yellow.

## Other sizes

Everything is a share of the height and width (the `layout()` table), so the bands keep their
proportions: 200x55 gives summit row 3, mist 19-25, lake 25-44, shore 44-47, table 47-54, pines
17 and 10 rows; 80x24 gives summit row 1, mist 8-11, lake 11-21, shore row 22, table row 23,
no pines (under 30 rows), and the mountains become a two-to-five-row ridge of strokes. Under 45
rows (no planter) the shore is one row and the table the last row. The centre band and margins scale with
the width. The landscape screen reads as a long low range over a wide lake; the tiny one as a
ridge line, which is what an 80x24 terminal can hold.

## The technique, and why

**Paint, halftone, ink** (the three passes in `landscape_shapes.py`):

1. *Paint.* The scene is painted as one RGB colour per cell: sky gradient, ranges back to
   front from profiles (a crest row per column, in half-rows), the mist's alpha, the lake,
   the shore. This is where composition and light live, in plain numbers (the colours of
   snow, rock, forest, haze, mist, water are named constants).
2. *Halftone.* Every cell's colour becomes the nearest mix the console can show: a glyph
   from ` ░ ▒ █` in a foreground slot over one of four background slots (black and the three
   sky blues), chosen from a curated list of mixes with an 8x8 Bayer ordered dither (amplitude
   7 in RGB, 2.5 in the quiet zone) and a small penalty on grainy pairs. Solid █ is allowed
   only for the snow and rock tones, so a gradation is always made inside the cell with ░ ▒
   and never by a checker of whole cells (the first render did that, and it looked like
   bricks).
3. *Ink.* Structural strokes over the halftone, each keeping the background slot of the cell
   it lands on: the crest lines (`/` `\` for steep, `'` `.` `_` `-` for gentle by where the
   crest crosses the cell, top or bottom half; `^` on a summit), white where snowed and lit,
   soft white in shade, grey where rock, haze-coloured for the far range; gullies and
   hatching on the faces (`\` down a right-falling flank, `/` down a left-falling one, denser
   with depth and on the shade side, grey on snow, black on rock); `^` tree tops along the
   hills' crests and sparsely at the range's feet; the pines (fixed drawings); tufts on the
   shore; a few `-` ripples.

Why this and not the alternatives: a pure density ramp (` .:-=+*#%@`) on black is the
"screensaver ASCII" look, grey and busy, and it would put dense glyphs behind the tree; a pure
pixel picture (half blocks) needs the font switch, drops the drawn quality his image 1 has, and
its 2-pixel cells make the tree's thin strokes look thinner by contrast; solid colour fills
(bg only) are flat paint. Painting first gives real light and distance (the physics above)
cheaply; the halftone keeps the picture smooth and the colour count small; the ink gives it
the hand of ASCII art, the hatching of image 1 and Sesshū's one-stroke crests. It also keeps
the tree legible: tone sits in low-contrast ░ ▒ mixes, strokes are sparse, and the zone behind
the tree is nearly empty.

**Font.** Not needed. Uni2-Fixed has ░ ▒ █ and every ASCII stroke used. (If he later wants
smoother crests, a round could add ▀ ▄ on the crest cells with the Terminus font; I would
first see the ridge strokes on the real screen, since a drawn `/` line is the look we want.)

## The palette (16 slots, exact RGB), by day

| slot | RGB | letter | used by |
|---|---|---|---|
| 0 | #000000 | k | the console; the table; pines, forest, deepest shade; **bg** |
| 1 | #8a3324 | | rosewood stand, Teizan clay (planter only) |
| 2 | #2f8f3e | | leaves shaded (tree only) |
| 3 | #784c20 | | trunk, branches, Teizan trim (unchanged) |
| 4 | #2c5c9e | B | deep sky, the zenith; **bg**; the oval pot's glaze |
| 5 | #5b8ec8 | b | mid sky; **bg**; the lake near the viewer (as ░ ▒ on p) |
| 6 | #a8c4db | p | pale sky at the horizon, mist, the far lake; **bg**; the celadon pot |
| 7 | #d5dbe0 | g | soft white: cloud bodies, snow in shade, gravel |
| 8 | #7b8b9b | d | grey-blue: cloud bases, far clouds, rock, the tree's shadow |
| 9 | #e0452b | | autumn red leaves (tree only) |
| 10 | #52c95a | | leaves lit, buds (tree only) |
| 11 | #f2d33c | | growing tip, autumn yellow leaves (tree only) |
| 12 | #4a7ab3 | i | steel blue: shadowed snow, the water's depth; the oval pot's highlight |
| 13 | #8ea7c3 | h | haze: the far range; this is the free "bright magenta" slot |
| 14 | #c6d8e7 | c | ice: bright mist, snow in shade; the celadon pot's highlight |
| 15 | #f6f8fa | W | bright white: cloud tops, sunlit snow |

The tree keeps its slots; 2 and 10 are tuned a touch darker and more saturated than the
console's defaults so lit leaves hold against pale water (the lake is #a8c4db; shaded leaves
#2f8f3e and the trunk #784c20 are dark on it; lit leaves #52c95a differ from it in hue, as the
red and yellow autumn leaves do). The planter sits on black as before. The pots change hue
only: cobalt oval, pale-blue celadon.

**Backgrounds: only slots 0, 4, 5, 6** (k B b p). Every other slot is foreground only. This is
what keeps the colour pairs inside curses' 64: the backdrop at 135x120 uses 23 pairs (listed
by `stats`); the tree's 9 foreground colours (1 2 3 7 8 9 10 11 15) on the four backgrounds
are 36, of which W g d on each background are already the backdrop's: 59 in all, under 63.
The programmer allocates pairs on demand from a (fg, bg) -> pair table.

**Fallback** when the palette cannot be set (`curses.can_change_color()` false, a generic
terminal): remap letters b -> B, h -> d, i -> B, c -> p for foregrounds, and the background
b -> B. The sky is then blue to cyan to white on a standard palette: crude but readable, and
`sky = no` turns it all off. With `can_change_color()` true (the Linux console, xterm), the
sixteen `init_color` calls above are the whole set-up.

## The sky

Three stops, a gradient by row share v: #2c5c9e at 0, #5b8ec8 at 0.17, #a8c4db at 0.34 and
beyond (the horizon is hidden by the mist, so the palest sky meets the mountains' feet). The
halftone makes it: solid B, then ░ b on B, ▒ b on B, ░ B on b, solid b, ░ p on b, ▒ p on b,
░ b on p, solid p, nine steps dithered into each other with the Bayer pattern, so on his
screen it is a dotted gradation like the halftone of his image 1 and like the *bokashi* of a
print. The deep band is 7 rows, the mid band 13, then pale behind the peaks.

**The clouds on it.** The three greys keep their roles: W bright white (tops), g soft white
(bodies), d grey-blue (bases, far clouds, mist). On the deep and mid sky every grey is lighter
than the sky (cirrus live there, rows 2-19, and real cirrus are white); over the pale sky and
mist the bases are darker than the sky, as cumulus bases are. A cloud cell is drawn as
(cloud char, cloud fg, **the backdrop's bg at that cell**). Cumulus rows (0.10-0.46 H = 12-55)
cross the peaks; a lenticular over a summit is exactly where lenticulars form. One change I
recommend with the blue sky: fill a cumulus' interior (the spaces between its first and last
painted cell on each row) with `░` in g, and the top row's interior with `▒` in W, so a cloud
passing a rock face veils it instead of showing it through a wire outline. Cirrus and the mist
band stay as they are (strands). The dynamic mist band (0.52-0.78 H) now drifts over the
lake: d-grey `~` on pale water, right.

## Generation: procedural, seeded, once per run

The backdrop is built once at start from the run's seed (or a fresh one) and stays for every
tree: it is the place the tree lives, and a view does not change between trees. What the seed
draws: the light (left or right), which side the main summit is on and where (0.33-0.39 or
0.61-0.67 of the width), the second summit across the centre, the shoulder, 3-5 lesser
summits and their widths, the far range's 4-6 crests, the hills' crests and knolls, the
snowline (0.42-0.58), the snow's patches, the gullies, the forest line, the five spears,
the pines' sides and cuts, the ripples. What is fixed: the bands' shares, the centre band,
the colours, the pine drawings. No two runs are the same mountain; every run is this
composition. Deterministic for a seed, so renders are repeatable.

**The ranges** (`profiles()`): each range is the upper envelope of peaks, each peak
`base - h * (1 - d/width)^k` with k > 1 (steep near the summit, a wide foot), asymmetric
widths, roughened with 3-octave value noise scaled to the local height, and clamped to one row
per column so every crest cell is a `/` or `\` at most (no vertical spikes). The main range's
base is under the mist; the far range's 6 half-rows lower (so it is only ever seen through the
saddles); the hills' 4 lower, with higher roughness (a wooded line).

**Light and snow** (`paint()`): a column's face is lit when its crest falls away from the
light (left flank lit with light from the left); blended across 4 columns at summits and
saddles. Snow by altitude (0 at the mist, 1 at the summit) around the snowline with 2D noise
for patches, shed on steep faces, wind-packed patches a shade darker even where lit;
lit snow #f4f6f8, shaded snow #b9cadb (sky-lit, blue), lit rock #93a0ad, shaded rock #4d5864,
gullies #343c46 running down the flank away from the crest (a 1D noise along the fall line,
stronger with depth and in shade), forest #2a3542 below 0.26 of the height outside the
centre. The far range is haze #7390b2 fading to the pale sky toward its feet; the hills
#27323f with a lighter uneven canopy, sinking into the mist from 4 rows under the crest.

**The mist** (`spears()`): the core band at 0.35-0.45 H, alpha 0.55 rising to 0.95 over its
first 3 rows (a soft top), colour #cfdbe6; above it five spears, straight-edged rectangles
whose ends taper over 3 cells, alpha 0.5-0.85, two in the centre band rising to 0.25 H, three
elsewhere rising less; plus a thin general haze in the 4 rows over the core.

**The lake**: #a8c4db by the far shore to #86a9d0 at the near shore (the deepening starts at
0.45 of its height); reflections only of the hills, only at the sides, 40 % fading over 14
rows. **The shore**: #141c24 with a #2a3a4a top edge, tufts. **The pines**: three fixed
drawings (36, 22 and 10 rows; a 3-row one for ridges, unused in round 1), solid black `█`
bodies with `/` `\` edges and `|` `^` tips, in the sky_shapes form (`python3
landscape_shapes.py shapes` prints them with their paint rows); shorter screens sample their
rows evenly.

## Time of day (a proposal for round 2, not built into round 1)

The cells never change; only the sixteen RGB values do, at a tree boundary, from the clock:
day as above; evening (16-19 h): sky 4 #2f4f86, 5 #6a85b5, horizon 6 #c9bcb4, soft white 7
#dccfc8, grey 8 #767a8e, steel 12 #4e6a9a, haze 13 #a0919f, ice 14 #e3c9c2, snow 15 #f9e4d4
(alpenglow; the lake takes the warm horizon); night (19-6 h): 4 #0b1a33, 5 #15294d, 6
#2c4468, 7 #8e9ab0, 8 #4b5a70, 12 #1d3a62, 13 #3d5478, 14 #6f88a8, 15 #c9d6ea (moonlit
snow over a dark lake; the tree's greens read on it as they do on black now). `landrev/
s1_evening.png` and `s1_night.png` show both as pure swaps. The tree's own slots never
move. Dawn would be the evening set with the blues of morning; I would tune it on the
screen. Cost to the programmer: a table and one `init_color` loop per tree.

## Notes for the programmer

- `backdrop(W, H, seed)` returns rows of `(char, fg_letter, bg_letter)`; `LETTERS` maps
  letters to slots, `FALLBACK` the remap. Build it once in `screensaver()` after `getmaxyx`,
  and again on resize. Keep it as the bottom layer: `restore()` falls back to it (never to
  blank), the Sky's `put` uses its bg at the cell, `redraw` after `clear_softly()` repaints it
  first (row by row, so the clearing stays a wipe).
- Every tree cell, leaf, dust grain and planter cell is drawn with its own fg on **the
  backdrop's bg at that cell**; a (fg, bg) -> pair table allocated on demand, 63 pairs at
  most, the four backgrounds only. The planter and carpet sit on rows whose bg is black, as
  now.
- Cell counts at 135x120: 3601 open sky, 1230 main range, 136 far range, 138 hills, 2185
  mist, 5670 lake, 945 shore, 2295 table (`stats`).
- Generation takes about a second at 135x120 in pure Python (the halftone tries ~50 mixes per
  cell); fine once per run; cache by (W, H, seed) if a resize loop appears.
- A setting: `landscape = auto` (auto = with `sky = yes` when colours can be set; yes; no).
  With `landscape = no` the clouds keep the black sky they have now.
- I kept the dynamic mist band's rows (0.52-0.78 H) and all cloud rows unchanged.

## What I want to see in the first renders

1. Portrait 135x120, seeds 1 and 3, a finished moyogi and a bunjin on the backdrop, with the
   planter: does the crown read on the pale lake, the bunjin's tip on the mist, the trunk on
   the water; are the autumn leaves (yellow, red) visible as they fall across the mist and
   lake; does the carpet on the black table still look right.
2. The same frame with three cumulus and a cirrus on the sky: the outlines on the dotted
   gradient, a cumulus crossing the main peak (with and without the interior fill), the
   d-grey mist `~` over the lake.
3. The real console: the true ░ ▒ glyphs of Uni2-Fixed against my PNG emulation (the dot
   patterns decide how smooth the sky looks), the sixteen RGB values as the monitor shows
   them (is the deep blue too dark, the lake too bright at night), and whether the shade
   faces (black ▒ on deep blue) read as shadow or as "too blue".
4. 200x55 and 80x24 with a tree, to confirm the degradation is acceptable.
5. The evening and night swaps once, to decide whether round 2 builds the clock.

## References (for docs/references.md)

### The landscape

- ASCII mountains, asciiart.eu (Joan Stark's peaks with `^` snow and `=~-` water; hatched
  faces `W I i ; : .`; `^` forests; `#` snow over `.:;iIlT` foothills).
  https://www.asciiart.eu/nature/mountains
- ASCII mountains and landscapes, ascii.co.uk. https://ascii.co.uk/art/mountain and
  https://ascii.co.uk/art/landscape
- Joan Stark's tutorial: the slope ramp `_,.-'"^`, characters by their height in the cell.
  https://ludd.ltu.se/~vk/pics/ascii/junkyard/techstuff/tutorials/Joan_Stark.html
- Hayley Wakenshaw's tutorial: diagonals and gradual slopes.
  https://ludd.ltu.se/~vk/pics/ascii/junkyard/techstuff/tutorials/Hayley_Wakenshaw.html
- Xu, Zhang, Wong, "Structure-based ASCII Art", ACM TOG 29(4), SIGGRAPH 2010: tone-based vs
  structure-based ASCII art. https://history.siggraph.org/?p=105594
- Paul Bourke, character representation of grey-scale images: the ` .:-=+*#%@` and 70-step
  ramps, sampling at the cell's aspect. https://paulbourke.net/dataformats/asciiart/
- Ordered (Bayer) dithering, the 2x2, 4x4, 8x8 matrices and threshold rule.
  https://en.wikipedia.org/wiki/Ordered_dithering
- Floyd-Steinberg error diffusion. https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
- libcaca's study of dithering for text mode.
  https://gitea.zoy.org/cacalabs/web/src/branch/master/www/study/part3.html
- Semigraphics and block art: half-block pixels, teletext's 2x3 mosaics, PETSCII.
  https://en.wikipedia.org/wiki/Semigraphics and https://en.wikipedia.org/wiki/Block_art
- ANSI art: 16 foreground and 8 background colours, iCE colours.
  https://battleofthebits.com/lyceum/View/ansi+%28format%29
- The three distances (san'en) of Guo Xi; the six distances with mist.
  https://projects.mcah.columbia.edu/jaanus/record/sanen and
  https://projects.mcah.columbia.edu/jaanus/node/1715
- Kasumi and suyari-gasumi (spear mist): bands, the rounded head, dividing near from far.
  https://projects.mcah.columbia.edu/jaanus/record/kasumi
- Yohaku, the blank space that weighs as much as the painted.
  https://projects.mcah.columbia.edu/jaanus/record/yohaku
- Sesshū: one strong stroke for the cliffs, far peaks drawn on the grey sky with one line,
  mist wash dividing solid from void. https://en.wikipedia.org/wiki/Sessh%C5%AB
- Hasegawa Tōhaku, Pine Trees: near pines dark, far ones pale, blank paper as mist.
  https://en.wikipedia.org/wiki/Sh%C5%8Drin-zu_by%C5%8Dbu
- Hokusai, Fine Wind, Clear Morning: the sky in three deepening blues, snow at the summit,
  the dark forest at the foot. https://en.wikipedia.org/wiki/Fine_Wind,_Clear_Morning
- Aizuri-e, the all-blue prints of the 1830s. https://en.wikipedia.org/wiki/Aizuri-e
- Aerial perspective: contrast, saturation and detail fall with distance, hue goes to the
  sky's blue. https://en.wikipedia.org/wiki/Aerial_perspective
- The sky's blue and its paling toward the horizon (Rayleigh and Mie scattering).
  https://en.wikipedia.org/wiki/Diffuse_sky_radiation
- Texture strokes of Chinese landscape painting (hemp-fibre for gentle slopes, axe-cut for
  hard rock), Way and Shih 2001. https://diglib.eg.org/handle/10.2312/8856
