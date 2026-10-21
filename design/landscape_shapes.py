#!/usr/bin/env python3
"""The mountain landscape behind the bonsai: the backdrop generator (design hand-in).

    python3 landscape_shapes.py COLS ROWS SEED            # the backdrop as text (characters)
    python3 landscape_shapes.py COLS ROWS SEED fg         # the foreground paint letters
    python3 landscape_shapes.py COLS ROWS SEED bg         # the background paint letters
    python3 landscape_shapes.py COLS ROWS SEED png OUT.png [PALETTE]   # a review render (needs PIL)
    python3 landscape_shapes.py shapes                    # the fixed drawings (pines), text + paint
    python3 landscape_shapes.py stats COLS ROWS SEED      # colour pairs used, cell counts per layer

The backdrop is made in three passes, "paint, halftone, ink":

1. PAINT. The scene is painted in RGB at cell resolution (one colour per cell): the sky's
   gradation, three ranges of mountains back to front, the spear mist, the lake, the near
   shore. Shapes are profiles (a ridge row per column, in half-rows) drawn from the seed.
2. HALFTONE. Every cell's colour is matched to the nearest mix the console can show:
   a character from " ░▒█" in a foreground slot over a background slot (the four
   background slots the landscape may use: black and the three sky blues), with an 8x8
   ordered (Bayer) dither so the gradations are smooth and a penalty on grainy mixes.
3. INK. Structural strokes are written over the halftone: the ridge lines (/ \ ' . - _ ^
   by the ridge's slope and where it crosses the cell), the gullies and hatching on the
   mountain faces, the tree tops on the hills, the framing pines, the shore's tufts, the
   lake's few ripples. Each stroke keeps the background slot of the cell it lands on.

The result is rows of cells (char, fg letter, bg letter). Letters -> slots: LETTERS.
Only " ░▒█" and ASCII strokes are used: no font switch is needed (Uni2-Fixed has them).
"""

import math
import random
import sys

# ---- the palette ---------------------------------------------------------------------------
# slot -> (RGB by day, what uses it). The tree's and planter's slots are listed so the whole
# 16-slot palette is in one place; the landscape only draws with the slots in LETTERS.
PALETTE_DAY = {
    0:  ("#000000", "the console; the table under the planter; pines, forest, deepest shade"),
    1:  ("#9c4a30", "rosewood stand, Teizan red clay (planter only)"),
    2:  ("#1f6d2b", "leaves shaded (tree only)"),
    3:  ("#4f3014", "trunk, branches, Teizan trim (tree only; unchanged)"),
    4:  ("#5c7190", "deep sky, zenith (bg); the oval pot's glaze"),
    5:  ("#8092a8", "mid sky (bg)"),
    6:  ("#a9b5c1", "pale sky at the horizon, mist, far lake (bg); the celadon pot"),
    7:  ("#c9d0d6", "soft white g: snow in shade, light dots (the display gives this slot to the clouds)"),
    8:  ("#7f8b97", "grey-blue d: rock (the display gives this slot to the clouds)"),
    9:  ("#d33a1e", "autumn red leaves (tree only)"),
    10: ("#3db04a", "leaves lit, buds (tree only)"),
    11: ("#cf8f1c", "growing tip, autumn yellow leaves (tree only)"),
    12: ("#3b4757", "slate: pines, shore, forest, tree tops, gullies (the landscape's ink); oval pot pattern"),
    13: ("#8d99a8", "haze h: the far range (the display gives this slot to the clouds)"),
    14: ("#bfc8d1", "ice c: bright mist, snow in shade (the display gives this slot to the clouds)"),
    15: ("#e4e8ec", "bright white: sunlit snow, the landscape's lightest dots; the white pots' highlight"),
}
# The same slots at other hours (round 2 material: swapped at a tree boundary by the clock).
PALETTE_EVENING = {**PALETTE_DAY, **{
    4: ("#5a657e", ""), 5: ("#86899c", ""), 6: ("#b3aba6", ""),
    12: ("#3f4553", ""),
    15: ("#e8d8cc", "")}}
PALETTE_NIGHT = {**PALETTE_DAY, **{
    4: ("#1a2230", ""), 5: ("#27303f", ""), 6: ("#3e4858", ""),
    12: ("#232b37", ""),
    15: ("#b7c1cf", "")}}
PALETTE_DAWN = {**PALETTE_DAY, **{
    4: ("#6a7a90", ""), 5: ("#8c9bae", ""), 6: ("#b4bcc6", ""),
    12: ("#46505e", ""),
    15: ("#ece9e6", "")}}
PALETTES = {"day": PALETTE_DAY, "dawn": PALETTE_DAWN, "evening": PALETTE_EVENING,
            "night": PALETTE_NIGHT}
# The clock (round 2): night 21:00-05:59, dawn 06:00-07:59, day 08:00-16:59, evening
# 17:00-20:59, local time, swapped at a tree boundary; only these nine slots move.

# Paint letters (foreground) -> slots. W, g, d keep the sky design's meaning.
LETTERS = {"k": 0, "B": 4, "b": 5, "p": 6, "g": 7, "d": 8, "i": 12, "h": 13, "c": 14, "W": 15}
BG_LETTERS = "kBbp"   # the only background slots the landscape uses (0, 4, 5, 6)
# When the palette cannot be set (curses.can_change_color() is false), remap:
FALLBACK = {"b": "B", "h": "d", "i": "B", "c": "p"}   # bg 'b' -> 'B' too

