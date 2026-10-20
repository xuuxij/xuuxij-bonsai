#!/usr/bin/env python3
"""Render every form and every planter in the console's colours and build the gallery page.

    python3 gallery.py OUT.html [PROGRAM=..] [CONFIG=..]
"""

import curses
import html
import random
import sys

import common
from common import BOLD, Screen, colour_attrs, setup, virtual_clock

# The Linux console's palette: normal and bold.
CSS = {"black": ("#000000", "#555555"), "red": ("#aa0000", "#ff5555"), "green": ("#00aa00", "#55ff55"),
       "yellow": ("#aa5500", "#ffff55"), "blue": ("#0000aa", "#5555ff"), "magenta": ("#aa00aa", "#ff55ff"),
       "cyan": ("#00aaaa", "#55ffff"), "white": ("#aaaaaa", "#ffffff")}

FORMS = [
    ("Informal upright (moyogi)", "style = moyogi", "An S-curve trunk whose movements tighten toward the top; branches shortening as they climb; a back pad behind the trunk.", 3, {"style": "moyogi", "twin": "no"}),
    ("Twin trunk (sokan)", "style = moyogi, twin = yes", "An informal upright with a second, shorter trunk forking just above the soil; a fifth of the uprights.", 4, {"style": "moyogi", "twin": "yes"}),
    ("Formal upright (chokkan)", "style = chokkan", "A straight trunk, level branches rising gently at their ends.", 2, {"style": "chokkan"}),
    ("Slanting (shakan)", "style = shakan", "The trunk leans a column a row, bowing against the lean; branches level, parallel to the ground.", 5, {"style": "shakan"}),
    ("Literati (bunjin)", "style = bunjin", "Tall, slender, several reversals; branches only in the upper third; two or three small pads; the apex sometimes bare.", 1, {"style": "bunjin"}),
    ("Cascade (kengai)", "style = kengai", "A short rise with a crown, then the trunk arcs over the rim and falls beside a tall stand, pads hanging from it.", 1, {"style": "kengai"}),
]
PLANTERS = [
    ("Teizan rectangle", "pot = teizan", "Red clay, open lip, two bands, a carved gold key-fret, cloud feet. One of the two run planters.", {"pot": "teizan", "stand": "no"}),
    ("Teizan on a rosewood stand", "pot = teizan, stand = yes", "The same rectangle on a stand with a cusped openwork apron and scroll feet.", {"pot": "teizan", "stand": "yes"}),
    ("Glazed oval", "pot = oval", "Blue glaze, rolled lip, a wave scroll in relief, delicate feet. The other run planter.", {"pot": "oval", "stand": "no"}),
    ("Oval on a rosewood stand", "pot = oval, stand = yes", "", {"pot": "oval", "stand": "yes"}),
    ("Studded drum", "pot = drum", "White, nail-head stud bands, a foot ring.", {"pot": "drum", "stand": "no"}),
    ("Celadon", "pot = celadon", "Cyan, wavy rim, floral scroll and lotus-petal relief.", {"pot": "celadon", "stand": "no"}),
    ("Literati pot on the tall stand", "pot = bunjin", "Shallow, plain, a wavy rim; the tall stand is the ornament.", {"pot": "bunjin"}),
    ("Hexagon on the cascade stand", "style = kengai (its own planter)", "Blue glaze, gold diamond lattice, dark facets; as tall as it is wide; the cascade's own.", {"pot": "hexagon", "style": "kengai"}),
]
# The sky's clouds: (title, where it lives, note, pieces); a piece is (kind, size or seed, variant).
SKY = [
    ("Cumulus", "rows 10 to 46 %, 0.3 to 0.5 columns a second", "Small, medium and large, each with the second shape it breathes into every half minute: an ink outline, a lit top, an empty interior, a dark base. The nearest cloud, so the brightest; the large one always enters by the upwind edge.",
     [("cumulus", 0, 0), ("cumulus", 0, 1), ("cumulus", 1, 0), ("cumulus", 1, 1), ("cumulus", 2, 0), ("cumulus", 2, 1)]),
    ("Cirrus", "rows 2 to 16 %, 0.08 columns a second", "Small, medium and large, drawn for a wind blowing left: the hooked head leads and the strands trail behind it and droop, each lower one set further back. No bold white anywhere: the farthest cloud is the faintest. Mirrored for a wind blowing right.",
     [("cirrus", 0, 0), ("cirrus", 1, 0), ("cirrus", 2, 0)]),
    ("Mackerel sky", "rows 6 to 22 %, 0.12 columns a second", "Altocumulus: a brick lattice of small arcs, the top row lit, the outer rows shorter, one arc in five left out; a different field each time. A high sky's cloud.",
     [("mackerel", 1, 0), ("mackerel", 4, 0)]),
    ("Lenticular", "rows 14 to 26 %, still", "A standing lens that forms where it is and dissolves from its edges; one tree in twelve.",
     [("lenticular", 0, 0)]),
    ("Stratocumulus roll", "rows 30 to 48 %, 0.45 columns a second", "A long low roll of soft humps on one base, entering by the upwind edge; one cumulus in five is a roll, at most one per tree and one in the sky.",
     [("roll", 2, 0), ("roll", 5, 0)]),
    ("Spear mist (suyari-gasumi)", "rows 52 to 78 %, still", "The one stylised piece, from Japanese painting: short separate bands of dark ~ on adjacent rows, overlapping a third, the ends tapered to a dot, a rare ' of grey; forms behind the trunk and dissolves.",
     [("mist", 3, 0), ("mist", 8, 0)]),
]


