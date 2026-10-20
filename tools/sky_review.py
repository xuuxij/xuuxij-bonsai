#!/usr/bin/env python3
"""Run the sky and a few trees on the virtual clock and write what the screen shows
at regular moments: a text frame, and a tone map where every cloud cell is its grey
(W bright, g plain, d dark) and everything else is '#', so the three greys can be
judged without a terminal.

    python3 sky_review.py OUTDIR [SEED] [TREES] [EVERY] [key=value ...] [SIZE=COLSxROWS]

Also writes OUTDIR/sky.log: every cloud born, what and where, and the mood of each
tree's sky.
"""

import os
import random
import sys

import common
from common import Screen, plain_attrs, setup, virtual_clock

SKY = {"W": 20, "g": 21, "d": 22}
TONES = {v: k for k, v in SKY.items()}


def frames(log, times):
    """The screen at each time in `times`: (chars, tones) per moment."""
    H, W = common.H, common.W
    chars = [[" "] * W for _ in range(H)]
    tones = [[" "] * W for _ in range(H)]
    out, i = [], 0
    log = sorted(log, key=lambda e: e[0])
    for until in times:
        while i < len(log) and log[i][0] <= until:
            _t, y, x, text, attr = log[i]
            i += 1
            for k, ch in enumerate(text):
                if 0 <= y < H and 0 <= x + k < W:
                    chars[y][x + k] = ch
                    tones[y][x + k] = " " if ch == " " else TONES.get(attr, "#")
        out.append(([row[:] for row in chars], [row[:] for row in tones]))
    return out


def main():
    mod, cfg, rest = setup(sys.argv[1:])
    outdir = rest[0]
    seed = int(rest[1]) if len(rest) > 1 else 1
    trees = int(rest[2]) if len(rest) > 2 else 2
    every = float(rest[3]) if len(rest) > 3 else 30.0
    os.makedirs(outdir, exist_ok=True)
    clock, log = virtual_clock(mod)
    scr = Screen(clock, log)
    attrs = plain_attrs(mod, cfg)
    attrs.update(SKY)
    rng = random.Random(seed)
    notes = []
    sky = mod.Sky(scr, random.Random(f"sky {seed}"), attrs)
    born = sky.birth

    def noted_birth(now, kind, size, **kw):
        before = len(sky.clouds)
        born(now, kind, size, **kw)
        if len(sky.clouds) > before:
            c = sky.clouds[-1]
            notes.append(f"{now - t0:7.1f}s  {c.kind:<10} size {size if size is not None else '-'} "
                         f"at row {c.y}, col {int(c.x)}, {c.width} wide, {c.ends}, "
                         f"{abs(c.speed):.2f} cols/s {'→' if c.speed > 0 else '←' if c.speed < 0 else ''}"
                         + ("  (the empty-sky floor)" if kw else ""))
        else:
            notes.append(f"{now - t0:7.1f}s  {kind} not born (no room)")
    sky.birth = noted_birth

    current = {"tree": None}
    faults = []
    put = sky.put

    def checked_put(cell, ch, attr):  # the sky never writes over the tree or a leaf in the air
        tree = current["tree"]
        if tree is not None and (cell in tree.grid or cell in tree.busy):
            faults.append((round(clock[0] - t0, 1), cell, ch))
        put(cell, ch, attr)
    sky.put = checked_put

    t0 = clock[0]
    sky.new_tree(clock[0] - 300, cfg["cycle"], common.H - 1)
    notes.append(f"before the first tree: mood {sky.mood}, wind {'→' if sky.wind > 0 else '←'}")
    for t in range(300, 0, -1):
        sky.tick(clock[0] - t, {}, draw=False)
    inherit = None
    t_start = clock[0]
    for n in range(trees):
        tree = mod.Tree(scr, cfg, rng, attrs, inherit)
        tree.sky = sky
        current["tree"] = tree
        if inherit is None:
            tree.draw_pot()
        new_tree = sky.new_tree

        def noted_new_tree(now, cycle, floor, n=n):
            new_tree(now, cycle, floor)
            notes.append(f"tree {n + 1} ({tree.style}): mood {sky.mood}, wind {'→' if sky.wind > 0 else '←'}, "
                         f"{len(sky.events)} clouds to come, {len(sky.clouds)} in the sky")
        sky.new_tree = noted_new_tree
        mod.run_tree(scr, cfg, tree, t_start)
        sky.new_tree = new_tree
        t_start += cfg["cycle"] or (clock[0] - t_start)
        inherit = {"planter": tree.planter_spec(), "grid": tree.grid}
    end = clock[0]
    times = [t0 + k * every for k in range(int((end - t0) / every) + 1)]
    for t, (chars, tones) in zip(times, frames(log, times)):
        stamp = f"{int(t - t0):04d}"
        with open(os.path.join(outdir, f"{stamp}.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join("".join(r).rstrip() for r in chars) + "\n")
        with open(os.path.join(outdir, f"{stamp}.tones"), "w", encoding="utf-8") as fh:
            fh.write("\n".join("".join(r).rstrip() for r in tones) + "\n")
    with open(os.path.join(outdir, "sky.log"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(notes) + "\n")
    print(f"{len(times)} frames over {end - t0:.0f}s in {outdir}; {len(notes)} notes in sky.log; "
          f"{len(faults)} sky cells written over the tree" + (f", e.g. {faults[:3]}" if faults else ""))


if __name__ == "__main__":
    main()
