# The design log

What each round decided, in the owner's words where he gave them, newest first. Kept from
the tree-variations round on; the earlier rounds are written back from the session.

## 2026-10-21 — foliage, bark, deadwood and five forms

- The ask: "add variations on the foliage collection as well as the trunk/branches
  variations. I just want to add more now that the platform is set-up." And: keep design
  notes if they help the next round be "more precise/easier/fluid"; the gallery already
  catalogues the assets, so only what the catalogue does not hold (this folder's
  `BRIEF.md` and this log).
- Built from the reviewer's `tree_variations.md`: eight foliage styles, five barks,
  deadwood (shari, jins, the top jin), the windswept, broom, clump, exposed-root and
  semi-cascade forms, with settings `foliage`, `foliages`, `bark`, `barks`, `deadwood` and
  the five forms in `styles`.
- Changed from the note, for the standing rulings: no per-form pots (the planter is the
  run's wide tray); deadwood in slot 13, the clouds' white, since slot 7 is #252521 on
  screen; the semi-cascade planted a dozen columns from the rim in a wide tray.
- Round 3, the reviewer's numbers after the renders (section 11 of `tree_variations.md`):
  the elm thicker, the juniper narrower, the willow's curtains shorter and its cap wider,
  the tuft less holed, fewer blooms and fruit, plates four wide and three tall, the twist
  only on rows four wide or more, the hollow by the stroke's own height, the shari with
  its own texture, the windswept with real branches (18 to 30 columns) and bigger pads at
  a 30-degree lean, the broom's crown higher and softer, the clump without its giant cap,
  the rock in the deadwood's grey with the legs bowing outward, the semi-cascade with a
  rise of 18 to 24 rows and a two-row run. Everything else left as rendered.

## 2026-10-20 — the clouds' amount

- "Can I get more of the clouds that are high up on the screen? The ones around the tops
  of the mountains that go kind of behind the mountain and in front of it? And can you
  create a variable for the amount of clouds?" Settings `clouds_far`, `clouds_mid`,
  `clouds_near`; his laptop runs `clouds_far = 3`.

## 2026-10-20 — the grey square

- "There's a square of blank area in the middle ... between the black trees on either
  side, there's no design in there, it's just grey." The lake and mist had flattened into
  one slab when the whole palette was dimmed to 1 % light. Fixed by splitting design from
  display: the halftone is computed on the full-light design, then every slot is shaded
  for display (`LANDSCAPE_L`, `LANDSCAPE_CHROMA`, `CLOUD_L`). "The rest of the background
  looks amazing, and I don't want to mess that up."

## 2026-10-19 — the tonal clouds

- "Cranking the brightness and contrast on the clouds might make them pop a bit ... have
  the designer put some options together." Then: "make them match the realism of the
  background"; "there should be some off in the background near the mountains, going
  behind and in front, then more prominent ones closer up. The ones there now look like
  they're from a Mario cartoon"; "don't delete them from the asset list, I just want more
  realism for this one, all the assets should be retained." The tonal set at three depths
  with occlusion behind the summits, beside the ink set. Brightness: "reduce the brightness
  of them to like 15 %" then "much better, go for 8 %" (`CLOUD_L` 0.41).

## 2026-10-19 — the landscape's light

- "Make the background less vibrant." "There's so much contrast everywhere." "Can you
  make it 20 %." "Try 3 %." "That's not 3 %, it's still so bright" (light, not chroma: the
  chroma had been cut first). "Much better, try 1 %." "Perfect." The landscape at
  lightness 0.26.

## 2026-10-19 — the tree over the landscape

- "I love the background. The tree/pot will need some modifications to be more bold ...
  send that to the designer with the background as reference to make the tree more
  prominent." The trunk's inside on black, pads with a lit cap and a dark underside,
  filled planters, the one-cell halo of plain ground (`tree_prominence.md`).

## 2026-10-18 — the landscape

- Two reference photographs of mountains. "The sky behind the clouds can be blue, but
  design it to look like a sky, not just a solid blue background. The designer should look
  up ASCII art examples ... I want this to look as beautiful and realistic as possible,
  it's the only thing running on the laptop so resources aren't an issue." The paint,
  halftone, ink landscape (`landscape_design.md`, `landscape_shapes.py`).
- "Can the trunk be more dark brown": the console's slot 3 set to brown.

## 2026-10-18 — the sky

- "Add some more scenery in the background ... sky and clouds ... have a designer look up
  references and then design them ... they can float around just like clouds ... different
  kinds of clouds ... something elegant, creative, beautiful." The ink set: real cloud
  kinds at real heights, one wind, a mood per tree (`sky_design.md`).
