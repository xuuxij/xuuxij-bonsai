#!/usr/bin/env python3
"""Grow four trees in a row in one planter, off-screen, and show the carpet building up.

    python3 cycles.py SEED [key=value ...] [PROGRAM=..] [CONFIG=..]
"""

import random
import sys

from common import Screen, frame, plain_attrs, setup, virtual_clock


def main():
    mod, cfg, rest = setup(sys.argv[1:])
    rng = random.Random(int(rest[0]) if rest else 1)
    clock, log = virtual_clock(mod)
    scr = Screen(clock, log)
    inherit = None
    for n in range(4):
        tree = mod.Tree(scr, cfg, rng, plain_attrs(mod, cfg), inherit)
        if inherit is None:
            tree.draw_pot()
        tree.draw()
        tree.autumn()
        tree.fall()
        tree.crumble()
        carpet = sum(1 for e in tree.grid.values() if e[0] in ("fallen", "dust"))
        rows = sorted({y for (y, x), e in tree.grid.items() if e[0] in ("fallen", "dust")})
        print(f"tree {n + 1}: {tree.style}{' twin' if tree.twin else ''} in {tree.report['planter']}, "
              f"carpet {carpet} cells on rows {rows[0] if rows else '-'} to {rows[-1] if rows else '-'}")
        inherit = {"planter": tree.planter_spec(), "grid": tree.grid}
    log.sort(key=lambda e: e[0])
    chars, _ = frame(log, clock[0])
    print("\n".join("".join(r).rstrip() for r in chars[tree.base - 6:]))


if __name__ == "__main__":
    main()
