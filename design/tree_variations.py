#!/usr/bin/env python3
"""Specimens of the proposed tree variations for xuuxij-bonsai (see tree_variations.md).

Prints, as plain text with a paint map beside it:
  1. every foliage style as one pad over the same sample twig (a primary of 16 cells with
     one secondary), paint letters: L lit leaf (bold green, slot 10), l shaded leaf
     (slot 2), u underside (black fg), e edge (slot 2), A accent (a bloom in bold red 9,
     a bud in rosewood 1, a fruit in gold 11), w wood;
  2. every bark style as a trunk section 9 wide tapering to 3 over 14 rows with two
     movements, paint letters: b bark edge (slot 3 on the backdrop), k ink inside (slot 3
     on black), v the hollow's void (blank on black), d deadwood (slot 7 on black), j jin
     (slot 7 on the backdrop), r root/nebari;
  3. the FORMS-table entries for the new forms, the foliage and bark tables, as dicts.

The shape rules here are the ones tree_variations.md specifies, written the way
fill_pad / make_trunk do it, so they can be lifted into the program.
Run: python3 tree_variations.py [seed]
"""
import math
import random
import sys

LEAFINESS = 1.1          # the program's default
SCALE = 1.0              # a full-size tree (R >= 60 rows)

# ---------------------------------------------------------------------------------------
# 1. FOLIAGE
# ---------------------------------------------------------------------------------------

# name -> the numbers. "inside" / "edge" / "seam" are the character sets; "ry" is the
# pad's height rule from rx (the present one is rx/3.5 + 1); "lit" the share of each
# column's dome height that is lit from the top (or "row" = the top row of each tier /
# column); "edge_at" the normalised distance where feathering starts (0.8 now); "hole"
# the chance an inside cell is left empty; "under" whether the bottom row is the black
# underside; "accent" = (char set, where, share, slot).
FOLIAGE = {
    "cloud": {   # the present pad, unchanged: the broadleaf cloud
        "inside": ("&*", 75, "*^", 25), "edge": ".,'", "rx": 1.0, "ry": "rx/3.5+1", "lit": 0.40,
        "edge_at": 0.8, "hole": 0.0, "under": True, "autumn": "as set (yellow red)",
        "forms": "all", "weight": 40},
    "pine": {    # needle tiers: pads in strata of two rows with a dark seam between
        "inside": "^^*", "edge": "'.", "seam": ".^", "rx": 1.0, "ry": "max(4, rx/3.5+1)",
        "lit": "tier top row", "edge_at": 0.8, "hole": 0.0, "under": True, "autumn": "yellow",
        "forms": "chokkan shakan bunjin kengai fukinagashi hankengai moyogi", "weight": 18},
    "juniper": { # flat lozenge pads, two twigs a branch, a dense scaly mass
        "inside": "%&", "edge": ".,", "rx": 1.15, "ry": "max(2, rx/5+1)", "lit": 0.35,
        "edge_at": 0.78, "hole": 0.0, "under": True, "twigs": 2, "autumn": "yellow",
        "forms": "moyogi shakan bunjin kengai fukinagashi hankengai", "weight": 14},
    "elm": {     # fine small leaves: a taller, rounder dome of tiny marks
        "inside": ":;\":;*", "edge": ".,", "rx": 1.0, "ry": "rx/2.5+1", "lit": 0.40,
        "edge_at": 0.8, "hole": 0.05, "under": True, "autumn": "as set (yellow red)",
        "forms": "hokidachi moyogi chokkan kabudachi neagari", "weight": 8},
    "willow": {  # a thin cap on the branch and strands hanging below it
        "inside": "&*", "edge": ".,'", "strand": "|||;:", "cap_rx": "0.3 len + 3", "cap_ry": 3, "cap_at": 0.85, "twigs": 0,
        "strand_len": "3 + 7 t (+0..2), t = share along the branch, from t = 0.25, every 2nd column, starting under the cap",
        "lit": "top 2 cells of a strand, cap top row", "under": False, "autumn": "yellow",
        "forms": "moyogi shakan kabudachi", "weight": 5},
    "tuft": {    # sparse literati tufts: small, airy, holes in the mass, no underside
        "inside": "^^*'", "edge": "'.", "rx": 1.0, "ry": "min(ry, 3)", "lit": "top row of each column",
        "edge_at": 0.75, "hole": 0.20, "under": False, "autumn": "yellow",
        "forms": "bunjin fukinagashi neagari hankengai", "weight": 6},
    "azalea": {  # the cloud in bloom: blooms over the top 60 %, a few buds
        "inside": "&*", "edge": ".,'", "rx": 1.0, "ry": "rx/3.5+1", "lit": 0.40, "edge_at": 0.8,
        "hole": 0.0, "under": True, "accent": (("@", "bloom", 0.18, "bold red 9"), ("o", "bud", 0.05, "rosewood 1")),
        "autumn": "blooms fall first, then as set", "forms": "moyogi shakan kabudachi neagari", "weight": 5},
    "fruit": {   # the cloud with fruit hanging in its lower 60 %
        "inside": "&*", "edge": ".,'", "rx": 1.0, "ry": "rx/3.5+1", "lit": 0.40, "edge_at": 0.8,
        "hole": 0.0, "under": True, "accent": (("o", "fruit", 0.07, "gold 11"),),
        "autumn": "leaves as set, the fruit last", "forms": "moyogi chokkan shakan kabudachi", "weight": 4},
}