def span(mod, chars, attr):
    text = html.escape("".join(chars))
    number = attr & 0xFF
    if attr == 0 or not text.strip() or not 10 <= number < 18:
        return text
    name = list(mod.COLORS)[number - 10]
    bold = bool(attr & BOLD)
    colour = CSS[name][1 if bold else 0]
    return f'<span style="color:{colour}{";font-weight:bold" if bold else ""}">{text}</span>'


def render(mod, base_cfg, seed, over):
    cfg = dict(base_cfg)
    for k, v in over.items():
        cfg[k] = mod.convert(k, str(v))
    clock, log = virtual_clock(mod)
    tree = mod.Tree(Screen(clock, log), cfg, random.Random(seed), colour_attrs(mod, cfg))
    tree.draw_pot()
    tree.draw()
    H, W = common.H, common.W
    cells = {}
    for _t, y, x, text, attr in sorted(log, key=lambda e: e[0]):
        for i, ch in enumerate(text):
            if 0 <= y < H and 0 <= x + i < W:
                cells[(y, x + i)] = (ch, attr)
    rows = [[cells.get((y, x), (" ", 0)) for x in range(W)] for y in range(H)]
    while rows and all(ch == " " for ch, _a in rows[0]):
        rows.pop(0)
    out = []
    for row in rows:
        line, run, run_attr = [], [], None
        for ch, attr in row:
            if attr != run_attr and run:
                line.append(span(mod, run, run_attr))
                run = []
            run_attr = attr
            run.append(ch)
        if run:
            line.append(span(mod, run, run_attr))
        out.append("".join(line).rstrip())
    return "\n".join(out), tree.report


def sky_shape(mod, kind, n, variant):
    """One cloud's text rows and paint rows: `n` is the size for the drawn shapes, the
    seed for the generated ones."""
    rng = random.Random(n)
    if kind == "cumulus":
        text = mod.CLOUD_SHAPES["cumulus"][n][1 + variant]
        return text, mod.paint_for(text, mod._heap)
    if kind == "cirrus":
        text = mod.CLOUD_SHAPES["cirrus"][n][1]
        return text, mod.paint_for(text, mod._cirrus)
    if kind == "lenticular":
        text = mod.CLOUD_SHAPES["lenticular"]
        return text, mod.paint_for(text, mod._heap)
    if kind == "mackerel":
        return mod.mackerel_field(rng)
    if kind == "roll":
        return mod.stratocumulus_roll(rng)
    return mod.mist_band(rng, 70)


