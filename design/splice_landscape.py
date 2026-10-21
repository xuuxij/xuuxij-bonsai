"""Splice the designer's landscape generator into the program as its own section,
renaming the generic names, and append the Backdrop class."""
import re
import sys

HERE = sys.argv[1]
src = open(f"{HERE}/landscape_shapes.py", encoding="utf-8").read().split("\n")
prog = open(f"{HERE}/xuuxij-bonsai", encoding="utf-8").read()

start = next(i for i, l in enumerate(src) if l.startswith("# ---- the palette"))
end = next(i for i, l in enumerate(src) if l.startswith("def rows_text"))
section = "\n".join(src[start:end]).rstrip() + "\n"

renames = {
    r"\blayout\(": "land_layout(", r"\bprofiles\(": "land_profiles(", r"\bpaint\(": "land_paint(",
    r"\bhalftone\(": "land_halftone(", r"\bink\(": "land_ink(", r"\bspears\(": "land_spears(",
    r"\bstamp\(": "land_stamp(", r"\bshape\(": "land_shape(", r"\bplace_pines\(": "land_pines(",
    r"\bbackdrop\(": "land_backdrop(", r"\bblack\)": "ink_black)", r"\bdef black\(": "def ink_black(",
}
for pat, rep in renames.items():
    section = re.sub(pat, rep, section)
# the design file's palettes are the DESIGN (full light); the program shows a dimmed copy
section = re.sub(r"\bPALETTE_(DAY|DAWN|EVENING|NIGHT)\b", r"DESIGN_\1", section)
# the inner helper in ink() was named put(): keep it local but distinct
section = section.replace("    def put(y, x, ch, fg, bg=None):", "    def write(y, x, ch, fg, bg=None):")
section = re.sub(r"(?m)^(\s+)put\((y|L\[\"lake_bot\"\])", r"\1write(\2", section)
assert "def land_backdrop(" in section and "def land_ink(" in section
assert not re.search(r"(?m)^\s+put\(", section), "a put( call was not renamed"