def sample_twig():
    """A primary of 16 cells (curve profile: a dip, then rising) and a secondary of 5
    rising steeply from its ninth cell; (y, x, glyph), the way plan_branch makes them."""
    primary = []
    y, x = 12, 0
    dys = [0, 0, 1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, -1]
    for j, dy in enumerate(dys):
        y += dy
        x = j
        glyph = "~" if dy == 0 else ("/" if dy < 0 else "\\")
        primary.append((y, x, glyph))
    jy, jx, _g = primary[9]
    secondary = []
    y, x = jy - 1, jx + 1
    for j in range(5):
        secondary.append((y, x, "/"))
        y, x = y - 1, x + 1
    return primary, secondary


def pad_radii(twig, style):
    """The pad's radii for a primary, as pad_radii does it (by_branch), then the style's rules."""
    n = len(twig)
    rx = max(3, int(round((0.5 * n + 4) * LEAFINESS)))
    ry = max(2, int(round(rx / 3.5)) + 1)
    return style_radii(rx, ry, style)


def style_radii(rx, ry, style):
    if style == "pine":
        return rx, max(4, ry)
    if style == "juniper":
        rx = int(round(rx * 1.15))
        return rx, max(2, int(round(rx / 5)) + 1)
    if style == "elm":
        return rx, int(round(rx / 2.5)) + 1
    if style == "tuft":
        return rx, min(ry, 3)
    return rx, ry


def cloud_of(twig, rx, ry, at=0.70):
    cy, cx = twig[int(len(twig) * at)][:2]
    return (twig, rx, ry, cy, cx)


def dome_union(members):
    """(y, x) -> (d, rx, ry, cy, cx): every cell inside the union of the flat-bottomed
    domes, each by its nearest dome; as fill_pad computes it."""
    out = {}
    y0 = min(cy + 1 - ry for _t, rx, ry, cy, cx in members)
    y1 = max(cy + 1 for _t, rx, ry, cy, cx in members)
    x0 = min(cx - rx for _t, rx, ry, cy, cx in members)
    x1 = max(cx + rx for _t, rx, ry, cy, cx in members)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            best = None
            for _t, rx, ry, cy, cx in members:
                if cy + 1 - ry <= y <= cy + 1:
                    d = math.hypot((x - cx) / rx, (cy + 1 - y) / ry)
                    if best is None or d < best[0]:
                        best = (d, rx, ry, cy, cx)
            if best is not None and best[0] <= 1:
                out[(y, x)] = best
    return out


def column_top(y, x, d_info):
    _d, rx, ry, cy, cx = d_info
    dxn = (x - cx) / rx
    y_top = cy + 1 - ry * math.sqrt(max(0.0, 1 - dxn * dxn))
    return y_top, cy + 1 - y_top


def pick(rng, chars):
    return rng.choice(chars)


