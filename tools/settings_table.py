#!/usr/bin/env python3
"""Prints the settings reference for the README, from the program's own table.

    python3 settings_table.py [PROGRAM=..]
"""

import sys

from common import setup


def main():
    mod, _cfg, _rest = setup(sys.argv[1:])
    print("| Setting | Default | What it does |")
    print("|---|---|---|")
    for key, (default, kind, low, high, text) in mod.SETTINGS.items():
        shown = mod.show(default)
        if kind == "duration":
            shown = "10m"
        rng = f" ({low:g} to {high:g})" if low is not None and kind in (int, float) else ""
        print(f"| `{key}` | `{shown}` | {text}{rng} |")


if __name__ == "__main__":
    main()
