"""Original ink-and-watercolour illustrations, drawn as SVG.

Every illustration combines soft watercolour washes (blurred blobs with
irregular edges) with ink line work that wobbles slightly like a hand-drawn
pen line. They are returned as data URIs because Streamlit's HTML sanitiser
strips inline <svg> elements.
"""

from __future__ import annotations

import base64
from functools import lru_cache

INK = "#26251E"
INK_SOFT = "#6F6C5B"
PAPER = "#FCFDFD"
WASH = {
    "sand": "#DCD9C9",
    "amber": "#F7C873",
    "gold": "#FDE047",
    "orange": "#F97316",
    "sky": "#C7D8E4",
    "sage": "#C5D1B5",
    "rose": "#EBC8B8",
    "navy": "#16233D",
}

_DEFS = """
<defs>
  <filter id="ink" filterUnits="userSpaceOnUse" x="-100" y="-100" width="3000" height="3000">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6"/>
  </filter>
  <filter id="wash" filterUnits="userSpaceOnUse" x="-200" y="-200" width="3200" height="3200">
    <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="9" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="34" result="d"/>
    <feGaussianBlur in="d" stdDeviation="2.2"/>
  </filter>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="2"/>
    <feColorMatrix values="0 0 0 0 0.15  0 0 0 0 0.14  0 0 0 0 0.11  0 0 0 0.06 0"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
</defs>
"""


def _svg(w: int, h: int, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f"{_DEFS}{body}</svg>")