COVER = {" ": 0.0, "░": 0.25, "▒": 0.5, "█": 1.0}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else hi if v > hi else v


def smoothstep(e0, e1, v):
    t = clamp((v - e0) / (e1 - e0)) if e1 != e0 else (1.0 if v >= e1 else 0.0)
    return t * t * (3 - 2 * t)


# ---- noise ---------------------------------------------------------------------------------

class Noise:
    """Value noise on a lattice, 1-D and 2-D, from the seed. fbm sums octaves."""

    def __init__(self, rng):
        self.grid = {}
        self.rng = rng

    def _lat(self, *key):
        v = self.grid.get(key)
        if v is None:
            v = self.grid[key] = self.rng.random()
        return v

    def n1(self, x, period, tag=0):
        u = x / period
        i = math.floor(u)
        f = u - i
        f = f * f * (3 - 2 * f)
        return self._lat(tag, i) * (1 - f) + self._lat(tag, i + 1) * f

    def fbm1(self, x, period, octaves=3, gain=0.5, tag=0):
        s, a, p, total = 0.0, 1.0, period, 0.0
        for o in range(octaves):
            s += a * self.n1(x, p, (tag, o))
            total += a
            a *= gain
            p /= 2.0
        return s / total

    def n2(self, x, y, px, py, tag=0):
        u, v = x / px, y / py
        i, j = math.floor(u), math.floor(v)
        fu, fv = u - i, v - j
        fu = fu * fu * (3 - 2 * fu)
        fv = fv * fv * (3 - 2 * fv)
        a = self._lat(tag, i, j) * (1 - fu) + self._lat(tag, i + 1, j) * fu
        b = self._lat(tag, i, j + 1) * (1 - fu) + self._lat(tag, i + 1, j + 1) * fu
        return a * (1 - fv) + b * fv

    def fbm2(self, x, y, px, py, octaves=3, gain=0.5, tag=0):
        s, a, total = 0.0, 1.0, 0.0
        for o in range(octaves):
            s += a * self.n2(x, y, px, py, (tag, o))
            total += a
            a *= gain
            px /= 2.0
            py /= 2.0
        return s / total


# ---- the layout ----------------------------------------------------------------------------

