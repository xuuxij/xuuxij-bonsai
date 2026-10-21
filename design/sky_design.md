# The sky behind the bonsai: clouds, round 1 (design, read-only)

## Recommendation in one breath

Real cloud kinds, drawn the sumi-e way: an ink outline with a lit top, an empty interior, three greys on the black (which is paper, not night), mostly empty sky. One Japanese quotation only: the low mist band (suyari-gasumi) that forms behind the trunk now and then. Not a stylised gold-cloud sky: shown below, and why not.

## What the research gives us

**Real clouds, from the ground.** Low (below ~2 km): cumulus, white domed tops over flat grey bases; stratocumulus, a lumpy grey layer in rolls; stratus/fog, a featureless veil near the ground. Middle (2–7 km): altocumulus, small rounded clumps in rows (mackerel sky); lenticular, a smooth lens that sits still over hills while everything else moves. High (5–12 km): cirrus, wispy translucent streaks with a hooked head and trailing tail (mare's tails); cirrostratus, a thin sheet. Cumulonimbus: a dark tower with an anvil. Apparent motion is wind over distance: cirrus ride the fastest wind yet look nearly still; low cumulus visibly drift. Hence the parallax on screen: cirrus slowest, cumulus fastest, mist still.

**ASCII clouds** that work use parentheses, `.-~-.` arcs, underscores for flat bases and `~ - . , '` for wisps; filled blocks and letters look like blobs.

**Japanese painting.** Kasumi (mist) runs in flat horizontal bands behind the subject; from the 13th century the bands get straight edges and rounded heads (suyari-gasumi, "spear mist"), later gold leaf. The bands divide depth, hide what need not be shown and mark time passing; in Hiroshige's Genji prints the scenes "fade in and out" through them, with metal dots imitating cut gold leaf (kirihaku). Sumi-e makes mist from blank paper and dilute ink. That is where "elegant" lives: restraint, emptiness (ma), a band behind the subject, not clouds all over it.

## Palette and grammar

Three greys only: `W` bold white (lit tops, never more than a fifth of a cloud), `g` plain white (bodies), `d` bold black (bases, far clouds, mist, births and deaths). No colour. Interiors stay black. Every cloud below gives its text rows and a paint map of the same size (space = nothing drawn). Cells are twice as tall as wide, so a 22-column, 3-row cloud reads about 3.5:1, right for a fair-weather cumulus. A mirror of any shape is a second variant: swap `(` `)`, `'` `` ` ``.

## The kinds

**Cumulus** (the everyday cloud): three sizes, each with an A and B form; a cloud "breathes" by stepping A→B→A every 25–45 s (one hump grows).

```
cumulus small A                 cumulus small B
  .-~~-.      ggWWgg             .-~.-~~-.      ggWggWWgg
 (______)     gddddddg          (_________)    gdddddddddg

cumulus medium A                              cumulus medium B
        .-~~~-.._                ggWWWgggg           .-~~-.   .-~-.          ggWWgg   ggWgg
   .--~'         '-.          gggWg         ggg    .-'      '-'     '-.    ggg      ggg     ggg
  (_________________)        gdddddddddddddddddg   (___________________)   gdddddddddddddddddddg

cumulus large A
             .-~~-.                             ggWWgg
       .-~~-(      )-~~-.                 ggWWgg      ggWWgg
   .-~'                  '~-..__        gggg                  ggggggg
  (______________________________)     gddddddddddddddddddddddddddddddg

cumulus large B
                  .-~~~-.                             ggWWWgg
       .--~~-.  .'       '-.               gggWWgg  gg       ggg
   .-~'       ''            '~-.         gggg       gg            gggg
  (______________________________)     gddddddddddddddddddddddddddddddg
```

**Cirrus** (mare's tails): the head leads downwind, the tails trail; mirrored for the other wind.

```
cirrus small     ,.-~~~~~--..__          gggWWWWWggdddd

cirrus medium    ,.-~~~~~~~~~~~--..__    gggWWWWWWWWWWWggdddd
                   '~~~~~~--.._            gggggggggddd
                      `~--.                   ddddd

cirrus large     ,.-~~~~~~~~~~~~~~~~~--..___    gggWWWWWWWWWWWWWWWWWggddddd
                   '~~~~~~~~~~~--..__             ggggggggggggggdddd
                     `~~~~--.._                     dddddddddd
                        `-.                            ddd
```

**Altocumulus, mackerel sky** (rare): scales `.-.` over `'-'` on a lattice 5 columns apart, rows staggered by half a unit, 30 % of units left out, the field's outline a wedge, never a rectangle. 40–70 columns wide, 2–4 rows. One sample:

```
  .-.  .-.       .-.  .-.  .-.           ggg  ggg       ggg  ggg  ggg
  '-'  '-'  .-.  '-'  '-'  '-'  .-.      ddd  ddd  ggg  ddd  ddd  ddd  ggg
       .-.  '-'       .-.       '-'           ggg  ddd       ggg       ddd
       '-'            '-'                     ddd            ddd
```

**Lenticular** (rare, still): smooth, bright, a standing wave while the cumulus drift past it.

```
        _..--~~~~~~~~~--.._              gggggWWWWWWWWWggggg
   _.-~'                   '~-._      gggWg                   gWggg
  '--..___________________..--'       gggggdddddddddddddddddddggggg
```

**Stratocumulus roll** (occasional): a long lumpy band, grey only, no bold white; 36–60 columns.

```
 _.-~~-.__.-~~~-.._.-~~-.__.-~~~~-._.-~-._     ggggggggggggggggggggggggggggggggggggggggg
(_________________________________________)    gdddddddddddddddddddddddddddddddddddddddddg
```

**Mist band, kasumi** (the one stylised piece): 2 or 3 straight rows of dark-grey `~` with a `-` every 5–9 cells, each row a different length and offset so the ends step like spear mist; density 85 % in the middle thinning to 20 % over the last 8 columns of each row (the rounded head); one cell in 14 a plain-grey `'` or `.` (the kirihaku dots). 50 columns to the full width. It sits behind the trunk and lower pads and shows only in the gaps. One sample, 70 wide (paint: all `d`, the `'` and `.` `g`):

```
            ~ ~~-~~~~-~~~~~~~-~~~~~~~~~~-~~~~~~~~~~~-~~~~~~-~~~ ~
   ~ ~~-~~~~~~~~~~-~~~~~~~~~~~~~~'~~~~~~~~~~~~-~~~~~~~~~~~~~~-~~ ~  ~
        ~ ~~~-~~~~~~~~~-~~~~~~~~~~~~~~-~~~~~~~~~~.~~~~-~~~ ~~ ~
```

## Their life (rows as shares of the height, 0 = top; speeds for 135 columns, scale by W/135)

| kind | rows | columns/s | born | dies | lives | at once | how often |
|---|---|---|---|---|---|---|---|
| cirrus | 0.02–0.16 | 0.08 | fades in in place (d → g → W over 40 s) | fades out, tail first, 40 s | 3–6 min | ≤2 | 1–2 per tree |
| mackerel field | 0.06–0.22 | 0.12 | fades in, scattered order, 60 s | fades out 60 s | 4–6 min | 1 | 1 tree in 8 |
| lenticular | 0.14–0.26 | 0 | fades in 30 s | fades out 30 s | 3–5 min | 1 | 1 tree in 12 |
| cumulus small | 0.10–0.32 | 0.30 | drifts in from the upwind edge (60 %) or forms in place from a 1-row `.-~-.` growing to small over 50 s (40 %) | drifts out, or dissolves in place (edges first, 40 s) | crossing | ≤3 all sizes | fair: one every 90–150 s; clear: 0–1 per tree |
| cumulus medium | 0.18–0.40 | 0.40 | same | same | crossing | | |
| cumulus large | 0.24–0.46 | 0.50 | from the edge only | drifts out | crossing (~6 min) | | |
| stratocumulus roll | 0.30–0.48 | 0.45 | from the edge | drifts out | crossing | 1 | replaces a cumulus 1 time in 5 |
| mist band | 0.52–0.78 | 0 | forms in place over 40 s | dissolves over 40 s | 2–4 min | 1 | misty tree: 1–2; any tree: 1 in 10 |

Bigger is lower and faster (nearer); smaller is higher and slower. Nothing ever moves vertically. All kinds share one wind direction, drawn once per run and flipped (1 chance in 5) only at a tree boundary when the sky is empty.

**Moods.** Each tree draws a sky with its random generator (so a seed repeats it): clear 35 % (0–1 cumulus, a cirrus or two, often nothing for minutes), fair 40 % (1–3 cumulus about, a cirrus), high 12 % (mackerel or two long cirrus, no cumulus), misty 13 % (a mist band, at most one cumulus). The sky is never reset between trees; clouds on screen carry over. At program start, run the sky five minutes forward silently so the first tree is not born under an empty sky.

**Rhythm.** Fast clouds step one column every 2 s; outside the drift, at most one cell of any cloud changes per 10 s (a breath, a fade step). No cell flickers.

**The breeze.** The leaves' sway is a ground breeze with no mean; the clouds' wind is theirs. One tie, cheap and true: the fall's gusts are drawn 2:1 in the clouds' direction, so the world has a prevailing wind. Optional seasonal tie: during the bare hold and the crumble, the mist band's odds triple (a bare tree in mist).

**Rare kinds:** lenticular, mackerel sky, the stratocumulus roll, the large cumulus (1 in 4 cumulus). **Not drawn:** cumulonimbus (a storm makes the sky the subject), cirrostratus (a full-sky veil is just a greyer screen), fog on the ground (it would sit on the planter), sun, moon, stars, birds, rain.

## The stylised alternative, shown and declined

A kumogata band (scalloped auspicious cloud, zuiun), outline in grey:

```
      .-.   .--.   .-.
   .-'   '-'    '-'   '-.______
  (                            )
   '--.___.---.____.----.____.'
```

As the whole sky it is wallpaper: it does not move like weather, its real force is opaque gold, and bold yellow is the trunk's colour, so a gold band behind a yellow trunk swallows the tree. Keep the tradition where it belongs: the mist band, low, behind the trunk, now and then.

## What not to do

Filled blocks (`#`, `@`, `%`, `O`, letters) or `*`/`&` (those are leaves); any colour in the sky; bold on bodies; filled interiors; more than 5 clouds, or a sky empty less than a third of the time; clouds under 8 columns (debris); symmetric shapes or two identical clouds at once; vertical motion, bouncing, wrap-around (a cloud leaving right never reappears left); two clouds on the same rows closer than 8 columns (born elsewhere instead); any cloud over the planter, stand or table (below 0.80 of the height only the mist, 6 rows above the rim); per-frame flicker; a sky that reacts to every gust.

## Notes for the programmer (from the code)

`grid` holds only the tree, pot and carpet; `restore()` blanks a cell `grid` lacks, so it must fall back to the sky layer or every falling leaf and dust grain punches holes in the clouds. The sky needs its own tick (0.25 s is plenty) inside `pause()`/`sleep_until()`, and a redraw after `clear_softly()` and a resize. Cloud cells never enter `grid`, so leaves land through mist unchanged.

## Sources

- Cloud genera, heights, appearance: https://en.wikipedia.org/wiki/List_of_cloud_types ; NWS cloud chart https://www.weather.gov/media/arh/brochures/CloudChart.pdf ; cirrus look still yet move fastest https://en.wikipedia.org/wiki/Cirrus_cloud ; jet stream speeds https://en.wikipedia.org/wiki/Jet_stream ; lenticular, anvil, mackerel https://www.metoffice.gov.uk/blog/2026/deep-dive-from-mountain-waves-to-mammatus and https://en.wikipedia.org/wiki/Altocumulus_cloud ; fog as grounded stratus https://cloudappreciationsociety.org/cloud-library/fog/ and https://en.wikipedia.org/wiki/Stratus_cloud
- ASCII clouds: https://www.asciiart.eu/nature/clouds
- Kasumi and suyari-gasumi: https://projects.mcah.columbia.edu/jaanus/record/kasumi ; cloud motifs (unmon, kumotori): https://projects.mcah.columbia.edu/jaanus/record/unmon ; Hiroshige's Genji mist bands and kirihaku dots: https://ukiyo-e.org/image/honolulu/5874 ; Rinpa gold clouds, Sōtatsu's Waves at Matsushima: https://asia.si.edu/object/F1906.231-232/ ; sky gradation (bokashi) in prints: https://projects.mcah.columbia.edu/jaanus/node/3857 ; clouds in Japanese art (Kersey lecture): https://www.uni-heidelberg.de/en/node/50078