head = '''# ---- the landscape ---------------------------------------------------------------------
# The mountain landscape behind everything, designed from references on ASCII landscape
# art, image halftoning and the sansui painting conventions (docs/references.md): a blue
# print behind a coloured tree. Made in three passes, "paint, halftone, ink": the scene
# is painted in RGB per cell (the sky's gradation, three ranges of mountains, the spear
# mist, a still lake, the near shore), halftoned to the nearest mix the console shows (a
# glyph from " ░▒█" in one slot over one of four background slots, with an ordered dither),
# then drawn over with ASCII strokes (ridge lines, hatching, tree tops, the framing pines).
# Built once per run from the seed: the same place for every tree.

'''
tail = '''

# A paint letter -> (console colour, bold). Backgrounds use the colour alone.
LAND_INK = {"k": (0, False), "B": (4, False), "b": (5, False), "p": (6, False), "g": (7, False),
            "d": (0, True), "i": (4, True), "h": (5, True), "c": (6, True), "W": (7, True)}
# The landscape keeps to five slots (4 5 6 12 15) so the clouds have four of their own
# (7 8 13 14) that stay bright however dim the landscape is: its finer tones are merged
# (soft white and ice into the snow white, rock into the slate, haze into the mid sky).
LAND_REMAP = {"g": "W", "c": "W", "d": "i", "h": "b"}

# What the console shows: the design's colours with the landscape's lightness scaled
# down (the owner wants a dim ground that keeps its contrast and a little of its colour)
# and its chroma kept or scaled, the clouds' greys at their own lightness, the tree's
# and planter's as designed. Scaling lightness in a perceptual space (OKLab) keeps the
# steps between the tones, where scaling the light itself crushed them together. The
# halftone is always made against the design, so the picture keeps its texture.
LANDSCAPE_L = 0.26        # the landscape's lightness, as a share of the design's
LANDSCAPE_CHROMA = 1.0    # and its colour (1 = as designed)
CLOUD_L = 0.41            # the clouds' greys' lightness
LANDSCAPE_SLOTS = (4, 5, 6, 12, 15)
CLOUD_SLOTS = {13: "W", 14: "c", 7: "g", 8: "d"}  # slot -> the tonal clouds' tone


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _srgb(v):
    v = max(0.0, min(1.0, v))
    return int(round((12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055) * 255))


def shade(hexcol, k_l, k_c=1.0):
    """`hexcol` with its lightness scaled by k_l and its chroma by k_c (OKLab)."""
    r, g, b = (_lin(c) for c in hex_rgb(hexcol))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_) * k_l
    a = (1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_) * k_c
    bb = (0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_) * k_c
    l_ = (L + 0.3963377774 * a + 0.2158037573 * bb) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * bb) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * bb) ** 3
    return "#%02x%02x%02x" % (_srgb(4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_),
                              _srgb(-1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_),
                              _srgb(-0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_))


def display_palette(design, cloud_tones):
    out = {}
    for slot, (rgb, use) in design.items():
        if slot in LANDSCAPE_SLOTS:
            out[slot] = (shade(rgb, LANDSCAPE_L, LANDSCAPE_CHROMA), use)
        elif slot in CLOUD_SLOTS:
            out[slot] = (shade(cloud_tones[CLOUD_SLOTS[slot]], CLOUD_L), use)
        else:
            out[slot] = (rgb, use)
    return out


class Backdrop:
    """The landscape as the screen holds it: a character and an attribute per cell, with
    the background slot each cell shows, so everything drawn over it (the tree, the
    planter, the clouds, a falling leaf) takes the cell's own background."""

    HALO_CHARS = set("░▒/\\\\'.-_~^")  # texture and light strokes give way to the halo

    def __init__(self, W, H, seed, pairs, fallback=False):
        cells, self.meta = land_backdrop(W, H, seed)
        self.W, self.H, self.pairs = W, H, pairs
        self.layer = self.meta["layer"]  # per cell: ' ' open sky, C far range, B main range, A hills, M mist, L lake, S shore, T table
        self.chars, self.fgl, self.bg, self.attr = [], [], [], []
        self.halo = {}  # cell -> how many tree cells it neighbours: a blank margin of paper
        for row in cells:
            chars, fgs, bgs, attrs = [], [], [], []
            for ch, fg, bg in row:
                if fallback:  # a terminal whose palette cannot be set: the standard colours
                    fg, bg = FALLBACK.get(fg, fg), ("B" if bg == "b" else bg)
                else:
                    fg = LAND_REMAP.get(fg, fg)
                colour, bold = LAND_INK[fg]
                under = LAND_INK[bg][0]
                chars.append(ch)
                fgs.append(fg)
                bgs.append(under)
                attrs.append(pairs.attr(colour, under) | (curses.A_BOLD if bold else 0))
            self.chars.append(chars)
            self.fgl.append(fgs)
            self.bg.append(bgs)
            self.attr.append(attrs)

    def cell(self, y, x):
        if (y, x) in self.halo:
            return " ", self.pairs.attr(7, self.bg[y][x])
        return self.chars[y][x], self.attr[y][x]

    def halo_shift(self, cell, d):
        """Counts a neighbouring tree cell in (+1) or out (-1); True when the cell's look
        changed. Solid blocks and the landscape's own ink (slate and black: pines, shore,
        tree tops, gullies) keep their marks."""
        y, x = cell
        if self.chars[y][x] not in self.HALO_CHARS or self.fgl[y][x] in ("k", "i"):
            return False
        before = self.halo.get(cell, 0)
        after = before + d
        if after > 0:
            self.halo[cell] = after
        else:
            self.halo.pop(cell, None)
        return (before > 0) != (after > 0)

    def clear(self, y, x0, x1):
        """Blanks the cells x0..x1 of row y to black: the planter's body sits on black."""
        for x in range(max(0, x0), min(self.W - 1, x1) + 1):
            self.chars[y][x], self.fgl[y][x], self.bg[y][x] = " ", "k", 0
            self.attr[y][x] = self.pairs.attr(0, 0)

    def draw(self, scr):
        """Paints the whole landscape (runs of one attribute at a time)."""
        for y in range(self.H):
            chars, attrs = self.chars[y], self.attr[y]
            x = 0
            while x < self.W:
                k = x + 1
                while k < self.W and attrs[k] == attrs[x]:
                    k += 1
                try:
                    scr.addstr(y, x, "".join(chars[x:k]), attrs[x])
                except curses.error:
                    pass
                x = k
'''
marker = "# ---- the sky ----"
i = prog.index(marker)
old = prog.find("# ---- the landscape ----")
if 0 <= old < i:  # replace the section already spliced in
    prog = prog[:old] + prog[i:]
    i = old
prog = prog[:i] + head + section + tail + "\n\n" + prog[i:]
open(f"{HERE}/xuuxij-bonsai", "w", encoding="utf-8", newline="\n").write(prog)
print("spliced", section.count("\n"), "lines")