def layout(W, H):
    """Where the bands fall, in rows, for a screen of W x H. Shares of the height; the
    planter's table at the bottom keeps the black the planter was designed on."""
    tall = H >= 45
    L = {
        "summit": max(1, round(0.06 * H)),          # the main summit's row
        "far_top": max(2, round(0.12 * H)),         # the far range's highest crest
        "hill_top": round(0.22 * H),                # the side hills' crests
        "mist_top": round(0.35 * H),                # the spear mist's core begins
        "mist_bot": round(0.45 * H),                # the lake begins (hidden shore)
        "lake_bot": round(0.80 * H) if tall else H - 2,
        "shore_bot": round(0.86 * H) if tall else H - 1,
        "margin": max(2, W // 13),                  # the tree keeps clear of this (MARGIN rule)
        "centre": (int(0.34 * W), int(0.66 * W)),   # the quiet column band above the crown
    }
    L["spear_rise"] = max(2, round(0.10 * H))       # how far above mist_top the spears reach
    return L


# ---- the profiles (ridge rows per column, in half-rows: 2 per cell) -------------------------

def peak_profile(W, base2, peaks, noise, tag, rough, max_slope=2.0):
    """The upper envelope of peaks (x, height in half-rows, left width, right width,
    exponent), roughened by fbm scaled to the local height, slopes clamped."""
    y = []
    for x in range(W):
        best = base2
        for (px, h, wl, wr, k) in peaks:
            d = (px - x) / wl if x < px else (x - px) / wr
            if d < 1:
                v = base2 - h * (1 - d) ** k
                best = min(best, v)
        y.append(best)
    out = []
    for x in range(W):
        local = base2 - y[x]
        n = (noise.fbm1(x, 11.0, 3, 0.55, tag) - 0.5) * 2
        out.append(y[x] + n * rough * (0.35 + 0.65 * local / max(1, base2)) * 6)
    # no slope steeper than max_slope half-rows per column (a / or \ per cell)
    for x in range(1, W):
        out[x] = max(out[x], out[x - 1] - max_slope)
    for x in range(W - 2, -1, -1):
        out[x] = max(out[x], out[x + 1] - max_slope)
    return out


def profiles(rng, W, H, L, noise):
    """The three ranges, the snowline and the light, drawn from the seed."""
    base2 = 2 * L["mist_bot"] + 2
    summit2 = 2 * L["summit"]
    hmain = base2 - summit2
    light = rng.choice((-1, 1))                 # -1: light from the left; +1: from the right
    side = rng.choice((-1, 1))                  # the main summit left (-1) or right of centre
    u_main = 0.5 + side * rng.uniform(0.11, 0.17)
    x_main = int(u_main * W)
    # The main range is a massed ridge, not one spike: the main summit (steep near the top,
    # k>1, a wide foot, asymmetric), a second summit across the centre, a shoulder beside
    # the main one, and three to five lesser summits spread along the width, so the crest
    # runs the whole screen with saddles between.
    wl = rng.uniform(0.5, 0.7) * W
    wr = rng.uniform(0.5, 0.7) * W
    peaks = [(x_main, hmain, wl, wr, rng.uniform(1.35, 1.6))]
    x2 = int((1 - u_main + side * rng.uniform(-0.04, 0.06)) * W)
    peaks.append((x2, hmain * rng.uniform(0.70, 0.86), rng.uniform(0.3, 0.5) * W,
                  rng.uniform(0.3, 0.5) * W, rng.uniform(1.25, 1.5)))
    peaks.append((x_main - side * int(rng.uniform(0.09, 0.14) * W), hmain * rng.uniform(0.62, 0.74),
                  rng.uniform(0.2, 0.32) * W, rng.uniform(0.2, 0.32) * W, rng.uniform(1.15, 1.4)))
    n_lesser = rng.randint(3, 5)
    for i in range(n_lesser):
        px = int((i + rng.uniform(0.15, 0.85)) / n_lesser * W)
        peaks.append((px, hmain * rng.uniform(0.45, 0.68), rng.uniform(0.12, 0.25) * W,
                      rng.uniform(0.12, 0.25) * W, rng.uniform(1.1, 1.4)))
    yB = peak_profile(W, base2, peaks, noise, "B", rough=1.0)
    # the far range: lower, smoother, four to six crests, so one shows in every saddle
    far_h = base2 - 2 * L["far_top"]
    fpeaks = []
    n_far = rng.randint(4, 6)
    for i in range(n_far):
        fpeaks.append((int((i + rng.uniform(0.2, 0.8)) / n_far * W), far_h * rng.uniform(0.7, 1.0),
                       rng.uniform(0.15, 0.3) * W, rng.uniform(0.15, 0.3) * W, rng.uniform(1.0, 1.25)))
    yC = peak_profile(W, base2 + 6, fpeaks, noise, "C", rough=0.5, max_slope=1.5)
    # the side hills: a wooded crest just inside each edge, falling toward the centre band
    # and reaching the mist before it; a lesser knoll on each
    c0, c1 = L["centre"]
    hill_h = base2 - 2 * L["hill_top"]
    hpeaks = [(int(0.03 * W), hill_h * rng.uniform(0.85, 1.0), 0.2 * W, (c0 - 0.03 * W) * rng.uniform(0.85, 1.0), 1.1),
              (int(0.97 * W), hill_h * rng.uniform(0.7, 1.0), (W - c1 - 0.03 * W) * rng.uniform(0.85, 1.0), 0.2 * W, 1.1),
              (int(rng.uniform(0.12, 0.24) * W), hill_h * rng.uniform(0.5, 0.75), 0.1 * W, 0.12 * W, 1.1),
              (int(rng.uniform(0.76, 0.88) * W), hill_h * rng.uniform(0.5, 0.75), 0.12 * W, 0.1 * W, 1.1)]
    yA = peak_profile(W, base2 + 4, hpeaks, noise, "A", rough=1.6, max_slope=2.0)
    snowline = rng.uniform(0.42, 0.58)          # altitude (0 at the mist, 1 at the summit)
    return {"yB": yB, "yC": yC, "yA": yA, "base2": base2, "summit2": summit2, "light": light,
            "x_main": x_main, "snowline": snowline, "side": side}


# ---- paint ---------------------------------------------------------------------------------

SKY_STOPS = [(0.00, "#5c7190"), (0.17, "#8092a8"), (0.34, "#a9b5c1")]
C_SNOW_LIT, C_SNOW_SHADE = hex_rgb("#e0e5ea"), hex_rgb("#b5c0cb")
C_ROCK_LIT, C_ROCK_SHADE = hex_rgb("#98a3ae"), hex_rgb("#76828e")
C_RIB, C_FOREST = hex_rgb("#5a6470"), hex_rgb("#4b5563")
# Round 2: the shade tones a step lighter (sky-lit snow and rock are blue-grey, not navy),
# so a shade face halftones to d on p / d on b mixes and is no longer the heaviest shape.
C_HAZE = hex_rgb("#8d99a8")
C_MIST = hex_rgb("#b9c3cd")
C_LAKE_FAR, C_LAKE_NEAR = hex_rgb("#a9b5c1"), hex_rgb("#96a4b3")
C_HILL, C_HILL_EDGE = hex_rgb("#46525f"), hex_rgb("#56626f")
# These greys sit nearer the grey mixes (d on k, d on B, k on b) than the solid deep blue,
# so shaded rock halftones as grey-blue texture and never as a flat patch of sky blue.
C_REFLECT = hex_rgb("#7d8a98")
C_SHORE, C_SHORE_TOP = hex_rgb("#3b4757"), hex_rgb("#4a5664")


def sky_colour(v):
    stops = [(s, hex_rgb(c)) for s, c in SKY_STOPS]
    if v <= stops[0][0]:
        return stops[0][1]
    for (s0, c0), (s1, c1) in zip(stops, stops[1:]):
        if v <= s1:
            return lerp(c0, c1, (v - s0) / (s1 - s0))
    return stops[-1][1]


def sky_bg_letter(y, H):
    """The background slot the quantizer will give the open sky on this row (for strokes)."""
    v = y / H
    return "B" if v < 0.085 else "b" if v < 0.255 else "p"


def spears(rng, W, L):
    """The spear mist: horizontal bands with straight edges above the mist's core, the
    longest and highest in the centre. Each: (x0, x1, top row)."""
    c0, c1 = L["centre"]
    top = L["mist_top"]
    rise = L["spear_rise"]
    out = []
    n = 6 if W >= 100 else 3
    for i in range(n):
        width = int(rng.uniform(0.22, 0.5) * W)
        if i < 2:   # the centre spears
            cx = int(rng.uniform(c0 + 0.1 * W, c1 - 0.1 * W))
            r = top - rng.randint(int(0.7 * rise), rise)
        else:
            cx = int(rng.uniform(0.05 * W, 0.95 * W))
            r = top - rng.randint(1, max(1, int(0.5 * rise)))
        out.append((max(0, cx - width // 2), min(W - 1, cx + width // 2), r))
    return out


def paint(rng, W, H, L, P, noise):
    """The RGB painting, one colour per cell, with a layer map for the ink pass."""
    img = [[None] * W for _ in range(H)]
    layer = [[" "] * W for _ in range(H)]      # ' ' sky, C far, B main, A hill, M mist, L lake, S shore, T table
    lit_map = [[0.5] * W for _ in range(H)]
    yB, yC, yA = P["yB"], P["yC"], P["yA"]
    light, snowline = P["light"], P["snowline"]
    c0, c1 = L["centre"]
    mist_top, mist_bot = L["mist_top"], L["mist_bot"]
    sp = spears(rng, W, L)
    # Round 2: the mist core's top wanders by a row (-1, 0, +1) along a slow noise, so it
    # is a bank of mist and not a ruled line across the screen.
    wander = [int(round(2.5 * (noise.fbm1(x, 28.0, 2, 0.5, "misttop") - 0.5))) for x in range(W)]
    for y in range(H):
        v = y / H
        for x in range(W):
            mt = mist_top + wander[x]
            col = sky_colour(v)
            lay = " "
            # the far range, in haze, fading into the pale sky toward its feet
            if y * 2 >= yC[x]:
                t = clamp((y - yC[x] / 2) / max(1.0, (mist_top - yC[x] / 2)))
                col = lerp(C_HAZE, hex_rgb("#a9b5c1"), 0.3 + 0.7 * t * t)
                lay = "C"
            # the main range
            if y * 2 >= yB[x]:
                depth = y - yB[x] / 2
                alt = clamp((mist_top - y) / max(1.0, mist_top - P["summit2"] / 2))
                s = (yB[min(W - 1, x + 2)] - yB[max(0, x - 2)]) / 4.0   # half-rows per col, + = falls right
                lit = clamp(0.5 - 0.5 * s * light / 1.2 * -1)             # faces toward the light are lit
                lit = clamp(0.5 + 0.5 * clamp(s * light / 1.2, -1, 1))
                lit_map[y][x] = lit
                nsnow = (noise.fbm2(x, y, 9.0, 4.0, 2, 0.5, "snow") - 0.5) * 0.22
                snow = smoothstep(snowline - 0.10, snowline + 0.10, alt + nsnow)
                snow *= 1.0 - 0.55 * smoothstep(1.2, 2.4, abs(s))   # steep faces shed snow
                # the snow is not flat: wind-packed patches a shade darker, even where lit
                grain = noise.fbm2(x, y, 6.0, 3.0, 2, 0.5, "snowgrain")
                snow_c = lerp(C_SNOW_SHADE, C_SNOW_LIT, lit * (1 - 0.35 * smoothstep(0.55, 0.8, grain)))
                rock_c = lerp(C_ROCK_SHADE, C_ROCK_LIT, lit)
                col = lerp(rock_c, snow_c, snow)
                # ribs: gullies run down the flank, away from the crest
                u = x - (1 if s > 0 else -1) * depth * 0.5
                rib = noise.fbm1(u, 5.0, 2, 0.5, "rib")
                rib_k = smoothstep(0.58, 0.8, rib) * clamp(depth / 5.0) * (0.85 - 0.45 * lit)
                col = lerp(col, C_RIB, rib_k * 0.4)
                # the forest at the feet (outside the centre band; the centre is the mist valley)
                f = smoothstep(0.26, 0.10, alt) * 0.85
                # thinner in the centre band (the mist valley), fading in over eighteen
                # columns each side so the valley has no edge
                f *= 1 - 0.65 * smoothstep(c0 - 14, c0 + 4, x) * smoothstep(c1 + 14, c1 - 4, x)
                col = lerp(col, C_FOREST, f)
                lay = "B"
            # the side hills, dark and wooded, only outside the centre band; their bodies
            # fade into the mist from a few rows under the crest (the mist lies on them)
            if y * 2 >= yA[x] and y < mist_bot + 2:
                edge = smoothstep(2.5, 0.0, y - yA[x] / 2)
                wood = noise.fbm2(x, y, 4.0, 2.0, 2, 0.5, "wood")     # the canopy's unevenness
                hill = lerp(C_HILL, C_HILL_EDGE, 0.6 * edge + 0.3 * (wood - 0.5))
                sink = smoothstep(yA[x] / 2 + 4, mist_top + 3, y) * 0.8
                col = lerp(hill, C_MIST, sink)
                lay = "A"
            # the spear mist: the core band (its top softened over three rows), then the
            # spears above it, straight-edged, their ends tapered over three cells
            a = 0.0
            if mt <= y < mist_bot:
                a = 0.55 + 0.40 * smoothstep(mt - 1, mt + 3, y)
            elif y >= mist_bot:
                a = 0.0
            else:
                # the spears: soft wisps, not slabs; the ends feather over ten cells, the
                # top over three rows, the body thinned by noise, and never solid
                for (x0, x1, r) in sp:
                    if r - 1 <= y and x0 <= x <= x1:
                        end = min(x - x0, x1 - x)
                        wisp = 0.65 + 0.35 * noise.fbm2(x, y, 7.0, 2.5, 2, 0.5, "spear")
                        a = max(a, (0.3 + 0.4 * smoothstep(r, mt, y)) * smoothstep(-2, 10, end)
                                * smoothstep(r - 1, r + 3, y) * wisp)
                a = max(a, 0.45 * smoothstep(mt - 4, mt, y))
            if a > 0:
                col = lerp(col, C_MIST, a)
                if a > 0.5:
                    lay = "M"
            # the lake, pale by the far shore, deeper toward the viewer; faint reflections
            if y >= mist_bot:
                t = smoothstep(0.45, 1.0, (y - mist_bot) / max(1, L["lake_bot"] - mist_bot))
                col = lerp(C_LAKE_FAR, C_LAKE_NEAR, t)
                lay = "L"
                if x < c0 or x > c1:
                    ys = 2 * mist_bot - y          # the hill row this cell mirrors
                    if ys * 2 >= yA[x] and ys < mist_top:
                        fade = 0.4 * smoothstep(mist_bot + 14, mist_bot, y) * (1 - 0.5 * smoothstep(c0 - 10, c0, x) if x < c0 else 1 - 0.5 * smoothstep(c1 + 10, c1, x))
                        col = lerp(col, C_REFLECT, fade)
                # the near shore (dark), its top edge a little lighter
                if y >= L["lake_bot"]:
                    col = lerp(C_SHORE, C_SHORE_TOP, smoothstep(2, 0, y - L["lake_bot"]))
                    lay = "S"
                if y >= L["shore_bot"]:
                    col = (0, 0, 0)
                    lay = "T"
            img[y][x] = col
            layer[y][x] = lay
    return img, layer, lit_map, sp


# ---- halftone ------------------------------------------------------------------------------

BAYER8 = [[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
          [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
          [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
          [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]

# The mixes the quantizer may choose: (fg letter, bg letter, characters allowed).
MIXES = [
    ("k", "k", " "), ("i", "k", "░▒█"), ("B", "k", "░▒"), ("d", "k", "░▒"),
    ("B", "B", " "), ("b", "B", "░▒"), ("d", "B", "░▒"), ("i", "B", "░▒█"),
    ("b", "b", " "), ("B", "b", "░▒"), ("p", "b", "░▒"), ("h", "b", "░▒"), ("d", "b", "░▒"),
    ("i", "b", "░▒█"),
    ("p", "p", " "), ("b", "p", "░▒"), ("c", "p", "░▒█"), ("g", "p", "░▒█"), ("W", "p", "░▒█"),
    ("h", "p", "░▒"), ("d", "p", "░▒█"), ("i", "p", "░▒█"),
]
# Round 4: black (k) is only the table's background; the landscape's darkest tone is the
# slate slot i, so pines, shore, forest and hills are dark grey-blue, never ink-black.
# Solid blocks (█) are allowed only for the snow and rock tones (W, g, c, d): every other
# in-between tone is made inside the cell with ░ ▒, so a gradation never turns into a
# checker of whole cells.
GRAIN = 0.25   # the penalty on mixing two far-apart colours in one cell (round 4: calmer)


def build_mixes(palette):
    rgb = {let: hex_rgb(palette[slot][0]) for let, slot in LETTERS.items()}
    out = []
    for fg, bg, chars in MIXES:
        for ch in chars:
            c = COVER[ch]
            mix = lerp(rgb[bg], rgb[fg], c)
            d2 = sum((rgb[fg][i] - rgb[bg][i]) ** 2 for i in range(3))
            grain = GRAIN * c * (1 - c) * 4 * d2
            out.append((mix, grain, ch, fg, bg))
    return out


def halftone(img, palette, dither=12.0, quiet=None):
    """Each cell's colour -> (char, fg, bg), nearest mix with an ordered dither. `quiet`
    (a function y, x -> factor) scales the dither down where the tree stands."""
    mixes = build_mixes(palette)
    H, W = len(img), len(img[0])
    cells = [[None] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            t = img[y][x]
            amp = dither * (quiet(y, x) if quiet else 1.0)
            off = (BAYER8[y % 8][x % 8] / 64.0 - 0.5) * 2 * amp
            tgt = (t[0] + off, t[1] + off, t[2] + off)
            best, bc = None, 1e18
            for mix, grain, ch, fg, bg in mixes:
                cost = (mix[0] - tgt[0]) ** 2 + (mix[1] - tgt[1]) ** 2 + (mix[2] - tgt[2]) ** 2 + grain
                if cost < bc:
                    bc, best = cost, (ch, fg, bg)
            cells[y][x] = best
    return cells


# ---- ink -----------------------------------------------------------------------------------

def ridge_char(y2, slope):
    """The stroke for a ridge crossing a cell: y2 the crest in half-rows (its parity says
    which half of the cell), slope in half-rows per column (+ = falls to the right)."""
    top = int(math.floor(y2)) % 2 == 0
    if slope <= -1.4:
        return "/"
    if slope >= 1.4:
        return "\\"
    if abs(slope) < 0.35:
        return "'" if top else "_"
    if slope < 0:        # rising to the right: gentle
        return "'" if top else "."
    return "'" if top else "."


def ink(cells, img, layer, lit_map, rng, W, H, L, P, noise):
    """Writes the strokes over the halftone. Returns the cells (changed in place)."""
    yB, yC, yA, light = P["yB"], P["yC"], P["yA"], P["light"]
    c0, c1 = L["centre"]
    mist_top, mist_bot = L["mist_top"], L["mist_bot"]
    snowline = P["snowline"]

    def put(y, x, ch, fg, bg=None):
        if 0 <= y < H and 0 <= x < W:
            cells[y][x] = (ch, fg, bg or cells[y][x][2])

    def slope_at(prof, x):
        return (prof[min(W - 1, x + 1)] - prof[max(0, x - 1)]) / 2.0

    # the far range's crest: a soft line in haze on the sky
    for x in range(W):
        y = int(yC[x] // 2)
        if y < mist_top - 1 and yC[x] < yB[x] - 1 and y >= 0:
            put(y, x, ridge_char(yC[x], slope_at(yC, x)), "h", sky_bg_letter(y, H))
    # the main range's crest: snow-white where snowed, grey where rock; on the sky's bg
    for x in range(W):
        y = int(yB[x] // 2)
        if y >= mist_top - 1:
            continue
        s = slope_at(yB, x)
        alt = clamp((mist_top - y) / max(1.0, mist_top - P["summit2"] / 2))
        snowed = alt + (noise.fbm1(x, 6.0, 2, 0.5, "snowcrest") - 0.5) * 0.2 > snowline - 0.05
        lit = lit_map[min(H - 1, y + 1)][x]
        fg = ("W" if lit > 0.5 else "g") if snowed else ("d" if lit > 0.5 else "d")
        ch = ridge_char(yB[x], s)
        if abs(s) < 0.6 and yB[x] <= min(yB[max(0, x - 1)], yB[min(W - 1, x + 1)]) and alt > 0.5:
            ch = "^"   # a summit
        put(y, x, ch, fg, sky_bg_letter(y, H))
    # gullies and hatching on the faces: down the flank, denser with depth, on the shade side
    for y in range(L["summit"], mist_top):
        for x in range(W):
            if layer[y][x] != "B":
                continue
            depth = y - yB[x] / 2
            if depth < 1.5:
                continue
            s = slope_at(yB, x)
            lit = lit_map[y][x]
            u = x - (1 if s > 0 else -1) * depth * 0.5
            rib = noise.fbm1(u, 5.0, 2, 0.5, "rib")
            thr = 0.80 - 0.05 * clamp(depth / 8.0) - 0.06 * (1 - lit)
            alt = clamp((mist_top - y) / max(1.0, mist_top - P["summit2"] / 2))
            if rib > thr and alt > 0.12:
                ch = "\\" if s > 0 else "/"
                ch_cell, fg_cell, bg_cell = cells[y][x]
                fg = "d" if fg_cell in ("W", "g", "c", "p") else "i"
                put(y, x, ch, fg)
    # tree tops along the hills' crests and at the main range's feet (outside the centre)
    for x in range(W):
        y = int(yA[x] // 2)
        if y < mist_bot:
            put(y, x, "^" if rng.random() < 0.35 else ridge_char(yA[x], slope_at(yA, x)), "i", sky_bg_letter(y, H) if layer[max(0, y - 1)][x] in " C" else None)
            if rng.random() < 0.15 and y + 1 < mist_bot:
                put(y + 1, x, "^", "i")
    for x in range(W):
        if c0 - 4 < x < c1 + 4:
            continue
        for y in range(mist_top - 6, mist_top):
            if layer[y][x] == "B" and y * 2 > yB[x] + 6 and rng.random() < 0.06:
                put(y, x, "^", "d" if cells[y][x][1] in ("W", "g", "c") else "i")
    # the lake: a few ripples, only at the sides and low down, never where the tree stands
    m = L["margin"]
    for y in range(mist_bot + 3, L["lake_bot"]):
        for x in range(W):
            far_side = x < c0 - 8 or x > c1 + 8
            low = y > L["lake_bot"] - 5
            if (far_side and rng.random() < 0.0) or (low and rng.random() < 0.0):   # round 4: no ripples
                put(y, x, "-", "c" if cells[y][x][2] == "p" else "p")
    # the shore: tufts at the water's edge, on the lake's last row (round 4: not on the
    # shore's own row, where they would punch pale holes in the solid slate)
    for x in range(W):
        if rng.random() < 0.15:
            put(L["lake_bot"] - 1, x, rng.choice('"\',.'), "i")
    # the framing pines: one tall near each edge, a shorter beside it, feet on the shore
    place_pines(cells, rng, W, H, L)
    return cells


# ---- the fixed drawings: pines (text rows + paint rows, the sky_shapes form) ---------------

SHAPES = []


def shape(name, text, rule):
    width = max(len(t) for t in text)
    text = [t.ljust(width) for t in text]
    paint = ["".join(" " if ch == " " else rule(y, x, ch) for x, ch in enumerate(line))
             for y, line in enumerate(text)]
    SHAPES.append((name, text, paint))
    return text, paint


def black(y, x, ch):
    return "i"   # round 4: the pines in slate, the landscape's ink, not the console's black


PINE_TALL = shape("pine tall (36 rows)", [
    "     |      ",
    "     ^      ",
    "    /█\\     ",
    "    |█|     ",
    "   /███\\    ",
    "   /███\\    ",
    "    |█|     ",
    "   /███\\    ",
    "  /█████\\   ",
    "  /█████\\   ",
    "   /███\\    ",
    "  /█████\\   ",
    " /███████\\  ",
    " /███████\\  ",
    "  /█████\\   ",
    " /███████\\  ",
    "/█████████\\ ",
    "/█████████\\ ",
    "  /█████\\   ",
    " /███████\\  ",
    "/█████████\\ ",
    "/█████████\\ ",
    " /███████\\  ",
    "/█████████\\ ",
    "/██████████\\",
    "/██████████\\",
    " /███████\\  ",
    "/█████████\\ ",
    "/██████████\\",
    "/██████████\\",
    "/██████████\\",
    "     █      ",
    "     █      ",
    "     █      ",
    "     █      ",
    "     █      ",
], black)

PINE_MID = shape("pine mid (22 rows)", [
    "    ^    ",
    "   /█\\   ",
    "   |█|   ",
    "  /███\\  ",
    "   |█|   ",
    "  /███\\  ",
    " /█████\\ ",
    "  /███\\  ",
    " /█████\\ ",
    "/███████\\",
    " /█████\\ ",
    "/███████\\",
    "/███████\\",
    " /█████\\ ",
    "/███████\\",
    "/███████\\",
    "/███████\\",
    "/███████\\",
    "    █    ",
    "    █    ",
    "    █    ",
    "    █    ",
], black)

PINE_SMALL = shape("pine small (10 rows)", [
    "  ^  ",
    " /█\\ ",
    " |█| ",
    "/███\\",
    " /█\\ ",
    "/███\\",
    "/███\\",
    "/███\\",
    "  █  ",
    "  █  ",
], black)

PINE_RIDGE = shape("pine on a ridge (3 rows)", [
    " ^ ",
    "/█\\",
    " | ",
], black)


def scale_shape(text, rows_wanted):
    """A shorter copy of a pine: rows sampled evenly (the trunk rows kept at the end)."""
    if rows_wanted >= len(text):
        return text
    n = len(text)
    idx = sorted({int(i * (n - 1) / max(1, rows_wanted - 1)) for i in range(rows_wanted)})
    return [text[i] for i in idx]


def stamp(cells, text, paint, y0, x0, H, W):
    for dy, (row, prow) in enumerate(zip(text, paint)):
        for dx, (ch, p) in enumerate(zip(row, prow)):
            if p == " ":
                continue
            y, x = y0 + dy, x0 + dx
            if 0 <= y < H and 0 <= x < W:
                cells[y][x] = (ch, p, cells[y][x][2])


def place_pines(cells, rng, W, H, L):
    """Pines at the two margins, feet on the shore's top row, never alike on both sides:
    one side a tall pine cut by the edge with a small one at its foot, the other a mid
    pine standing a little in from the edge (or a tall one, 1 time in 3). Heights scale
    with the screen; nothing is placed on a screen under 30 rows."""
    if H < 30:
        return
    foot = L["lake_bot"]
    tall_rows = max(8, min(36, int(0.32 * H)))
    mid_rows = max(6, min(22, int(0.19 * H)))
    small_rows = max(4, min(10, int(0.085 * H)))
    tall = (scale_shape(PINE_TALL[0], tall_rows), scale_shape(PINE_TALL[1], tall_rows))
    mid = (scale_shape(PINE_MID[0], mid_rows), scale_shape(PINE_MID[1], mid_rows))
    small = (scale_shape(PINE_SMALL[0], small_rows), scale_shape(PINE_SMALL[1], small_rows))
    tw, mw, sw = len(tall[0][0]), len(mid[0][0]), len(small[0][0])
    tall_side = rng.choice((-1, 1))
    for side in (-1, 1):
        if side == tall_side:
            cut = rng.randint(2, 4)
            tx = -cut if side < 0 else W - tw + cut
            stamp(cells, tall[0], tall[1], foot - tall_rows + 1, tx, H, W)
            if rng.random() < 0.7:
                sx = (tx + tw - 2) if side < 0 else (tx - sw + 2)
                stamp(cells, small[0], small[1], foot - small_rows + 1, sx, H, W)
        elif rng.random() < 0.33:
            cut = rng.randint(3, 5)
            tx = -cut if side < 0 else W - tw + cut
            stamp(cells, tall[0], tall[1], foot - tall_rows + 1, tx, H, W)
        else:
            inset = rng.randint(1, 3)
            mx = inset if side < 0 else W - mw - inset
            stamp(cells, mid[0], mid[1], foot - mid_rows + 1, mx, H, W)
            if rng.random() < 0.5:
                sx = (mx + mw - 1) if side < 0 else (mx - sw + 1)
                stamp(cells, small[0], small[1], foot - small_rows + 1, sx, H, W)


# ---- the backdrop --------------------------------------------------------------------------

def backdrop(W, H, seed, palette=PALETTE_DAY):
    """Rows of cells (char, fg letter, bg letter) for a W x H screen from the seed."""
    rng = random.Random(seed)
    noise = Noise(random.Random(seed * 7919 + 1))
    L = layout(W, H)
    P = profiles(rng, W, H, L, noise)
    img, layer, lit_map, sp = paint(rng, W, H, L, P, noise)
    c0, c1 = L["centre"]

    def quiet(y, x):   # less dither where the tree stands: the lake's centre
        if y >= L["mist_top"] and L["margin"] <= x < W - L["margin"]:
            return 0.5   # a little, so a near-threshold tone softens instead of snapping into blocks
        return 1.0

    cells = halftone(img, palette, dither=3.0, quiet=quiet)
    ink(cells, img, layer, lit_map, rng, W, H, L, P, noise)
    return cells, {"layout": L, "profiles": P, "layer": layer}


def rows_text(cells, which="text"):
    out = []
    for row in cells:
        if which == "text":
            out.append("".join(c[0] for c in row))
        elif which == "fg":
            out.append("".join(c[1] if c[0] != " " else "." for c in row))
        else:
            out.append("".join(c[2] for c in row))
    return out


# ---- a review render (PIL) ----------------------------------------------------------------

def render_png(cells, palette, out, scale=1):
    from PIL import Image, ImageDraw, ImageFont
    H, W = len(cells), len(cells[0])
    cw, ch = 8 * scale, 16 * scale
    img = Image.new("RGB", (W * cw, H * ch), (0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", int(14 * scale))
    except OSError:
        font = ImageFont.load_default()
    rgb = {let: hex_rgb(palette[slot][0]) for let, slot in LETTERS.items()}
    for y in range(H):
        for x in range(W):
            c, fg, bg = cells[y][x]
            X, Y = x * cw, y * ch
            d.rectangle([X, Y, X + cw - 1, Y + ch - 1], fill=rgb[bg])
            f = rgb[fg]
            if c == " ":
                continue
            if c == "█":
                d.rectangle([X, Y, X + cw - 1, Y + ch - 1], fill=f)
            elif c in "░▒":
                for py in range(ch):
                    for px in range(cw):
                        if c == "▒" and (px // scale + py // scale) % 2 == 0:
                            d.point((X + px, Y + py), fill=f)
                        if c == "░" and (px // scale) % 2 == 0 and (py // scale) % 4 == (px // scale // 2) % 2 * 2:
                            d.point((X + px, Y + py), fill=f)
            else:
                d.text((X, Y - scale), c, fill=f, font=font)
    img.save(out)
    return img.size


def stats(cells, meta):
    pairs = {}
    for row in cells:
        for c, fg, bg in row:
            pairs[(fg, bg)] = pairs.get((fg, bg), 0) + 1
    layers = {}
    for row in meta["layer"]:
        for l in row:
            layers[l] = layers.get(l, 0) + 1
    return pairs, layers


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "shapes":
        for name, text, paint in SHAPES:
            print(f"\n{name}: {len(text)} rows x {len(text[0])} cols")
            for t, p in zip(text, paint):
                print("   |" + t + "|   " + p + "|")
        sys.exit(0)
    if args and args[0] == "stats":
        W, H, seed = int(args[1]), int(args[2]), int(args[3])
        cells, meta = backdrop(W, H, seed)
        pairs, layers = stats(cells, meta)
        print(f"{W}x{H} seed {seed}: {len(pairs)} colour pairs (fg on bg)")
        for (fg, bg), n in sorted(pairs.items(), key=lambda kv: -kv[1]):
            print(f"   {fg} on {bg}: {n}")
        print("layers:", layers)
        L = meta["layout"]
        print("layout:", {k: v for k, v in L.items()})
        P = meta["profiles"]
        print("light from the", "left" if P["light"] < 0 else "right", "; main summit at column", P["x_main"],
              "; snowline", round(P["snowline"], 2))
        sys.exit(0)
    W, H, seed = int(args[0]), int(args[1]), int(args[2])
    mode = args[3] if len(args) > 3 else "text"
    # The cells are always made against the day palette; another palette only changes
    # the slots' RGB at render time, exactly as the console would on a palette swap.
    pal = PALETTES[args[5]] if len(args) > 5 else PALETTE_DAY
    cells, meta = backdrop(W, H, seed, PALETTE_DAY)
    if mode == "png":
        print(render_png(cells, pal, args[4]))
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        for line in rows_text(cells, mode):
            print(line)
