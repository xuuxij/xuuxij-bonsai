#!/usr/bin/env python3
"""Render every form and every planter in the console's colours and build the gallery page.

    python3 gallery.py OUT.html [PROGRAM=..] [CONFIG=..]
"""

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
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bonsai Forms and Planters</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@500;700&family=IBM+Plex+Mono:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap">
<style>{STYLE}</style></head><body><main>
<h1>Bonsai Forms and Planters</h1>
<p class="lede">Every form and every planter the screensaver can draw, rendered off-screen at the console's size (135 columns by 120 rows) in the colours the console shows. Each form is shown with the planter it drew; each planter is shown under the same informal upright.</p>
<p class="key"><span style="color:#ffff55">trunk and branches</span><span style="color:#55ff55">leaves, lit</span><span style="color:#00aa00">leaves, shaded</span><span style="color:#aaaaaa">gravel</span><span style="color:#555555">shadow</span></p>
<h2>Forms</h2><section class="grid">{"".join(forms)}</section>
<h2>Planters</h2><section class="grid">{"".join(planters)}</section>
</main></body></html>
"""
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("wrote", out)


if __name__ == "__main__":
    main()
