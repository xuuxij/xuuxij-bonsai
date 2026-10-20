#!/usr/bin/env python3
"""Grow trees off-screen and save snapshots of each build for review.

    python3 render_review.py OUTDIR [SEED ...] [key=value ...] [phases] [PROGRAM=..] [CONFIG=..]

For each seed it writes OUTDIR/seed-N.txt: the tree at 20 %, 50 %, 80 % and 100 % of
its growth, with `phases` frames of the autumn as well, then a map of what each finished
cell is (w wood, t moving tip, L/l bright/dim leaf, b bud, m moss, p planter, y/r
turned leaves), then the build's numbers.
"""

import os
import random
import sys

from common import Screen, frame, plain_attrs, setup, text_of, virtual_clock


def checks(tree, chars, kinds):
    wood_cells = [(y, x) for y in range(len(chars)) for x in range(len(chars[0])) if kinds[y][x] in "wt"]
    leaf_cells = [(y, x) for y in range(len(chars)) for x in range(len(chars[0])) if kinds[y][x] in "Llb"]
    out = dict(tree.report)
    out["wood cells"], out["leaf cells"] = len(wood_cells), len(leaf_cells)
    out["leaf / wood"] = f"{len(leaf_cells) / max(1, len(wood_cells)):.2f}"
    out["top row with anything"] = min((y for y, x in wood_cells + leaf_cells), default=None)
    out["strokes"] = len(tree.strokes)
    out["clouds"] = f"{tree.clouds} kept, in {sum(s.kind == 'leaf' for s in tree.strokes)} pads"
    out["branches"] = (f"{sum(s.kind == 'primary' for s in tree.strokes)} main, "
                       f"{sum(s.kind == 'secondary' for s in tree.strokes)} secondary, "
                       f"{sum(s.kind == 'fallb' for s in tree.strokes)} on the fall")
    path = [tree.trunk_path[y] for y in sorted(tree.trunk_path, reverse=True)]
    diffs = [b - a for a, b in zip(path, path[1:]) if b != a]
    out["trunk direction changes"] = sum(1 for a, b in zip(diffs, diffs[1:]) if a * b < 0)
    out["largest step per row"] = max((abs(b - a) for a, b in zip(path, path[1:])), default=0)
    out["pot"] = f"{tree.pot_spec}, trunk on row {tree.base}"
    out["spread"] = tree.spread()
    return out


def main():
    mod, cfg, rest = setup(sys.argv[1:])
    phases = "phases" in rest
    rest = [r for r in rest if r != "phases"]
    outdir, seeds = rest[0], [int(s) for s in rest[1:]] or [1, 2, 3, 4]
    os.makedirs(outdir, exist_ok=True)
    for seed in seeds:
        clock, log = virtual_clock(mod)
        scr = Screen(clock, log)
        tree = mod.Tree(scr, dict(cfg, seed=seed), random.Random(seed), plain_attrs(mod, cfg))
        tree.draw_pot()
        tree.draw()
        total = clock[0]
        marks = [("grown", total)]
        if phases:
            for name, phase in (("turned", tree.autumn), ("bare", tree.fall), ("crumbled", tree.crumble)):
                clock[0] += 1e-6  # so a phase's first writes never land in the previous frame
                phase()
                marks.append((name, clock[0]))
        log.sort(key=lambda e: e[0])
        parts = []
        for share in (0.2, 0.5, 0.8, 1.0):
            chars, _ = frame(log, total * share)
            parts.append(f"===== seed {seed}: {int(share * 100)} % of the build "
                         f"({total * share:.0f} s of {total:.0f} s) =====\n{text_of(chars)}")
        for (name, t_end), (_prev, t_start) in zip(marks[1:], marks):
            for label, t in ((f"{name}, half way", (t_start + t_end) / 2), (name, t_end)):
                chars, kinds_now = frame(log, t)
                parts.append(f"===== seed {seed}: {label} ({t:.0f} s) =====\n{text_of(chars)}")
                if name == "turned":
                    parts.append(f"===== seed {seed}: {label}, what each cell is =====\n{text_of(kinds_now)}")
        chars, kinds = frame(log, total)
        parts.append(f"===== seed {seed}: what each finished cell is =====\n{text_of(kinds)}")
        numbers = checks(tree, chars, kinds)
        numbers["build time"] = f"{total:.0f} s"
        if phases:
            numbers["phases"] = ", ".join(f"{name} at {t:.0f} s" for name, t in marks[1:])
        parts.append(f"===== seed {seed}: numbers =====\n" + "\n".join(f"{k}: {v}" for k, v in numbers.items()))
        with open(os.path.join(outdir, f"seed-{seed}.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n\n".join(parts) + "\n")
        print(f"seed {seed}: {numbers.get('style')}{' twin' if numbers.get('twin') else ''}, "
              f"{numbers['build time']}, {numbers['branches']}, {numbers['clouds']}, "
              f"leaf/wood {numbers['leaf / wood']}, {numbers.get('planter')}, {numbers.get('composition')}")


if __name__ == "__main__":
    main()