def fill(style, members, wood, rng):
    """One pad of `style` over the family `members`; returns (y, x) -> (char, paint)."""
    spec = FOLIAGE[style]
    dome = dome_union(members)
    cover = {c for c in wood}  # the family's own twigs may be covered (as fill_pad's cover)
    bottom = max(cy + 1 for _t, rx, ry, cy, cx in members)
    edge_at = spec.get("edge_at", 0.8)
    inside = spec["inside"]
    if style == "cloud":
        inside = "&*"  # the specimen shows the broadleaf set; the needle set *^ is drawn 25 % of the time
    out = {}
    for (y, x), info in dome.items():
        d = info[0]
        if (y, x) in wood and (y, x) not in cover:
            continue
        if (y, x) not in wood and rng.random() > (1.0 if d < edge_at else (1 - d) / (1 - edge_at)):
            continue
        edge = d > edge_at
        y_top, h = column_top(y, x, info)
        if edge:
            out[(y, x)] = (pick(rng, spec["edge"]), "e")
            continue
        if spec.get("hole") and rng.random() < spec["hole"] and (y, x) not in wood:
            continue
        if style == "pine":
            r = bottom - y                  # 0 = the lowest row
            above = (y - 1, x) in dome and dome[(y - 1, x)][0] <= edge_at
            k = r % 3                       # 0 seam, 1 shaded, 2 lit
            if not above:
                out[(y, x)] = (pick(rng, inside), "L")      # the top of a column is always lit
            elif k == 0:
                out[(y, x)] = (pick(rng, spec["seam"]), "u")  # the seam: a dark line under each tier
            elif k == 1:
                out[(y, x)] = (pick(rng, inside), "l")
            else:
                out[(y, x)] = (pick(rng, inside), "L")
            if y == bottom:
                out[(y, x)] = (pick(rng, inside), "u")      # the underside, as now
            continue
        if style == "tuft":
            lit = y < y_top + 1.0
            out[(y, x)] = (pick(rng, inside), "L" if lit else "l")
            continue
        lit = y < y_top + spec["lit"] * h
        tone = "L" if lit else "l"
        if spec.get("under") and y == bottom:
            tone = "u"
        char = pick(rng, inside)
        if spec.get("accent") and tone != "u":
            for a_char, what, share, _slot in spec["accent"]:
                in_zone = (y < y_top + 0.6 * h) if what in ("bloom", "bud") else (y >= y_top + 0.4 * h)
                if in_zone and rng.random() < share:
                    char, tone = a_char, "A"
                    break
        out[(y, x)] = (char, tone)
    # no specks: a row of fewer than four cells covering no wood goes (as fill_pad)
    by_row = {}
    for (y, x) in out:
        by_row.setdefault(y, []).append(x)
    for y, xs in by_row.items():
        if len(xs) < 4 and not any((y, x) in cover for x in xs):
            for x in xs:
                del out[(y, x)]
    return out


def fill_willow(members, primary, wood, rng):
    """The willow: a cap over the branch's end and strands hanging from the branch, the
    ones under the cap starting below it."""
    spec = FOLIAGE["willow"]
    twig = primary
    n = len(twig)
    cap_rx, cap_ry = int(round(0.3 * n + 3)), 3
    cy, cx = twig[int(n * 0.85)][:2]
    dome = dome_union([(twig, cap_rx, cap_ry, cy, cx)])
    out = {}
    for (y, x), info in dome.items():
        d = info[0]
        if (y, x) not in wood and d > 0.8 and rng.random() > (1 - d) / 0.2:
            continue
        y_top, h = column_top(y, x, info)
        if d > 0.8:
            out[(y, x)] = (pick(rng, spec["edge"]), "e")
        else:
            out[(y, x)] = (pick(rng, spec["inside"]), "L" if y < y_top + 1.0 else "l")
    strand_chars = spec["strand"]
    for j, (y, x, _g) in enumerate(twig):
        t = j / (n - 1)
        if t < 0.25 or j % 2:
            continue
        length = int(round(3 + 7 * t)) + rng.randint(0, 2)
        k, yy = 0, y + 1
        while k < length:
            cell = (yy, x)
            yy += 1
            if cell in out and out[cell][1] != "e":
                continue  # under the cap: the strand begins below it
            if cell in wood:
                break
            if k < 2:
                out[cell] = ("|", "L")
            elif k == length - 1:
                out[cell] = (rng.choice(",'"), "l")
            else:
                out[cell] = (pick(rng, strand_chars), "l")
            k += 1
    return out


def show(title, note, cells, wood, paint_wood=True):
    """Prints the text and its paint side by side."""
    ys = [y for y, _x in list(cells) + list(wood)]
    xs = [x for _y, x in list(cells) + list(wood)]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    width = x1 - x0 + 1
    print(f"--- {title}")
    if note:
        print(f"    {note}")
    for y in range(y0, y1 + 1):
        text, paint = [], []
        for x in range(x0, x1 + 1):
            if (y, x) in cells:
                c, p = cells[(y, x)]
                text.append(c)
                paint.append(p)
            elif (y, x) in wood:
                text.append(wood[(y, x)])
                paint.append("w" if paint_wood else wood[(y, x)])
            else:
                text.append(" ")
                paint.append(" ")
        print("    " + "".join(text).ljust(width) + "   |   " + "".join(paint))
    print()