def render_sky(mod, pieces):
    """The pieces one under another in the sky's three greys."""
    white, black = 10 + list(mod.COLORS).index("white"), 10 + list(mod.COLORS).index("black")
    tones = {"W": white | BOLD, "g": white, "d": black | BOLD}
    out = []
    for kind, n, variant in pieces:
        text, paint = sky_shape(mod, kind, n, variant)
        for row, prow in zip(text, paint):
            line, run, run_attr = [], [], None
            for ch, pt in zip(row, prow):
                attr = tones.get(pt, 0)
                if attr != run_attr and run:
                    line.append(span(mod, run, run_attr))
                    run = []
                run_attr = attr
                run.append(ch)
            if run:
                line.append(span(mod, run, run_attr))
            out.append("  " + "".join(line).rstrip())
        out.append("")
    return "\n".join(out).rstrip("\n")


def landscape_html(mod, seed, W=135, H=120):
    """The landscape of one seed as coloured text, every cell on its own background."""
    pairs = mod.Pairs(live=False)
    back = mod.Backdrop(W, H, seed, pairs)
    rgb = {slot: spec[0] for slot, spec in mod.PALETTE_DAY.items()}
    out = []
    for y in range(H):
        line, run, key = [], [], None
        for x in range(W):
            ch, attr = back.chars[y][x], back.attr[y][x]
            n = (attr & mod.A_COLOR_MASK) >> mod.PAIR_SHIFT
            fg, bg = pairs.of.get(n, (7, -1))
            if attr & curses.A_BOLD and fg < 8:
                fg += 8
            k = (fg, 0 if bg < 0 else bg)
            if k != key and run:
                line.append(cell_span(run, key, rgb))
                run = []
            key = k
            run.append(ch)
        if run:
            line.append(cell_span(run, key, rgb))
        out.append("".join(line))
    return "\n".join(out)


def cell_span(chars, key, rgb):
    fg, bg = key
    style = f"color:{rgb[fg]}" + (f";background:{rgb[bg]}" if bg else "")
    return f'<span style="{style}">{html.escape("".join(chars))}</span>'


def card(title, setting, note, body, facts):
    note_html = f'<p class="note">{html.escape(note)}</p>' if note else ""
    return (f'<article class="card"><header><h3>{html.escape(title)}</h3>'
            f'<code class="setting">{html.escape(setting)}</code></header>{note_html}'
            f'<div class="screen"><pre>{body}</pre></div><p class="facts">{html.escape(facts)}</p></article>')


STYLE = """
:root { --bg: #0b0b0d; --panel: #131316; --screen: #000; --fg: #d9d4c8; --muted: #8f8a7f; --rule: #2a2a2e; --accent: #c9a24a;
  --display: "Shippori Mincho", "Times New Roman", serif; --body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", "Cascadia Mono", Consolas, "DejaVu Sans Mono", monospace; color-scheme: dark; }
body { margin: 0; background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 16px; line-height: 1.5;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 32px 48px; }
main { max-width: 1760px; margin: 0 auto; }
h1 { font-family: var(--display); font-weight: 500; font-size: clamp(2rem, 4vw, 3rem); margin: 0 0 .25rem; text-wrap: balance; }
.lede { max-width: 62ch; color: var(--muted); margin: 0 0 2.5rem; }
h2 { font-family: var(--display); font-weight: 500; font-size: 1.6rem; margin: 2.5rem 0 1rem; padding-top: 1.5rem; border-top: 1px solid var(--rule); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 820px), 1fr)); gap: 24px; }
.card { background: var(--panel); border-radius: 6px; padding: 16px 16px 12px; min-width: 0; display: grid; gap: 10px; align-content: start; }
.card header { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 16px; }
h3 { font-family: var(--display); font-weight: 700; font-size: 1.25rem; margin: 0; }
.setting { font-family: var(--mono); font-size: .8rem; color: var(--accent); white-space: nowrap; }
.note { margin: 0; color: var(--muted); max-width: 70ch; }
.screen { background: var(--screen); border-radius: 4px; overflow-x: auto; padding: 8px 10px; }
.screen pre { margin: 0; font-family: var(--mono); font-size: 9.5px; line-height: 1.15; color: #aaa; white-space: pre; width: max-content; }
.screen pre span[style*="background"] { line-height: 1.15; padding: 1px 0; }
.facts { margin: 0; font-family: var(--mono); font-size: .78rem; color: var(--muted); }
.key { display: flex; flex-wrap: wrap; gap: 6px 18px; font-family: var(--mono); font-size: .8rem; color: var(--muted); margin: 0 0 1rem; }
"""


