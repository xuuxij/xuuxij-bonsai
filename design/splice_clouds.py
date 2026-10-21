"""Splice the designer's tonal cloud generator (cloud_shapes_r6.py) into the program as
its own section before the Cloud class, with its names prefixed so they sit beside the
landscape's; replaces the section if it is already there."""
import re
import sys

HERE = sys.argv[1]
src = open(f"{HERE}/cloud_shapes_r6.py", encoding="utf-8").read().split("\n")
prog = open(f"{HERE}/xuuxij-bonsai", encoding="utf-8").read()

start = next(i for i, l in enumerate(src) if l.startswith("TONES = "))
end = next(i for i, l in enumerate(src) if l.startswith("# ---- the catalogue"))
section = "\n".join(src[start:end]).rstrip() + "\n"

# the landscape section already defines these, identically
for name in ("BAYER8", "clamp", "smoothstep"):
    section = re.sub(rf"(?ms)^(def {name}\(.*?)(?=^\S)", "", section) if name != "BAYER8" else \
        re.sub(r"(?ms)^BAYER8 = \[\[.*?\]\]\n", "", section)
renames = {
    "TONES": "TC_TONES", "COVER": "TC_COVER", "DITHER": "TC_DITHER", "SAMPLES": "TC_SAMPLES",
    "DEPTHS": "TC_DEPTHS", "luminance": "tc_luminance", "LUM": "TC_LUM", "LADDER_SOFT": "TC_LADDER_SOFT",
    "LADDER": "TC_LADDER", "quantize": "tc_quantize", "halftone": "tc_halftone", "Noise": "TcNoise",
    "light_vector": "tc_light_vector", "domes_field": "tc_domes_field", "CUMULUS_SIZES": "TC_CUMULUS_SIZES",
    "cumulus_domes": "tc_cumulus_domes", "cumulus": "tc_cumulus", "pair": "tc_pair",
    "CIRRUS_SIZES": "TC_CIRRUS_SIZES", "cirrus": "tc_cirrus", "lenticular": "tc_lenticular",
    "roll": "tc_roll", "mackerel": "tc_mackerel", "mist": "tc_mist", "cloud": "tc_cloud", "fade": "tc_fade",
}
for old, new in renames.items():
    section = re.sub(rf"\b{old}\b", new, section)
# string literals that are kind names must stay as they were
for kind in ("cumulus", "cirrus", "lenticular", "roll", "mackerel", "mist"):
    section = section.replace(f'"tc_{kind}"', f'"{kind}"')
assert "def tc_cloud(" in section and "def tc_fade(" in section and "def clamp(" not in section

head = '''# ---- the tonal clouds -------------------------------------------------------------------
# The second cloud set, the default over a landscape: clouds made the way the landscape
# is, painted as lit, shaded masses (domes of overlapping half-ellipsoids, roughened by
# noise, lit from above on the landscape's light side, dark under the base) and halftoned
# into ░ ▒ █ in four greys of their own (W c g d: slots 13 14 7 8), in three depths with
# aerial perspective: far clouds faint and never solid, mid ones capped at the glow, near
# ones with solid white crowns. No ink. Designed from the same references as the landscape.

'''
marker = "class Cloud:"
i = prog.index(marker)
old = prog.find("# ---- the tonal clouds ----")
if 0 <= old < i:
    prog = prog[:old] + prog[i:]
    i = old
tail = '''

# The console's palette: the design shaded for the screen (see display_palette).
PALETTE_DAY = display_palette(DESIGN_DAY, TC_TONES)
'''
prog = prog[:i] + head + section + tail + "\n\n" + prog[i:]
open(f"{HERE}/xuuxij-bonsai", "w", encoding="utf-8", newline="\n").write(prog)
print("spliced", section.count("\n"), "lines")
