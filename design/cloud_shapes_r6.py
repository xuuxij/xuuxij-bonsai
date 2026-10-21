#!/usr/bin/env python3
"""Round 6: the tonal cloud set, made the way the landscape is ("paint, halftone"), in
three depths. A second set beside the line clouds (which stay as the black-sky set).

    python3 cloud_shapes_r6.py                 # every kind / size / variant / depth, text + paint
    python3 cloud_shapes_r6.py png OUT.png     # the same on #080808, ░ ▒ emulated
    python3 cloud_shapes_r6.py fade            # a near medium cumulus at fade 1.0, 0.66, 0.33

    cloud(kind, size, variant, depth, rng, light=-1) -> (text_rows, paint_rows)
        kind    cumulus | cirrus | lenticular | roll | mackerel | mist
        size    cumulus 0 1 2 (small medium large); cirrus 0 1 2; roll and mist: the width
                in columns; lenticular and mackerel: ignored
        variant "A" | "B" for cumulus (B is A with one hump grown, the breathing swap:
                draw both from the same rng state, see pair()); ignored otherwise
        depth   "far" | "mid" | "near" (aerial perspective: see DEPTHS)
        light   -1 the sun to the left (light from above-left), +1 to the right; pass the
                landscape's light side
    pair(size, depth, rng, light) -> ((textA, paintA), (textB, paintB))
    fade(text, paint, p) -> the cloud at fade p in [0, 1] (see THE FADE)

THE PAINT. Every cloud is a field over its cells: (coverage, brightness) at 4 x 4 sample
points per cell, the cell's value their mean product (the light the cloud sends from that
cell). A cumulus is a heap of half-ellipsoid domes on a flat base: one main dome to the
top row and 2-6 lesser ones stepping down either side, radii drawn from the rng, each
dome's outline pushed in and out by value noise (no two humps alike, no stamped
silhouette) and its edge fading over its outer third. Light: brightness = 0.10 + 0.90 *
(normal . light)^1.5 for a sun high to one side and a little in front, so the crown and
the lit shoulder go white, the front mid grey, the far side dark grey, and the base darkens
to a third over its last row. The lenticular is two flat lenses, lit evenly with a bright
top edge; the roll a row of low domes on a tube, capped at grey; the mackerel sky a brick
lattice of pea-sized domes with a fifth missing, the top row lit; cirrus are tapered
streaks along a hooked, drooping path, bright at the head, dimming and thinning to the
tail, lower strands set back and fainter; the mist straight-edged bands of thin light with
one brighter kirihaku dot in fourteen cells.

DEPTH (aerial perspective, as for the ranges): the far cloud's brightness is capped at 0.42
and nothing in it is solid (░ ▒ only, the thinner halftone), its edges softer; the mid
cloud is capped at 0.62 (solid only in c); the near cloud takes the full ladder (W█ crowns).

THE HALFTONE. Four tones over the near-black sky: W #fbfbf8 (Y 0.96), c #d2d2ce (0.64),
g #8c8c88 (0.26), d #4a4a48 (0.07). The ladder of a cell's mean light (blank, ░d .017,
▒d .034, ░g .065, ▒g .131, ░c .161, ░W .241, ▒c .321, ▒W .481, █c .643, █W .963; no █g
and █d, which would sit on top of ░W and ░g and put solid grey blocks among the dots). The
nearest step in lightness (Y^0.5) to the value plus the landscape's 8x8 Bayer offset
(amplitude 0.06), the matrix fixed to the shape's grid: the mountains' texture, a dotted
mass with a solid crown. No ink.

THE FADE. fade(text, paint, p) scales every cell's light by p and puts it back on the
ladder with the cell's own dither offset; dots thin and darken together, the crown goes
white -> c -> grey -> dots -> nothing. Replace the per-cell "moment" with this: p runs
0 -> 1 over the fade-in and 1 -> 0 over the fade-out (30-60 s as now); keep the head-first
order if wanted by p_cell = clamp(1.5 p - 0.5 f) with f the cell's share along the wind.
"""

import math
import random
import sys