def _uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def wash(cx, cy, rx, ry, color, opacity=0.55):
    """A watercolour patch."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WASH.get(color, color)}" '
            f'opacity="{opacity}" filter="url(#wash)"/>')


def ink(d, width=2.4, color=INK, fill="none", extra=""):
    """An ink stroke along an SVG path."""
    return (f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
            f'stroke-linejoin="round" filter="url(#ink)" {extra}/>')


def dot(cx, cy, r, color=INK, opacity=1.0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WASH.get(color, color)}" opacity="{opacity}" filter="url(#ink)"/>'


def bolt(x, y, s=1.0, fill="amber"):
    """Lightning bolt, the FlashEDA motif."""
    pts = [(14, 0), (0, 26), (11, 26), (6, 46), (24, 17), (13, 17), (18, 0)]
    d = "M " + " L ".join(f"{x + px * s:.1f} {y + py * s:.1f}" for px, py in pts) + " Z"
    return ink(d, 2.2, fill=WASH.get(fill, fill))


def sheet(x, y, w, h, lines=6, gap=None):
    """A paper sheet with ruled lines."""
    gap = gap or (h - 30) / max(lines, 1)
    out = ink(f"M {x} {y + 8} Q {x} {y} {x + 8} {y} L {x + w - 8} {y} Q {x + w} {y} {x + w} {y + 8} "
              f"L {x + w} {y + h - 8} Q {x + w} {y + h} {x + w - 8} {y + h} L {x + 8} {y + h} Q {x} {y + h} {x} {y + h - 8} Z",
              fill=PAPER)
    for i in range(lines):
        ly = y + 20 + i * gap
        lw = w - 30 - (i * 13 % 3) * 12
        out += ink(f"M {x + 14} {ly} L {x + 14 + lw} {ly}", 1.6, INK_SOFT)
    return out


# ---------------------------------------------------------------------------
# Illustrations
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def hero() -> str:
    """A towering dataset, a quick sample of points, and a finished report and script."""
    b = ""
    b += wash(260, 300, 250, 150, "sand", 0.7) + wash(640, 250, 210, 120, "amber", 0.45)
    b += wash(990, 290, 230, 140, "sky", 0.6) + wash(620, 380, 520, 60, "sage", 0.35)
    # Tall stack of data sheets (the big file)
    for i in range(7):
        b += ink(f"M {150 + i * 6} {360 - i * 38} L {330 + i * 6} {360 - i * 38} L {350 + i * 6} {330 - i * 38} "
                 f"L {170 + i * 6} {330 - i * 38} Z", 2.0, fill=PAPER)
        b += ink(f"M {185 + i * 6} {346 - i * 38} L {300 + i * 6} {346 - i * 38}", 1.4, INK_SOFT)
    b += ink("M 150 360 L 150 396 L 330 396 L 330 360", 2.0, fill="none")
    b += f'<text x="190" y="430" font-family="Inter, Arial" font-size="17" fill="{INK_SOFT}">100,000,000 rows</text>'
    # Path of sampled points flowing to the right
    for i, (px, py) in enumerate([(395, 250), (430, 228), (468, 236), (505, 214), (540, 224), (575, 205)]):
        b += dot(px, py, 6 if i % 2 else 4.5, "orange" if i in (1, 4) else INK)
    # Grid of sampled dots with a bolt (centre)
    for r in range(6):
        for c in range(6):
            b += dot(585 + c * 22, 120 + r * 22, 3.2, INK_SOFT, 0.55)
    for (c, r) in [(2, 0), (3, 1), (2, 2), (1, 3), (2, 3), (3, 3), (2, 4), (1, 5)]:
        b += dot(585 + c * 22, 120 + r * 22, 5.2, "orange")
    b += ink("M 570 105 L 715 105 L 715 245 L 570 245 Z", 2.0)
    b += f'<text x="588" y="275" font-family="Inter, Arial" font-size="17" fill="{INK_SOFT}">5,000-row sample</text>'
    # Report clipboard
    b += ink("M 790 120 L 930 120 L 930 330 L 790 330 Z", 2.4, fill=PAPER)
    b += ink("M 835 108 L 885 108 L 885 132 L 835 132 Z", 2.2, fill=WASH["sand"])
    for i, hgt in enumerate([40, 70, 52, 95, 64]):
        b += ink(f"M {812 + i * 22} 300 L {812 + i * 22} {300 - hgt} L {828 + i * 22} {300 - hgt} L {828 + i * 22} 300 Z",
                 1.8, fill=WASH["amber"] if i == 3 else WASH["sky"])
    b += ink("M 806 160 L 900 160 M 806 176 L 880 176", 1.6, INK_SOFT)
    # Code sheet with a check mark
    b += sheet(965, 150, 150, 200, 7)
    b += f'<circle cx="1110" cy="345" r="26" fill="{WASH["sage"]}" filter="url(#ink)" stroke="{INK}" stroke-width="2.2"/>'
    b += ink("M 1097 345 L 1107 356 L 1124 334", 3.0)
    b += bolt(732, 30, 1.6)
    return _uri(_svg(1200, 460, b))


@lru_cache(maxsize=None)
def step(name: str) -> str:
    """Small spot illustrations for the five pipeline steps and feature cards."""
    b = ""
    if name == "sample":
        b += wash(160, 120, 120, 80, "amber", 0.45)
        for r in range(7):
            for c in range(9):
                b += dot(60 + c * 26, 40 + r * 26, 3.4, INK_SOFT, 0.5)
        for (c, r) in [(4, 0), (5, 1), (4, 2), (3, 3), (4, 3), (5, 3), (4, 4), (3, 5), (3, 6)]:
            b += dot(60 + c * 26, 40 + r * 26, 6, "orange")
    elif name == "analyse":
        b += wash(150, 130, 120, 80, "sky", 0.6)
        b += ink("M 70 40 L 230 40 L 230 210 L 70 210 Z", 2.4, fill=PAPER)
        for i, hgt in enumerate([50, 90, 66, 120, 80]):
            b += ink(f"M {92 + i * 26} 190 L {92 + i * 26} {190 - hgt} L {110 + i * 26} {190 - hgt} L {110 + i * 26} 190 Z",
                     1.8, fill=WASH["amber"] if i == 3 else WASH["sand"])
        b += ink("M 235 70 L 270 50 L 285 90 Z", 2.2, fill=WASH["gold"]) + ink("M 260 63 L 262 76", 2.4)
    elif name == "plan":
        b += wash(160, 130, 130, 85, "sage", 0.5)
        b += sheet(80, 30, 160, 190, 0)
        for i in range(5):
            y = 62 + i * 32
            b += ink(f"M 100 {y - 9} L 118 {y - 9} L 118 {y + 9} L 100 {y + 9} Z", 1.8)
            if i < 4:
                b += ink(f"M 103 {y} L 108 {y + 5} L 116 {y - 6}", 2.4, "#C2410C")
            b += ink(f"M 130 {y} L {215 - (i % 2) * 25} {y}", 1.6, INK_SOFT)
    elif name == "write":
        b += wash(160, 120, 135, 85, "amber", 0.4)
        b += ink("M 60 40 L 260 40 L 260 210 L 60 210 Z", 2.4, fill=WASH["navy"])
        for i, (x0, w) in enumerate([(80, 90), (95, 120), (95, 70), (110, 100), (95, 60), (80, 40)]):
            b += ink(f"M {x0} {66 + i * 24} L {x0 + w} {66 + i * 24}", 3.0, WASH["gold"] if i == 1 else "#CBD5E1")
    elif name == "validate":
        b += wash(160, 125, 135, 85, "sage", 0.55)
        b += sheet(50, 50, 100, 140, 5) + sheet(170, 50, 100, 140, 5)
        b += ink("M 150 112 L 170 112 M 150 128 L 170 128", 2.6)
        b += f'<circle cx="255" cy="185" r="24" fill="{WASH["sage"]}" stroke="{INK}" stroke-width="2.2" filter="url(#ink)"/>'
        b += ink("M 243 185 L 252 195 L 268 175", 3.0)
    elif name == "clean":
        b += wash(150, 125, 125, 80, "rose", 0.45)
        b += sheet(60, 50, 150, 150, 5)
        b += ink("M 230 40 L 180 170", 4.0) + ink("M 165 165 L 200 178 L 190 205 L 150 192 Z", 2.2, fill=WASH["amber"])
        for (x, y) in [(240, 90), (262, 120), (236, 140)]:
            b += ink(f"M {x - 7} {y} L {x + 7} {y} M {x} {y - 7} L {x} {y + 7}", 2.2, "#C2410C")
    elif name == "models":
        b += wash(160, 130, 130, 80, "sky", 0.55)
        for i, (hgt, col) in enumerate([(70, "sand"), (130, "amber"), (100, "sky")]):
            x = 85 + i * 60
            b += ink(f"M {x} 210 L {x} {210 - hgt} L {x + 48} {210 - hgt} L {x + 48} 210 Z", 2.2, fill=WASH[col])
        b += ink("M 70 210 L 260 210", 2.4) + bolt(158, 30, 0.9, "gold")
    elif name == "contracts":
        b += wash(160, 125, 120, 85, "sage", 0.55)
        b += ink("M 160 30 L 240 60 L 236 130 Q 228 190 160 220 Q 92 190 84 130 L 80 60 Z", 2.6, fill=PAPER)
        b += ink("M 125 125 L 150 152 L 198 98", 4.0, "#3F6212")
    elif name == "drift":
        b += wash(160, 130, 140, 80, "amber", 0.35)
        b += ink("M 40 200 C 90 200 100 70 140 70 C 180 70 190 200 240 200", 2.6, fill="none")
        b += ink("M 80 200 C 130 200 150 100 190 100 C 230 100 240 200 290 200", 2.6, "#C2410C", extra='stroke-dasharray="8 7"')
        b += ink("M 30 202 L 300 202", 2.0)
    elif name == "databases":
        b += wash(160, 130, 110, 85, "sky", 0.6)
        for i in range(3):
            y = 60 + i * 45
            b += ink(f"M 100 {y} C 100 {y - 22} 220 {y - 22} 220 {y} L 220 {y + 40} C 220 {y + 62} 100 {y + 62} 100 {y + 40} Z", 2.3, fill=PAPER)
        b += ink("M 100 60 C 100 82 220 82 220 60", 2.0)
        for k in range(6):
            b += dot(245 + (k % 2) * 16, 90 + k * 18, 4.5, "orange" if k % 3 == 0 else INK_SOFT)
    elif name == "text":
        b += wash(150, 125, 125, 85, "rose", 0.45)
        b += ink("M 60 50 L 230 50 Q 250 50 250 70 L 250 150 Q 250 170 230 170 L 120 170 L 85 205 L 92 170 L 80 170 Q 60 170 60 150 L 60 70 Q 60 50 80 50 Z", 2.4, fill=PAPER)
        for i, w in enumerate([140, 110, 125]):
            b += ink(f"M 85 {85 + i * 26} L {85 + w} {85 + i * 26}", 1.8, INK_SOFT)
        b += ink("M 245 150 L 285 150 L 285 190 L 245 190 Z", 2.2, fill=WASH["amber"]) + ink("M 252 150 L 252 136 Q 265 120 278 136 L 278 150", 2.2)
    elif name == "time-series":
        b += wash(160, 130, 145, 80, "sky", 0.55)
        b += ink("M 40 200 L 290 200 M 40 200 L 40 40", 2.2)
        b += ink("M 45 170 L 75 150 L 100 160 L 130 120 L 160 132 L 190 96", 2.8)
        b += ink("M 190 96 L 220 104 L 250 74 L 280 82", 2.8, "#C2410C", extra='stroke-dasharray="7 7"')
        b += wash(240, 85, 50, 22, "amber", 0.6)
    elif name == "notebook":
        b += wash(160, 125, 125, 85, "amber", 0.4)
        b += ink("M 90 30 L 240 30 L 240 220 L 90 220 Z", 2.4, fill=PAPER)
        for i in range(7):
            b += ink(f"M 80 {48 + i * 26} Q 70 {54 + i * 26} 92 {58 + i * 26}", 2.0)
        for i, (w, col) in enumerate([(110, INK_SOFT), (80, "#C2410C"), (120, INK_SOFT), (70, INK_SOFT)]):
            b += ink(f"M 110 {64 + i * 38} L {110 + w} {64 + i * 38}", 2.0 if col == INK_SOFT else 3.0, col)
    elif name == "install":
        b += wash(160, 125, 135, 85, "sand", 0.7)
        b += ink("M 60 60 L 260 60 L 260 200 L 60 200 Z", 2.4, fill=WASH["navy"])
        b += ink("M 60 85 L 260 85", 2.0, "#CBD5E1")
        b += ink("M 80 115 L 95 127 L 80 139", 2.6, WASH["gold"]) + ink("M 105 140 L 190 140", 3.0, "#CBD5E1")
        b += bolt(220, 20, 1.0)
    elif name == "reference":
        b += wash(160, 125, 130, 85, "sky", 0.5)
        for i in range(3):
            b += ink(f"M {70 + i * 22} {50 + i * 12} L {200 + i * 22} {50 + i * 12} L {200 + i * 22} {210 + i * 4} L {70 + i * 22} {210 + i * 4} Z", 2.2, fill=PAPER)
        for i, w in enumerate([100, 80, 110, 60]):
            b += ink(f"M 130 {100 + i * 26} L {130 + w} {100 + i * 26}", 1.8, INK_SOFT)
        b += ink("M 128 86 L 175 86", 3.0, "#C2410C")
    else:
        b += wash(160, 125, 130, 85, "sand", 0.7) + bolt(140, 70, 1.8)
    return _uri(_svg(320, 250, b))


@lru_cache(maxsize=None)
def landscape() -> str:
    """Footer scene: a 'data forest' of bar-chart trees on rolling washes."""
    b = ""
    b += wash(250, 230, 330, 90, "sage", 0.55) + wash(750, 220, 360, 100, "sky", 0.5)
    b += wash(1150, 235, 300, 90, "sage", 0.5) + wash(520, 250, 260, 60, "amber", 0.3)
    heights = [70, 110, 85, 140, 60, 125, 95, 150, 75, 115, 90, 135, 65, 105, 120, 80, 145, 70, 100, 130]
    for i, hgt in enumerate(heights):
        x = 40 + i * 70 + (i % 3) * 6
        base = 300
        b += ink(f"M {x + 14} {base} L {x + 14} {base - hgt * 0.45}", 2.2)  # trunk
        canopy = ["sage", "amber", "sky", "sage", "rose"][i % 5]
        b += wash(x + 14, base - hgt * 0.62, 26, hgt * 0.28, canopy, 0.75)
        cy, ry = base - hgt * 0.72, hgt * 0.3
        b += ink(f"M {x - 4} {cy} C {x - 4} {cy - ry * 1.2} {x + 32} {cy - ry * 1.2} {x + 32} {cy} C {x + 32} {cy + ry * 1.05} {x - 4} {cy + ry * 1.05} {x - 4} {cy} Z", 1.6)
        if i % 4 == 1:
            b += dot(x + 14, base - hgt * 1.02 - 8, 5, "orange")
    b += ink("M 0 300 C 300 286 600 310 900 296 C 1100 288 1300 302 1440 296", 2.0, INK_SOFT)
    return _uri(_svg(1440, 320, b))