def main():
    mod, cfg, rest = setup(sys.argv[1:])
    out = rest[0] if rest else "gallery.html"
    forms = []
    for title, setting, note, seed, over in FORMS:
        body, report = render(mod, cfg, seed, over)
        forms.append(card(title, setting, note, body, f"planter here: {report.get('planter', '')}"))
        print("rendered", title)
    planters = []
    for title, setting, note, over in PLANTERS:
        body, report = render(mod, cfg, 3, dict({"style": "moyogi", "twin": "no"}, **over))
        planters.append(card(title, setting, note, body, report.get("planter", "")))
        print("rendered", title)
    sky = [card(title, "sky = yes", note, render_sky(mod, pieces), where) for title, where, note, pieces in SKY]
    land = [card(f"The landscape, seed {seed}", "landscape = auto",
                 "Snowy peaks with hatched shade faces, a far range in haze, wooded hills, the spear mist, the still lake, the framing pines, the black table; drawn once per run from the seed, in blues and greys only." if seed == 1 else "",
                 landscape_html(mod, seed), f"seed {seed}; the tree grows over the lake, the planter on the table")
            for seed in (1, 3)]
    for seed in (1, 3):
        print("rendered landscape", seed)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bonsai Forms and Planters</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@500;700&family=IBM+Plex+Mono:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap">
<style>{STYLE}</style></head><body><main>
<h1>Bonsai Forms and Planters</h1>
<p class="lede">Every form, every planter and every cloud the screensaver can draw, rendered off-screen at the console's size (135 columns by 120 rows) in the colours the console shows. Each form is shown with the planter it drew; each planter is shown under the same informal upright; each cloud at full strength.</p>
<p class="key"><span style="color:#ffff55">trunk and branches</span><span style="color:#55ff55">leaves, lit</span><span style="color:#00aa00">leaves, shaded</span><span style="color:#aaaaaa">gravel, cloud bodies</span><span style="color:#ffffff">cloud tops</span><span style="color:#555555">shadow, cloud bases and far clouds</span></p>
<h2>Forms</h2><section class="grid">{"".join(forms)}</section>
<h2>Planters</h2><section class="grid">{"".join(planters)}</section>
<h2>Sky</h2>
<p class="note">Clouds drift behind the tree, drawn only where nothing else is, in three greys on the black: real cloud kinds at their real heights (rows as a share of the screen, from the top), one wind for the whole run, a mood per tree (clear, fair, high or misty). Each enters by the upwind edge or forms in place and dissolves, tail first.</p>
<section class="grid">{"".join(sky)}</section>
<h2>Landscape</h2>
<p class="note">The mountain landscape behind the clouds: a blue print behind a coloured tree, painted in RGB, halftoned into ░ ▒ █ over four backgrounds, and inked with ASCII strokes. The console's sixteen colour slots are set to these exact colours where the terminal allows it.</p>
<section class="grid">{"".join(land)}</section>
</main></body></html>
"""
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("wrote", out)


if __name__ == "__main__":
    main()