def foliage_specimens(rng):
    primary, secondary = sample_twig()
    wood = {(y, x): g for y, x, g in primary + secondary}
    print("=" * 100)
    print("FOLIAGE: one pad of each style over the same family (a primary of 16, a secondary of 5)")
    print("paint: L lit (bold green)  l shaded (green)  u underside/seam (black)  e edge  A accent  w wood")
    print("=" * 100)
    print()
    show("the bare family (as plan_branch draws it)", "", {}, wood)
    for style in FOLIAGE:
        spec = FOLIAGE[style]
        if style == "willow":
            cells = fill_willow([], primary, wood, rng)
            show("willow", "a 3-row cap over the branch's end (at 0.85); strands every 2nd column from "
                 "t = 0.25, 3 + 7 t rows long, those under the cap starting below it; no secondary; "
                 "the branch itself takes the drooping profile", cells, wood)
            continue
        rx, ry = pad_radii(primary, style)
        members = [cloud_of(primary, rx, ry)]
        srx, sry = style_radii(max(3, round(8 * LEAFINESS)), max(2, round(4 * LEAFINESS)), style)
        members.append(cloud_of(secondary, srx, sry))
        extra = {}
        if spec.get("twigs") == 2:  # the juniper's second twig, at 0.35 of the primary
            jy, jx, _g = primary[5]
            second = [(jy - 1 - k, jx + 1 + k, "/") for k in range(4)]
            extra = {(y, x): g for y, x, g in second}
            members.append(cloud_of(second, srx, sry))
        cells = fill(style, members, {**wood, **extra}, rng)
        note = (f"rx {rx} ry {ry} (secondary {srx} x {sry}); inside {spec['inside']!r} edge {spec['edge']!r}"
                + (f" seam {spec['seam']!r}" if "seam" in spec else "")
                + f"; autumn: {spec['autumn']}")
        show(style, note, cells, {**wood, **extra})


# ---------------------------------------------------------------------------------------
# 2. BARK (the trunk and the branches' wood)
# ---------------------------------------------------------------------------------------

BARK = {
    "smooth": {  # the present trunk, unchanged
        "edges": "| / \\", "core": "|", "branches": "line: ~ / \\, primaries 2 rows thick for 40 %",
        "forms": "all", "foliage": "all", "weight": 45},
    "plated": {  # old black pine: plates two rows tall, three cells wide, in a brick bond
        "edges": "| / \\", "core": "| and _ in a brick bond", "branches": "heavy: 2 rows thick for 70 %, "
        "secondaries 2 rows for 30 %", "forms": "chokkan moyogi shakan hankengai", "foliage": "pine cloud",
        "weight": 15},
    "twisted": { # juniper, literati: round edges ( ), the grain following each movement
        "edges": "( ) on straight rows, / \\ where it moves", "core": "| with a ( drifting one column a row; "
        "the diagonal across the whole row where it moves", "branches": "line", "forms": "bunjin shakan "
        "kengai hankengai fukinagashi", "foliage": "juniper pine tuft", "weight": 15},
    "rough": {   # old elm, trident maple: flaking mottled bark, a knothole (uro)
        "edges": "{ } on straight rows, / \\ where it moves", "core": "| 78 %, % 12 %, : 10 %; one () knothole",
        "branches": "knuckled: a jog of one row every 3 to 5 cells, _ after a dip", "forms": "moyogi chokkan "
        "hokidachi kabudachi neagari", "foliage": "elm cloud azalea fruit", "weight": 12},
    "hollow": {  # sabamiki: the trunk split open, a black void with bark rims
        "edges": "| / \\", "core": "( void ) from 10 % to 45 % of R where the trunk is 5 or wider; "
        "the lip rows ' and .", "branches": "knuckled", "forms": "moyogi chokkan kabudachi hokidachi",
        "foliage": "elm cloud fruit", "weight": 6},
    "deadwood": {  # an overlay, not a bark: a shari strip up the trunk and a jin or two
        "shari": "slot 7 on black, 3 cells at the base to 1 at 55-75 % of R, on the outside of the first curve",
        "jin": "a 3 to 6 cell dead branch - ~ - ' in slot 7; a top jin | ' above a literati's apex",
        "over": "smooth twisted plated", "foliage": "pine juniper tuft", "forms": "bunjin shakan fukinagashi "
        "kengai hankengai chokkan", "chance": "by form (0.25 to 0.6)"},
}


def trunk_rows(w0=9, w_end=3, n=14):
    """Width per row, bottom first: w = w_end + (w0 - w_end) (1 - t)^1.15 (the program's taper
    shape, ending at 3 instead of 1 so the section shows every width)."""
    dxs = [0, 0, 0, 1, 1, 1, 0, 0, -1, -1, 0, 0, 0, 0]
    xs, x = [], 10
    for dx in dxs:
        xs.append(x)
        x += dx
    rows = []
    for i in range(n):
        t = i / (n - 1)
        w = max(1, int(round(w_end + (w0 - w_end) * (1 - t) ** 1.15)))
        dx = xs[i + 1] - xs[i] if i + 1 < n else 0
        rows.append((i, xs[i], w, dx))
    return rows


