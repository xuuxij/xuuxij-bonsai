"""Shared by the tools: loads the program as a module, builds a recording screen on a
virtual clock, and resolves the program and settings paths (next to this folder by
default, or PROGRAM= and CONFIG= among the arguments)."""

import importlib.machinery
import importlib.util
import os
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
H, W = 120, 135  # the console this was made for: portrait
BOLD = 1 << 21   # curses.A_BOLD


def load(program):
    loader = importlib.machinery.SourceFileLoader("bonsai", program)
    spec = importlib.util.spec_from_loader("bonsai", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


class Screen:
    """A curses window that only records what is written, when."""

    def __init__(self, clock, log):
        self.clock, self.log = clock, log

    def getmaxyx(self):
        return (H, W)

    def addstr(self, y, x, text, attr=0):
        self.log.append((self.clock[0], y, x, text, attr))

    def refresh(self):
        pass

    def erase(self):
        pass

    def move(self, y, x):
        pass

    def clrtoeol(self):
        pass

    def timeout(self, ms):
        pass

    def getch(self):
        return -1


def setup(argv):
    """Parses `key=value` overrides, PROGRAM=, CONFIG= and SIZE=COLSxROWS (the screen to
    render for, default 135x120); returns (mod, cfg, rest)."""
    global H, W
    program = os.path.join(ROOT, "xuuxij-bonsai")
    config = os.path.join(ROOT, "xuuxij-bonsai.conf")
    rest, overrides = [], []
    for item in argv:
        if item.startswith("PROGRAM="):
            program = item[8:]
        elif item.startswith("CONFIG="):
            config = item[7:]
        elif item.startswith("SIZE="):
            cols, rows = item[5:].lower().split("x")
            W, H = int(cols), int(rows)
        elif "=" in item:
            overrides.append(item)
        else:
            rest.append(item)
    mod = load(program)
    cfg = mod.load_config(config)
    for item in overrides:
        key, value = item.split("=", 1)
        cfg[key] = mod.convert(key, value)
    return mod, cfg, rest


def virtual_clock(mod):
    """Replaces the program's clock and its waits: time passes only as the program waits."""
    clock, log = [0.0], []
    mod.time = types.SimpleNamespace(monotonic=lambda: clock[0], time=lambda: clock[0])
    mod.pause = lambda _scr, seconds, clock=clock: clock.__setitem__(0, clock[0] + max(0.0, seconds))
    return clock, log


def plain_attrs(mod, cfg):
    """Attributes the tools can read back: one number per part."""
    return {"color": {name: 6 for name in mod.COLORS}, "wood": 1, "tip": 2 if cfg["highlight"] else 1,
            "leaf": (3, 4), "leaf_under": 3, "bud": 5, "moss": 7, "gravel": 6, "shadow": 6, "stand": 6, "turn": [8, 9]}


def colour_attrs(mod, cfg):
    """Attributes that carry the console colour: 10 + the colour's number, plus bold."""
    color = {name: 10 + i for i, name in enumerate(mod.COLORS)}
    wood, leaf = color[cfg["trunk_color"]], color[cfg["leaf_color"]]
    return {"color": color, "wood": wood, "tip": wood | BOLD, "leaf": (leaf, leaf | BOLD), "leaf_under": color["black"], "bud": leaf,
            "moss": leaf, "gravel": color["white"], "shadow": color["black"] | BOLD,
            "stand": color[cfg["stand_color"]],
            "turn": [color[n] | BOLD for n in cfg["autumn_colors"].split()]}


def frame(log, until):
    """The screen at time `until`: the characters, and what each cell is."""
    classes = {1: "w", 2: "t", 3: "l", 4: "L", 5: "b", 6: "p", 7: "m", 8: "y", 9: "r"}
    chars = [[" "] * W for _ in range(H)]
    kinds = [[" "] * W for _ in range(H)]
    for t, y, x, text, attr in log:
        if t > until:
            break
        for i, ch in enumerate(text):
            if 0 <= y < H and 0 <= x + i < W:
                chars[y][x + i] = ch
                kinds[y][x + i] = classes.get(attr & 0xFF, "?") if ch != " " else " "
    return chars, kinds


def text_of(grid):
    lines = ["".join(row).rstrip() for row in grid]
    while lines and not lines[0]:
        lines.pop(0)
    return "\n".join(lines)