TONES = {"W": "#fbfbf8", "c": "#d2d2ce", "g": "#8c8c88", "d": "#4a4a48"}
COVER = {"░": 0.25, "▒": 0.5, "█": 1.0}
BAYER8 = [[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
          [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
          [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
          [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]
DITHER = 0.06   # in lightness (Y^0.5)
SAMPLES = 4     # sample points per cell side

DEPTHS = {   # cap: brightness ceiling; solid: █ allowed; edge: the soft rim's share of a dome
    # Against mountains at 1 % light even a dim cloud is bright, so the far cap is low:
    # a far cloud peaks at ▒c / ░W dots, a mid one at █c, only a near one reaches █W.
    "far":  {"cap": 0.30, "solid": False, "edge": 0.45},
    "mid":  {"cap": 0.62, "solid": True,  "edge": 0.35},
    "near": {"cap": 1.00, "solid": True,  "edge": 0.30},
}


def luminance(hexs):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hexs[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


LUM = {k: luminance(v) for k, v in TONES.items()}
LADDER = sorted([(0.0, " ", " ")] + [(COVER[ch] * LUM[t], ch, t) for ch in COVER for t in TONES
                                     if not (ch == "█" and t in ("g", "d"))])
LADDER_SOFT = [s for s in LADDER if s[1] != "█"]


def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else hi if v > hi else v


def smoothstep(e0, e1, v):
    t = clamp((v - e0) / (e1 - e0)) if e1 != e0 else (1.0 if v >= e1 else 0.0)
    return t * t * (3 - 2 * t)


def quantize(value, x, y, solid=True):
    """The ladder step nearest the cell's value, dithered."""
    target = math.sqrt(max(0.0, value)) + (BAYER8[y % 8][x % 8] / 64.0 - 0.5) * 2 * DITHER
    ladder = LADDER if solid else LADDER_SOFT
    best = min(ladder, key=lambda s: abs(math.sqrt(s[0]) - target))
    return best[1], best[2]


def halftone(field, W, H, solid=True):
    """field(x, y) -> (coverage, brightness) at a point in cell units; returns rows."""
    text, paint = [], []
    for y in range(H):
        t, p = [], []
        for x in range(W):
            acc = 0.0
            for j in range(SAMPLES):
                for i in range(SAMPLES):
                    a, b = field(x + (i + 0.5) / SAMPLES, y + (j + 0.5) / SAMPLES)
                    acc += a * b
            ch, tone = quantize(acc / (SAMPLES * SAMPLES), x, y, solid)
            t.append(ch)
            p.append(tone)
        text.append("".join(t))
        paint.append("".join(p))
    return text, paint


class Noise:
    """Value noise on a lattice, from the cloud's rng."""

    def __init__(self, rng):
        self.grid, self.rng = {}, rng

    def _lat(self, i, j):
        v = self.grid.get((i, j))
        if v is None:
            v = self.grid[(i, j)] = self.rng.random()
        return v

    def at(self, x, y, px, py):
        u, v = x / px, y / py
        i, j = math.floor(u), math.floor(v)
        fu, fv = u - i, v - j
        fu = fu * fu * (3 - 2 * fu)
        fv = fv * fv * (3 - 2 * fv)
        a = self._lat(i, j) * (1 - fu) + self._lat(i + 1, j) * fu
        b = self._lat(i, j + 1) * (1 - fu) + self._lat(i + 1, j + 1) * fu
        return a * (1 - fv) + b * fv


# ---- the lit dome ---------------------------------------------------------------------------

def light_vector(light):
    """x right, y down, z toward the viewer: the sun high to one side, a little in front."""
    L = (0.55 * light, -0.60, 0.58)
    n = math.sqrt(sum(c * c for c in L))
    return tuple(c / n for c in L)


def domes_field(domes, base_y, light, noise, depth, cap_scale=1.0, base_dark=0.65, rough=0.22):
    """domes: (cx, cy, rx, ry) in cells, half-ellipsoids seen from the front, outlines
    roughened by noise; the flat base at row base_y. Returns field(x, y)."""
    L = light_vector(light)
    dp = DEPTHS[depth]
    cap = dp["cap"] * cap_scale

    def field(x, y):
        if y > base_y:
            return 0.0, 0.0
        best, bn = None, 9.0
        wobble = (noise.at(x, y, 2.6, 1.3) - 0.5) * 2 * rough
        for (cx, cy, rx, ry) in domes:
            u, v = (x - cx) / rx, (y - cy) / ry
            e = u * u + v * v + wobble * (0.6 + 0.4 * abs(u))
            if e < bn:
                bn, best = e, (u, v)
        if best is None or bn >= 1.0:
            return 0.0, 0.0
        u, v = best
        h = math.sqrt(max(0.0, 1.0 - bn))
        # the normal, in a space where a cell is twice as tall as it is wide
        nx, ny, nz = u, v * 2.0, h
        nn = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
        lit = clamp((nx * L[0] + ny * L[1] + nz * L[2]) / nn)
        b = 0.10 + 0.90 * lit ** 1.5
        b *= 0.88 + 0.24 * (noise.at(x * 1.7, y * 1.1, 3.0, 1.5) - 0.5)   # the body's grain
        b *= 1.0 - base_dark * smoothstep(base_y - 1.1, base_y + 0.05, y)
        a = smoothstep(1.0, 1.0 - dp["edge"], bn)
        return a, clamp(b) * cap
    return field


# ---- the kinds --------------------------------------------------------------------------

CUMULUS_SIZES = {0: (11, 2), 1: (23, 3), 2: (34, 4)}   # (cols, rows)


def cumulus_domes(size, rng):
    W, H = CUMULUS_SIZES[size]
    base = H - 0.12
    n = (3, 5, 7)[size]
    domes = []
    main_x = W * rng.uniform(0.36, 0.64)
    main_rx = W * (0.25, 0.17, 0.13)[size] * rng.uniform(0.9, 1.15)
    domes.append([main_x, base, main_rx, (H - 0.1) * rng.uniform(0.95, 1.0)])
    for i in range(n - 1):
        side = -1 if i % 2 == 0 else 1
        step = (i // 2 + 1)
        cx = main_x + side * (main_rx * rng.uniform(0.7, 1.1) + (step - 1) * W * rng.uniform(0.1, 0.16))
        cx = clamp(cx, W * 0.1, W * 0.9)
        ry = (H - 0.1) * rng.uniform(0.45, 0.8) / (1 + 0.25 * (step - 1))
        rx = W * rng.uniform(0.11, 0.19) / (1 + 0.15 * (step - 1))
        domes.append([cx, base, rx, ry])
    return domes, base, W, H


def cumulus(size, variant, depth, rng, light=-1):
    domes, base, W, H = cumulus_domes(size, rng)
    noise = Noise(random.Random(rng.random()))
    if variant == "B":   # one hump grown: the breathing swap
        k = 1 if len(domes) > 1 else 0
        domes[k][2] *= 1.25
        domes[k][3] = min(H - 0.1, domes[k][3] * 1.3)
    return halftone(domes_field(domes, base, light, noise, depth), W, H, DEPTHS[depth]["solid"])


def pair(size, depth, rng, light=-1):
    state = rng.getstate()
    a = cumulus(size, "A", depth, rng, light)
    rng.setstate(state)
    b = cumulus(size, "B", depth, rng, light)
    return a, b


CIRRUS_SIZES = {0: (16, 1), 1: (22, 3), 2: (29, 4)}


def cirrus(size, depth, rng, light=-1):
    """Streaks for a wind blowing left: the hooked head at the left, the strands trailing
    right and drooping; the lower strands set further back and fainter. Far by nature."""
    W, H = CIRRUS_SIZES[size]
    cap = DEPTHS[depth]["cap"]
    strands = []
    for k in range(H):
        x0 = 1 + k * (3 if size else 0) + rng.uniform(0, 1.5)
        length = max(6.0, (W - 2 - x0) * rng.uniform(0.8, 1.0) * (1.0 - 0.1 * k))
        strands.append((x0, k + 0.5, length, 1.0 - 0.2 * k))

    def field(x, y):
        a_best, b_best = 0.0, 0.0
        for (x0, y0, length, glow) in strands:
            t = (x - x0) / length
            if t < -0.05 or t > 1.05:
                continue
            tc = clamp(t)
            yc = y0 - 0.25 * math.sin(math.pi * tc * 0.5) + 0.4 * tc * tc   # hook, then droop
            w = 0.5 * (1.0 - 0.55 * tc) + 0.06
            a = smoothstep(w, w * 0.3, abs(y - yc)) * smoothstep(-0.05, 0.1, t)
            b = glow * ((1.0 - tc) ** 0.7 * 0.9 + 0.1)
            if a * b > a_best * b_best:
                a_best, b_best = a, b
        return a_best, b_best * cap
    return halftone(field, W, H, DEPTHS[depth]["solid"])


def lenticular(depth, rng, light=-1):
    W, H = 33, 3
    cx = W / 2 + rng.uniform(-1, 1)
    domes = [[cx, 2.3, W * 0.47, 2.1], [cx + rng.uniform(-2, 2), 1.05, W * 0.3, 1.0]]
    noise = Noise(random.Random(rng.random()))
    f = domes_field(domes, 2.88, light, noise, depth, base_dark=0.5, rough=0.08)
    return halftone(f, W, H, DEPTHS[depth]["solid"])


def roll(width, depth, rng, light=-1):
    """The stratocumulus roll: low domes in a row on a tube, grey only (capped at 0.7)."""
    W, H = max(34, min(58, width)), 2
    domes, x = [], rng.uniform(1.5, 3.5)
    while x < W - 1.5:
        rx = rng.uniform(2.6, 4.2)
        domes.append([x, 1.88, rx, rng.uniform(1.4, 1.9)])
        x += rx * rng.uniform(1.3, 1.7)
    noise = Noise(random.Random(rng.random()))
    f = domes_field(domes, 1.9, light, noise, depth, cap_scale=0.7, base_dark=0.6, rough=0.18)
    return halftone(f, W, H, DEPTHS[depth]["solid"])


def mackerel(depth, rng, light=-1):
    """A field of scales: tiny domes on a brick lattice (4 cols, rows offset 2), two or
    three rows, the outer rows shorter (a wedge), a fifth left out, the top row lit."""
    H = rng.randint(2, 3)
    units = rng.randint(8, 12)
    W = min(50, units * 4 + 4)
    cap = DEPTHS[depth]["cap"]
    domes = []
    for r in range(H):
        short = abs(r - (H - 1) / 2) * 2 + 1
        for u in range(units):
            cx = 2 + u * 4 + (2 if r % 2 else 0)
            if u < short / 2 - 0.5 or u > units - short / 2 - 0.5 or rng.random() < 0.2:
                continue
            domes.append([cx, r + 0.55, 1.6, 0.62, r])

    def field(x, y):
        a_best, b_best = 0.0, 0.0
        for (cx, cy, rx, ry, r) in domes:
            u, v = (x - cx) / rx, (y - cy) / ry
            e = u * u + v * v
            if e < 1:
                a = smoothstep(1.0, 0.55, e)
                b = (0.9 if r == 0 else 0.45) * (0.6 + 0.4 * (1 - e)) * (1.0 - 0.3 * clamp(-u * light))
                if a * b > a_best * b_best:
                    a_best, b_best = a, b
        return a_best, b_best * cap
    return halftone(field, W, H, DEPTHS[depth]["solid"])


def mist(width, depth, rng, light=-1):
    """Spear mist over the lake: three or four rows of straight-edged bands, each row's
    band its own length and offset, the ends tapered over six cells, a kirihaku dot one
    cell in fourteen. Thin light: ░ g with ▒ g in the middle, the dots ░ c."""
    W, H = max(40, min(80, width)), rng.randint(3, 4)
    bands = []
    for r in range(H):
        length = int(W * rng.uniform(0.45, 0.8))
        x0 = rng.randint(0, W - length)
        bands.append((x0, x0 + length, rng.uniform(0.09, 0.14)))
    dots = {(r, x) for r in range(H) for x in range(W) if rng.random() < 1 / 14}

    def field(x, y):
        r = int(y)
        if r >= H:
            return 0.0, 0.0
        x0, x1, b = bands[r]
        if x < x0 or x > x1:
            return 0.0, 0.0
        end = min(x - x0, x1 - x)
        if (r, int(x)) in dots:
            return 1.0, 0.17
        return smoothstep(-1, 6, end), b
    return halftone(field, W, H, solid=False)


def cloud(kind, size, variant, depth, rng, light=-1):
    if kind == "cumulus":
        return cumulus(size, variant, depth, rng, light)
    if kind == "cirrus":
        return cirrus(size, depth, rng, light)
    if kind == "lenticular":
        return lenticular(depth, rng, light)
    if kind == "roll":
        return roll(size, depth, rng, light)
    if kind == "mackerel":
        return mackerel(depth, rng, light)
    if kind == "mist":
        return mist(size, depth, rng, light)
    raise ValueError(kind)


# ---- the fade --------------------------------------------------------------------------

def fade(text, paint, p, solid=True):
    """The cloud at fade p: every cell's light scaled by p and put back on the ladder with
    the cell's own dither offset. Call it on the full cloud each step."""
    out_t, out_p = [], []
    for y, (row, prow) in enumerate(zip(text, paint)):
        t, pp = [], []
        for x, (ch, tone) in enumerate(zip(row, prow)):
            if ch == " ":
                c2, t2 = " ", " "
            else:
                c2, t2 = quantize(COVER[ch] * LUM[tone] * p, x, y, solid)
            t.append(c2)
            pp.append(t2)
        out_t.append("".join(t))
        out_p.append("".join(pp))
    return out_t, out_p


# ---- the catalogue --------------------------------------------------------------------------

def catalogue(seed=1, light=-1):
    rng = random.Random(seed)
    items = []
    names = ("small", "medium", "large")
    for depth, sizes in (("near", (1, 2)), ("mid", (0, 1)), ("far", (0,))):
        for size in sizes:
            (ta, pa), (tb, pb) = pair(size, depth, rng, light)
            items.append((f"cumulus {names[size]} A, {depth}", ta, pa))
            if depth == "near":
                items.append((f"cumulus {names[size]} B (breathed), {depth}", tb, pb))
    for size in (0, 1, 2):
        t, p = cirrus(size, "far", rng, light)
        items.append((f"cirrus {names[size]}, far (wind <-)", t, p))
    t, p = lenticular("mid", rng, light)
    items.append(("lenticular, mid", t, p))
    t, p = roll(44, "near", rng, light)
    items.append(("stratocumulus roll 44, near", t, p))
    t, p = mackerel("far", rng, light)
    items.append(("mackerel field, far", t, p))
    t, p = mist(66, "near", rng, light)
    items.append(("mist band 66", t, p))
    return items


def render(items, out, bg=(8, 8, 8)):
    from PIL import Image, ImageDraw
    cw, ch = 8, 16
    W = max(len(t[0]) for _n, t, _p in items) + 4
    H = sum(len(t) + 1 for _n, t, _p in items) + 1
    img = Image.new("RGB", (W * cw, H * ch), bg)
    d = ImageDraw.Draw(img)
    rgb = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in TONES.items()}
    y = 1
    for _n, t, p in items:
        for row, prow in zip(t, p):
            for x, (c, pt) in enumerate(zip(row, prow)):
                if c == " ":
                    continue
                f = rgb[pt]
                X, Y = (x + 2) * cw, y * ch
                if c == "█":
                    d.rectangle([X, Y, X + cw - 1, Y + ch - 1], fill=f)
                else:
                    for py in range(ch):
                        for px in range(cw):
                            if c == "▒" and (px + py) % 2 == 0:
                                d.point((X + px, Y + py), fill=f)
                            if c == "░" and px % 2 == 0 and py % 4 == (px // 2) % 2 * 2:
                                d.point((X + px, Y + py), fill=f)
            y += 1
        y += 1
    img.save(out)
    return img.size


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.stdout.reconfigure(encoding="utf-8")
    if args and args[0] == "png":
        print(render(catalogue(), args[1]))
        sys.exit(0)
    if args and args[0] == "fade":
        t, p = cumulus(1, "A", "near", random.Random(3))
        for f in (1.0, 0.66, 0.33):
            ft, fp = fade(t, p, f)
            print(f"\nfade {f}")
            for a, b in zip(ft, fp):
                print("   |" + a + "|   " + b + "|")
        sys.exit(0)
    print("ladder:", " ".join(f"{ch}{t}={lum:.3f}" for lum, ch, t in LADDER))
    for name, t, p in catalogue():
        print(f"\n--- {name} ({len(t)} rows x {len(t[0])} cols)")
        for a, b in zip(t, p):
            print("   |" + a + "|   " + b + "|")
