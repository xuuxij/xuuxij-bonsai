#!/usr/bin/env python3
"""Run four timed cycles off-screen on a virtual clock and report each tree's timing.

    python3 timer_test.py SEED [key=value ...] [PROGRAM=..] [CONFIG=..]
"""

import random
import sys

from common import Screen, plain_attrs, setup, virtual_clock


def main():
    mod, cfg, rest = setup(sys.argv[1:])
    rng = random.Random(int(rest[0]) if rest else 1)
    clock, log = virtual_clock(mod)
    scr = Screen(clock, log)
    inherit, t_start = None, 0.0
    for n in range(4):
        tree = mod.Tree(scr, cfg, rng, plain_attrs(mod, cfg), inherit)
        if inherit is None:
            tree.draw_pot()
        t0 = clock[0]
        mod.run_tree(scr, cfg, tree, t_start)
        print(f"tree {n + 1}: {tree.style}{' twin' if tree.twin else ''}, {tree.report.get('tempo', 'no clock')}; "
              f"started at {t0:.0f} s, done at {clock[0]:.0f} s, took {clock[0] - t0:.1f} s")
        t_start = t_start + cfg["cycle"] if cfg["cycle"] else clock[0]
        inherit = {"planter": tree.planter_spec(), "grid": tree.grid}


if __name__ == "__main__":
    main()
