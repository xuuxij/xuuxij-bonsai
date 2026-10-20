#!/usr/bin/env python3
"""Grow trees in a row in one planter and check the carpet obeys the heap's rules: no
leaf or dust with nothing under it, no slope steeper than a cell a row, piles within
their height. Prints the bottom of the screen after each autumn.

    python3 heap_check.py SEED [TREES] [key=value ...] [PROGRAM=..] [CONFIG=..] [SIZE=..]
"""

import random
import sys

import common
from common import Screen, frame, plain_attrs, setup, virtual_clock


class mod_pile_rows:
    value = 2


def faults(tree):
    """Carpet cells that break the rules."""
    out = []
    for (y, x), e in tree.grid.items():
        if e[0] not in ("fallen", "dust"):
            continue
        below = (y + 1, x)
        if y + 1 < tree.H and tree.passable(below) and not tree.is_carpet(below):
            out.append((y, x, "nothing under it"))
        for dx in (-1, 1):
            side, lower = (y, x + dx), (y + 1, x + dx)
            if (tree.passable(side) and y + 1 < tree.H and tree.passable(lower) and not tree.is_carpet(lower)):
                out.append((y, x, "could slide"))
        top = tree.surface(x)
        if y < top - getattr(mod_pile_rows, "value", 2):
            out.append((y, x, f"too high: ground row {top}"))
    return out


def main():
    mod, cfg, rest = setup(sys.argv[1:])
    mod_pile_rows.value = getattr(mod, "PILE_ROWS", 2)
    rng = random.Random(int(rest[0]) if rest else 1)
    trees = int(rest[1]) if len(rest) > 1 else 4
    clock, log = virtual_clock(mod)
    scr = Screen(clock, log)
    inherit = None
    for n in range(trees):
        tree = mod.Tree(scr, cfg, rng, plain_attrs(mod, cfg), inherit)
        if inherit is None:
            tree.draw_pot()
        tree.draw()
        tree.autumn()
        tree.fall()
        after_fall = faults(tree)
        tree.crumble()
        after_crumble = faults(tree)
        carpet = sum(1 for e in tree.grid.values() if e[0] in ("fallen", "dust"))
        print(f"tree {n + 1}: {tree.style}{' twin' if tree.twin else ''}, carpet {carpet} cells; "
              f"faults after the fall {len(after_fall)}, after the crumble {len(after_crumble)}"
              + (f" e.g. {after_crumble[:3]}" if after_crumble else ""))
        inherit = {"planter": tree.planter_spec(), "grid": tree.grid}
    log.sort(key=lambda e: e[0])
    chars, _ = frame(log, clock[0])
    print("\n".join("".join(r).rstrip() for r in chars[tree.base - 8:]))


if __name__ == "__main__":
    main()