def bark_specimen(style, rng, deadwood=False):
    """Text and paint of a trunk section in `style`; returns (y, x) -> (char, paint)."""
    cells = {}
    rows = trunk_rows()
    n = len(rows)
    uro_row = 5
    for i, x, w, dx in rows:
        y = n - 1 - i  # printed top down
        straight = dx == 0 or i < 2
        diag = "/" if dx > 0 else "\\"
        if style == "twisted":
            edge_l = edge_r = ("(" if straight else diag)
            if straight:
                edge_l, edge_r = "(", ")"
        elif style == "rough":
            edge_l, edge_r = ("{", "}") if straight else (diag, diag)
        else:
            edge_l = edge_r = "|" if straight else diag
        core = []
        for k in range(max(0, w - 2)):
            if style == "plated":
                core.append("|" if (k + i // 2) % 3 == 0 else "_")
            elif style == "twisted":
                if not straight:
                    core.append(diag)
                else:
                    core.append("(" if (k - i) % 4 == 0 else "|")
            elif style == "rough":
                r = rng.random()
                core.append("|" if r < 0.78 else ("%" if r < 0.90 else ":"))
            else:
                core.append("|")
        paint = ["k"] * len(core)
        if style == "hollow" and w >= 5:
            if 2 <= i <= 7:                      # the void: 10 % to 45 % of R on a real trunk
                core = ["("] + [" "] * (w - 4) + [")"]
                paint = ["k"] + ["v"] * (w - 4) + ["k"]
            elif i == 8:                          # the lip above the void
                core = ["'"] * (w - 2)
            elif i == 1:
                core = ["."] * (w - 2)
        if style == "rough" and i == uro_row and w >= 6:
            core[2:4] = ["(", ")"]                # a knothole (uro)
        if deadwood:                              # the shari strip: 3 at the base, 1 by 70 % up
            strip = 2 if i < 3 else (1 if i < 6 else 0)   # core cells; with the edge: 3, 2, then the edge alone
            for k in range(min(strip, len(core))):
                core[k] = "|" if straight else diag
                paint[k] = "d"
        text = edge_l + "".join(core) + edge_r if w >= 3 else (edge_l if w == 1 else edge_l + edge_r)
        pnt = "b" + "".join(paint) + "b" if w >= 3 else ("b" if w == 1 else "bb")
        if deadwood and i < 10 and w >= 3:
            pnt = "d" + pnt[1:]                   # the strip runs down the edge too, at the base
        x0 = x - w // 2
        if i == 0:                                # nebari roots on the first row
            text, pnt, x0 = "__/" + text + "\\__", "rrr" + pnt + "rrr", x0 - 3
        for k, ch in enumerate(text):
            cells[(y, x0 + k)] = (ch, pnt[k])
    if deadwood:
        # a jin: a dead branch leaving the right edge at row 9 (65 % up), its tip raised
        i = 9
        _i, x, w, _dx = rows[i]
        y = n - 1 - i
        for k, ch in enumerate("-~-'"):
            cells[(y - (1 if k == 3 else 0), x - w // 2 + w + k)] = (ch, "j")
        # a top jin: the trunk's dead leader above the apex
        _i, x, w, _dx = rows[-1]
        cells[(-1, x)] = ("|", "j")
        cells[(-2, x)] = ("'", "j")
    return cells


def bark_specimens(rng):
    print("=" * 100)
    print("BARK: a trunk section 9 wide tapering to 3 over 14 rows, two movements (right, then left)")
    print("paint: b bark edge  k ink inside (slot 3 on black)  v void (black)  d deadwood (slot 7 on black)"
          "  j jin (slot 7)  r nebari")
    print("=" * 100)
    print()
    for style in ("smooth", "plated", "twisted", "rough", "hollow"):
        spec = BARK[style]
        cells = bark_specimen(style, rng)
        show(style, f"edges {spec['edges']}; core {spec['core']}; branches {spec['branches']}",
             cells, {}, paint_wood=False)
    cells = bark_specimen("twisted", rng, deadwood=True)
    show("deadwood over twisted (shari + jin + top jin)",
         "the strip 3 cells at the base thinning to 1 by 70 % up, on the first curve's outside; "
         "a jin at 65 %; a dead leader above the apex", cells, {}, paint_wood=False)
    cells = bark_specimen("smooth", rng, deadwood=True)
    show("deadwood over smooth (a pine's shari)", "", cells, {}, paint_wood=False)


# ---------------------------------------------------------------------------------------
# 2b. BRANCH PROFILES
# ---------------------------------------------------------------------------------------

def branch(profile, length=18, side=1, rng=None, thick_share=0.4, knuckle=False):
    """A branch of `length` cells by profile, the glyph by its slope as plan_branch does
    (~ level, / rising, \\ falling, for a branch going right); the first `thick_share`
    two rows thick (the under row _ for ~, else the glyph); `knuckle` jogs a row every
    3 to 5 cells. Returns (y, x) -> glyph, y = 0 at the start, up is negative."""
    rng = rng or random.Random(1)
    cells, y, x = [], 0, 0
    acc, level_run, next_jog = 0.0, 0, rng.randint(3, 5)
    for j in range(length):
        dy = 0
        if j:
            if profile == "curve":
                s0, s1 = -1 / 4.0, 1 / 2.2
                slope = s0 + (s1 - s0) * j / (length - 1)
                cap = 5 if abs(slope) < 0.1 else 3
            elif profile == "wind":      # level, lifting a row every 8 cells, the tip dropping one
                slope, cap = 1 / 8.0, 8
            elif profile == "droop":     # level for 60 %, then falling a row every 3 cells
                slope = 0.0 if j < 0.6 * length else -1 / 3.0
                cap = 10 ** 6
            elif profile == "fan":       # the broom's: steep from the first cell
                slope, cap = 1 / 1.4, 10 ** 6
            else:                        # chokkan: level, then rising at the end
                slope = 0.0 if j < 0.6 * length else 1 / 5.0
                cap = 10 ** 6
            acc += slope
            if profile == "wind" and j == int(0.85 * length):
                dy, acc = 1, 0.0             # the one forced step: the tip drops a row
            elif knuckle and j == next_jog:
                dy = rng.choice((-1, 1))
                next_jog = j + rng.randint(3, 5)
            elif acc >= 1:
                acc, dy = acc - 1, -1
            elif acc <= -1:
                acc, dy = acc + 1, 1
            elif level_run >= cap:
                acc, dy = max(acc - 1, -0.5), -1
            y, x = y + dy, x + side
        level_run = level_run + 1 if dy == 0 else 0
        glyph = "~" if dy == 0 else ("/" if (side > 0) == (dy < 0) else "\\")
        cells.append((y, x, glyph, dy))
    out = {(y, x): g for y, x, g, _dy in cells}
    if knuckle:  # after a dip the next level cell is _: the branch sags into the jog
        for j in range(1, len(cells)):
            y, x, g, _dy = cells[j]
            if cells[j - 1][3] == 1 and g == "~":
                out[(y, x)] = "_"
    for j, (y, x, g, _dy) in enumerate(cells):
        if j < thick_share * length and (y + 1, x) not in out:
            out[(y + 1, x)] = "_" if g in "~_" else g
    return out


def branch_specimens():
    print("=" * 100)
    print("BRANCHES: one primary of 18 cells per profile, going right; wood only")
    print("=" * 100)
    print()
    for title, kw in (
            ("line: the present curve profile, 2 rows thick for 40 % (smooth, twisted bark)", dict(profile="curve")),
            ("heavy: the same, 2 rows thick for 70 % (plated bark)", dict(profile="curve", thick_share=0.7)),
            ("knuckled: a jog of a row every 3 to 5 cells, _ after a dip (rough, hollow bark)",
             dict(profile="chokkan", knuckle=True)),
            ("drooping: level for 60 %, then a row down every 3 cells (willow; pine on chokkan)", dict(profile="droop")),
            ("wind: level, a row up every 8 cells, the tip drops one (fukinagashi)", dict(profile="wind", length=26)),
            ("fan: steep from the first cell (hokidachi; the fan below)", dict(profile="fan", length=10, thick_share=0.3))):
        cells = branch(rng=random.Random(3), **kw)
        ys = [y for y, _x in cells]
        xs = [x for _y, x in cells]
        print(f"--- {title}")
        for y in range(min(ys), max(ys) + 1):
            print("    " + "".join(cells.get((y, x), " ") for x in range(min(xs), max(xs) + 1)))
        print()
    print("--- the broom's fan: 5 branches from the trunk's top; slopes 1 row per 0.6 (centre), 1.0, 2.2 columns (sides); "
          "each forks at 45 % and 70 %")
    fan = {}
    for side, run in ((-1, 2.2), (-1, 1.0), (0, 0.6), (1, 1.0), (1, 2.2)):
        y, x, acc = 0, 0, 0.0
        for j in range(12):
            if side == 0:
                y -= 1
                fan[(y, x)] = "|"
                continue
            if j:
                acc += 1 / run
                dy = -1 if acc >= 1 else 0
                acc = acc - 1 if acc >= 1 else acc
                y, x = y + dy, x + side
            fan[(y, x)] = "/" if side > 0 else "\\"
    ys = [y for y, _x in fan]
    xs = [x for _y, x in fan]
    for y in range(min(ys), max(ys) + 1):
        print("    " + "".join(fan.get((y, x), " ") for x in range(min(xs), max(xs) + 1)))
    pad = " " * (-min(xs) - 1)
    print("    " + pad + "|||")
    print("    " + pad + "|||")
    print()


# ---------------------------------------------------------------------------------------
# 3. NEW FORMS, as FORMS-table entries
# ---------------------------------------------------------------------------------------

NEW_FORMS = {
    "fukinagashi": {  # windswept: a steeper slant, every branch streaming to the lee
        "height": (0.42, 0.50), "spread": (0.65, 0.80), "trunk_width": ("by_height", 8.0, 6, 8),
        "line": "lean", "lean": (1.00, 1.40), "bow": (2, 4),
        "branches": (3, 4), "first_branch": (0.35, 0.45),
        "first_side": "with",              # NEW value: the lean's own side (the lee)
        "sides": "lee",                    # NEW key: every branch on the first side, no alternation
        "profile": "wind",                 # NEW profile: level, lifting a row every 8 cells, the last 15 % dropping one row
        "branch_length": "by_spread", "length_taper": 0.10,   # NEW key: the upper branches shorten by 10 % a step (17 % now)
        "twigs": 1, "pads": ((9, 13), (2, 3)), "apex_pad": 0.7, "back_pad": False,
        "planting": (0.30, "away_from_lean"), "roots": "lean",
        "foliage": {"pine": 45, "juniper": 30, "tuft": 25},
        "bark": {"twisted": 50, "smooth": 30, "plated": 20},
        "deadwood": 0.6,                   # NEW key: chance of a jin stub on the windward side
        "pot": "oval", "stand": "auto", "weight": 8,
    },
    "hokidachi": {    # broom: a short straight trunk, a fan of fine branches, one rounded crown
        "height": (0.50, 0.58), "spread": (0.60, 0.72), "trunk_width": ("by_height", 7.0, 7, 9),
        "line": "straight", "movement": 0, "apex": 0,
        "trunk_top": (0.30, 0.38),         # NEW key: the trunk ends at this share of R; the fan leaves its top
        "branches": (5, 7), "first_branch": None,
        "sides": "fan",                    # NEW: the branches leave the trunk's top row, spread across it
        "profile": "fan",                  # NEW profile: rises 1 row per 0.6 columns at the centre to 1 per 2.2 at the sides
        "branch_length": "by_height", "fan_height": (0.55, 0.65),   # NEW: rows climbed, of R - trunk_top
        "twigs": 2,                        # each fan branch forks at 45 % and 70 %, twig profile fan
        "pads": "crown",                   # NEW: one dome over the fan: base at 0.55 of the fan's height,
                                           #      rx = half the fan's width + 2, ry = 0.5 (R - top)
        "apex_pad": 0.0, "back_pad": False,
        "planting": (0.50, "left"), "roots": ("__/", "\\__"),
        "foliage": {"elm": 55, "cloud": 45},
        "bark": {"rough": 50, "smooth": 35, "hollow": 15},
        "pot": "oval", "stand": "auto", "weight": 8,
    },
    "kabudachi": {    # clump: three trunks from one base, the thickest the tallest, one canopy
        "height": (0.50, 0.60), "spread": (0.70, 0.85), "trunk_width": ("by_height", 8.0, 6, 8),
        "line": "s-curve", "movement": (4, 8), "apex": (-3, 3),
        "branches": (2, 3), "first_branch": 0.45, "first_side": "outside", "profile": "curve",
        "branch_length": "by_spread", "twigs": 1, "pads": "by_branch", "apex_pad": 1.0, "back_pad": False,
        "trunks": (                        # NEW key: the other trunks, forking 1 to 2 rows up:
            ((0.62, 0.72), "opposite_first_curve", 0.70, (8, 12)),   # (height share of R, side, width share of w0, lean columns)
            ((0.42, 0.52), "first_curve", 0.55, (10, 14)),
        ),
        "trunk_branches": (1, 2),          # NEW key: primaries per extra trunk, on its outer side, each with a pad
        "planting": (0.50, "left"), "roots": ("___/", "\\___"),
        "foliage": {"cloud": 40, "elm": 25, "pine": 20, "azalea": 15},
        "bark": {"smooth": 50, "rough": 35, "hollow": 15},
        "pot": "oval", "stand": "auto", "weight": 6,
    },
    "neagari": {      # exposed root: the trunk stands on bare root legs
        "height": (0.58, 0.68), "spread": (0.40, 0.55), "trunk_width": ("drawn", 4, 6),
        "line": "s-curve", "movement": (6, 10), "apex": (-4, 8),
        "branches": (2, 3), "first_branch": (0.55, 0.62), "first_side": "outside", "profile": "curve",
        "branch_length": (10, 16), "twigs": 1, "pads": "by_branch", "apex_pad": 1.0, "back_pad": False,
        "roots": "stilts",                 # NEW value: legs instead of a nebari row
        "root_height": (0.25, 0.35),       # NEW key: share of R the legs take; the trunk's line starts above them
        "root_legs": (3, 4),               # NEW key: legs 2 cells wide at the top, 1 at the soil, splayed to +-(w0 + 3) columns
        "planting": (0.50, "left"),
        "foliage": {"azalea": 30, "elm": 30, "cloud": 25, "tuft": 15},
        "bark": {"smooth": 60, "rough": 40},
        "rock": 0.3,                       # NEW key: chance the legs clasp a rock (sekijoju): ▒ in slot 8 on black between them
        "pot": "drum", "stand": "auto", "weight": 5,
    },
    "hankengai": {    # semi-cascade: its own planner, like kengai; the fall stays above the pot's base
        "rise": (10, 14), "crown": ((8, 10), (3, 4)),
        "out": (22, 30),                   # columns the trunk runs out past the rim
        "drop": (6, 10),                   # rows it falls below the rim; clamped to the pot's body rows - 1
        "thick": (3, 0.5, 2, 0.8),         # 3 rows thick for the first 50 % of the run, 2 to 80 %, then 1
        "fall_branches": (2, 3), "fall_pads": ((7, 10), (2, 3)),
        "trunk_width": 5, "planting": 0.35,
        "foliage": {"pine": 35, "juniper": 35, "cloud": 20, "tuft": 10},
        "bark": {"twisted": 45, "smooth": 35, "plated": 20},
        "deadwood": 0.4,
        "pot": "hexagon", "stand": "stand", "weight": 8,   # the hexagon on the normal stand, not the cascade stand
    },
}

STYLE_WEIGHTS = "moyogi:15 chokkan:10 shakan:30 bunjin:30 kengai:15 fukinagashi:8 hokidachi:8 kabudachi:6 neagari:5 hankengai:8"

# form -> foliage weights (the existing forms); a new form carries its own above.
FOLIAGE_BY_FORM = {
    "moyogi":  {"cloud": 45, "pine": 15, "juniper": 10, "elm": 10, "willow": 6, "azalea": 8, "fruit": 6},
    "chokkan": {"cloud": 35, "pine": 40, "elm": 15, "fruit": 10},
    "shakan":  {"cloud": 30, "pine": 25, "juniper": 25, "willow": 5, "azalea": 10, "fruit": 5},
    "bunjin":  {"cloud": 20, "pine": 35, "juniper": 20, "tuft": 25},
    "kengai":  {"cloud": 30, "pine": 30, "juniper": 40},
}
# form -> bark weights (the existing forms)
BARK_BY_FORM = {
    "moyogi":  {"smooth": 50, "plated": 15, "rough": 20, "hollow": 10, "twisted": 5},
    "chokkan": {"smooth": 45, "plated": 35, "rough": 15, "hollow": 5},
    "shakan":  {"smooth": 45, "plated": 15, "twisted": 30, "rough": 10},
    "bunjin":  {"smooth": 40, "twisted": 50, "plated": 10},
    "kengai":  {"smooth": 45, "twisted": 45, "plated": 10},
}
# foliage -> the barks it may be drawn with (a draw outside the list is redrawn)
BARK_BY_FOLIAGE = {
    "cloud": "smooth plated rough hollow twisted", "pine": "smooth plated twisted", "juniper": "smooth twisted",
    "elm": "smooth rough hollow", "willow": "smooth rough", "tuft": "smooth twisted plated",
    "azalea": "smooth rough", "fruit": "smooth rough hollow",
}
# deadwood chance by form, only with pine / juniper / tuft foliage, never with hollow or rough bark
DEADWOOD_BY_FORM = {"bunjin": 0.5, "shakan": 0.3, "kengai": 0.4, "chokkan": 0.15, "moyogi": 0.1,
                    "fukinagashi": 0.6, "hankengai": 0.4}


def tables():
    import pprint
    print("=" * 100)
    print("NEW FORMS (FORMS-table entries), the style weights, and the combination tables")
    print("=" * 100)
    pprint.pprint(NEW_FORMS, width=110, sort_dicts=False)
    print()
    print("styles =", STYLE_WEIGHTS)
    print()
    print("FOLIAGE_BY_FORM =")
    pprint.pprint(FOLIAGE_BY_FORM, width=110, sort_dicts=False)
    print("BARK_BY_FORM =")
    pprint.pprint(BARK_BY_FORM, width=110, sort_dicts=False)
    print("BARK_BY_FOLIAGE =")
    pprint.pprint(BARK_BY_FOLIAGE, width=110, sort_dicts=False)
    print("DEADWOOD_BY_FORM =", DEADWOOD_BY_FORM)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    rng = random.Random(seed)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    foliage_specimens(rng)
    bark_specimens(rng)
    branch_specimens()
    tables()


if __name__ == "__main__":
    main()
