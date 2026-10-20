#!/usr/bin/env python3
"""Run the landscape, the sky and a few trees on the virtual clock and draw the screen
at chosen moments as PNG images in the palette's colours (needs Pillow), plus the text
of each frame; the way to review the whole scene without the console.

    python3 scene_review.py OUTDIR [SEED] [TREES] [key=value ...] [SIZE=COLSxROWS] [AT=t1,t2,...]

AT lists the seconds (from the first tree's start) at which to draw; default 170, 330,
420 and 560 of every tree. The PNG emulates ░ ▒ with dot and checker patterns; the
console's own glyphs differ in texture.
"""

import curses
import os
import random
import sys

import common
from common import Screen, setup, virtual_clock

BOLD = curses.A_BOLD


def main():
    argv = sys.argv[1:]
    at = None
    for item in list(argv):
        if item.startswith("AT="):
            at = [float(v) for v in item[3:].split(",")]
            argv.remove(item)
    mod, cfg, rest = setup(argv)
    outdir = rest[0]
    seed = int(rest[1]) if len(rest) > 1 else 1
    trees = int(rest[2]) if len(rest) > 2 else 1
    os.makedirs(outdir, exist_ok=True)
    H, W = common.H, common.W
    clock, log = virtual_clock(mod)
    scr = Screen(clock, log)
    attrs = mod.make_attrs(cfg, live=False)
    pairs = mod.PAIRS
    backdrop = mod.Backdrop(W, H, seed, pairs)
    backdrop.draw(scr)
    rng = random.Random(seed)
    sky = mod.Sky(scr, random.Random(f"sky {seed}"), attrs)
    sky.backdrop = backdrop
    t0 = clock[0]
    sky.new_tree(clock[0] - 300, cfg["cycle"], H - 1)
    for t in range(300, 0, -1):
        sky.tick(clock[0] - t, {}, draw=False)
    inherit, t_start = None, clock[0]
    notes = []
    for n in range(trees):
        tree = mod.Tree(scr, cfg, rng, attrs, inherit)
        tree.sky, tree.backdrop = sky, backdrop
        if inherit is None:
            tree.draw_pot()
        mod.run_tree(scr, cfg, tree, t_start)
        notes.append(f"tree {n + 1}: {tree.style}{' twin' if tree.twin else ''}, sky mood {sky.mood}, "
                     f"wind {'→' if sky.wind > 0 else '←'}, planter {tree.report.get('planter', '')}")
        t_start += cfg["cycle"] or (clock[0] - t_start)
        inherit = {"planter": tree.planter_spec(), "grid": tree.grid}
    cycle = cfg["cycle"] or 600
    times = at or [k * cycle + s for k in range(trees) for s in (170, 330, 420, 560)]
    log.sort(key=lambda e: e[0])
    cells = [[(" ", 0)] * W for _ in range(H)]
    i = 0
    for until in times:
        while i < len(log) and log[i][0] <= t0 + until:
            _t, y, x, text, attr = log[i]
            i += 1
            for k, ch in enumerate(text):
                if 0 <= y < H and 0 <= x + k < W:
                    cells[y][x + k] = (ch, attr)
        stem = os.path.join(outdir, f"{int(until):04d}")
        with open(stem + ".txt", "w", encoding="utf-8") as fh:
            fh.write("\n".join("".join(c for c, _a in row).rstrip() for row in cells) + "\n")
        draw_png(mod, pairs, cells, stem + ".png")
        print("drew", stem + ".png")
    with open(os.path.join(outdir, "scene.log"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(notes) + "\n")
    print("\n".join(notes))
    print(f"{len(pairs.table)} colour pairs used")


def slots(pairs, attr):
    """The foreground and background palette slots an attribute shows."""
    n = (attr & mod_mask()) >> mod_shift()
    fg, bg = pairs.of.get(n, (7, -1))
    if attr & BOLD and fg < 8:
        fg += 8
    return fg, (0 if bg < 0 else bg)


_MOD = {}


def mod_mask():
    return _MOD["mask"]


def mod_shift():
    return _MOD["shift"]


def draw_png(mod, pairs, cells, out):
    from PIL import Image, ImageDraw, ImageFont
    _MOD["mask"], _MOD["shift"] = mod.A_COLOR_MASK, mod.PAIR_SHIFT
    H, W = len(cells), len(cells[0])
    cw, ch = 8, 16
    img = Image.new("RGB", (W * cw, H * ch), (0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    rgb = {slot: mod.hex_rgb(spec[0]) for slot, spec in mod.PALETTE_DAY.items()}
    for y in range(H):
        for x in range(W):
            c, attr = cells[y][x]
            fg, bg = slots(pairs, attr)
            X, Y = x * cw, y * ch
            if bg:
                d.rectangle([X, Y, X + cw - 1, Y + ch - 1], fill=rgb[bg])
            if c == " ":
                continue
            f = rgb[fg]
            if c == "█":
                d.rectangle([X, Y, X + cw - 1, Y + ch - 1], fill=f)
            elif c in "░▒":
                for py in range(ch):
                    for px in range(cw):
                        if c == "▒" and (px + py) % 2 == 0:
                            d.point((X + px, Y + py), fill=f)
                        if c == "░" and px % 2 == 0 and py % 4 == (px // 2) % 2 * 2:
                            d.point((X + px, Y + py), fill=f)
            else:
                d.text((X, Y - 1), c, fill=f, font=font)
    img.save(out)


if __name__ == "__main__":
    main()
