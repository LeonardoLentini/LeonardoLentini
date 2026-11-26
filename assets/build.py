"""Generates the SVG images used in the profile README.

Run from the repository root:  python3 assets/build.py
Every image is written to assets/ in a light and a dark version
(GitHub picks the right one through <picture> in the README).
"""

import os
from xml.sax.saxutils import escape

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- content
NAME = "Leonardo Lentini"
SUBTITLE = "AI & Data Engineering · University of Pisa"

# Phrases shown one after the other in the header (placeholders for now)
PHRASES = [
    "Too bad you read this, you just lost The Game.",
    "If you try until you can, then you can.",
]
PHRASE_SECONDS = 4.5

# ---------------------------------------------------------------- palettes
THEMES = {
    "light": dict(bg="#f5f2e9", ink="#1d3b2f", green="#2f7d4f", soft="#9cc7a4", muted="#6b7a70", faint="#c9cfc3"),
    "dark": dict(bg="#0f1813", ink="#dfeae2", green="#5fbf7f", soft="#2f5b3e", muted="#8fa496", faint="#2c3a31"),
}

SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Book Antiqua', serif"
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"


def svg(width, height, body, style, title, t):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<style>
.serif {{ font-family: {SERIF}; }}
.sans {{ font-family: {SANS}; }}
.ink, .acc, .mut, .fnt {{ fill: none; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }}
.ink {{ stroke: {t['ink']}; }}
.acc {{ stroke: {t['green']}; stroke-width: 2.6; }}
.mut {{ stroke: {t['muted']}; }}
.fnt {{ stroke: {t['faint']}; stroke-width: 1.6; }}
.draw {{ stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 1.8s ease-in-out forwards; }}
@keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
.fade {{ opacity: 0; animation: fade 1s ease-out forwards; }}
@keyframes fade {{ to {{ opacity: 1; }} }}
.flow {{ animation: flow 2.4s linear infinite; }}
@keyframes flow {{ to {{ stroke-dashoffset: -60; }} }}
.spin {{ transform-box: fill-box; transform-origin: center; animation: spin 14s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.bob {{ animation: bob 2.4s ease-in-out infinite; }}
@keyframes bob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
.beat {{ transform-box: fill-box; transform-origin: center; animation: beat 1.6s ease-in-out infinite; }}
@keyframes beat {{ 0%,100% {{ transform: scale(1); }} 15% {{ transform: scale(1.12); }} 30% {{ transform: scale(1); }} 45% {{ transform: scale(1.08); }} }}
{style}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; stroke-dashoffset: 0 !important; opacity: 1 !important; }}
  .ph {{ opacity: 0 !important; }} .ph0 {{ opacity: 1 !important; transform: none !important; }}
  .lvl {{ opacity: 0.9 !important; }} }}
</style>
<defs>
  <filter id="hand" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/>
    <feDisplacementMap in="SourceGraphic" scale="2.2"/>
  </filter>
</defs>
<rect width="{width}" height="{height}" rx="14" fill="{t['bg']}"/>
{body}
</svg>
"""


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("written", name)


def lines(paths, delay=0.0, step=0.06, cls="ink"):
    """Line-art strokes that draw themselves one after the other."""
    return "".join(f'<path d="{d}" class="{cls} draw" pathLength="1" style="animation-delay:{delay + i * step:.2f}s"/>'
                   for i, d in enumerate(paths))


def hand(content):
    return f'<g filter="url(#hand)">{content}</g>'


def river(x0, x1, y, amp=4, step=30):
    """A gentle wave from x0 to x1, used for the Arno."""
    d = f"M{x0},{y}"
    x, up = x0, True
    while x < x1:
        nx = min(x + step, x1)
        d += f" Q{(x + nx) / 2},{y - amp if up else y + amp} {nx},{y}"
        x, up = nx, not up
    return d


# ---------------------------------------------------------------- hero
def hero(theme):
    t = THEMES[theme]
    w, h = 1200, 270
    n = len(PHRASES)
    total, slot = n * PHRASE_SECONDS, 100 / n
    fade = slot * 0.12
    style = (f".ph {{ opacity: 0; animation: ph {total}s linear infinite; }}\n"
             f"@keyframes ph {{ 0% {{ opacity: 0; transform: translateY(6px); }} "
             f"{fade:.2f}% {{ opacity: 1; transform: none; }} {slot - fade:.2f}% {{ opacity: 1; transform: none; }} "
             f"{slot:.2f}% {{ opacity: 0; transform: translateY(-6px); }} 100% {{ opacity: 0; }} }}")
    texts = "".join(
        f'<text x="92" y="200" font-size="21" font-style="italic" fill="{t["ink"]}" class="serif ph ph{i}" '
        f'style="animation-delay:{i * PHRASE_SECONDS}s">{escape(p)}</text>' for i, p in enumerate(PHRASES))
    body = f"""
<text x="60" y="104" font-size="60" fill="{t['ink']}" class="serif fade" style="animation-delay:0.1s">{escape(NAME)}</text>
<text x="62" y="144" font-size="18" fill="{t['muted']}" class="sans fade" style="animation-delay:0.4s" letter-spacing="0.3">{escape(SUBTITLE)}</text>
<text x="60" y="210" font-size="48" fill="{t['green']}" class="serif fade" style="animation-delay:0.8s">“</text>
{texts}
<path d="{river(60, w - 60, h - 30)}" fill="none" stroke="{t['green']}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="18 12" class="flow"/>
"""
    write(f"hero-{theme}.svg", svg(w, h, body, style,
                                   f"{NAME}. M.Sc. student in AI and Data Engineering at the University of Pisa.", t))


# ---------------------------------------------------------------- skyline timeline
G = 220          # ground line of the skyline
NOW_X = 782      # where the drawn (past) part of the timeline ends (just past the Tower)

STOPS = [  # (x, date, title, detail, state)
    (90, "2021", "B.Sc. starts", "Computer Engineering", "done"),
    (380, "2025", "B.Sc. degree", "Computer Engineering", "done"),
    (NOW_X, "2025", "M.Sc. starts", "AI & Data Engineering", "now"),
    (1110, "next", "Still writing it", "", "next"),
]


def roofline():
    """One continuous line: the Pisa skyline along the Arno, used as the timeline."""
    g = G
    return " ".join([
        f"M40,{g} H120",
        # houses on the Lungarno
        f"V158 H176 V146 H226 V166 H270 V128 L285,118 L300,128 V160 H340 V{g}",
        "H430",
        # Baptistery
        f"V166 H440 C440,140 452,130 466,127 L480,88 L494,127 C508,130 520,140 520,166 H530 V{g}",
        "H550",
        # Cathedral
        f"V156 H565 V136 L590,124 V110 L620,88 L650,110 V124 L675,136 V156 H690 V{g}",
        "H718",
        # Leaning Tower
        f"L728,62 H731 V49 H751 V62 H756 L746,{g}",
        "H810",
        # Santa Maria della Spina
        f"V176 L816,150 L822,176 H842 L850,138 L858,176 H878 L884,150 L890,176 V{g}",
        "H920",
        # more houses
        f"V160 H966 V142 H1010 V170 H1044 V150 H1066 V{g}",
        "H1160",
    ])


def skyline_details():
    g = G
    d = []
    for x0, x1, top in [(120, 176, 158), (176, 226, 146), (226, 270, 166), (300, 340, 160),
                        (920, 966, 160), (966, 1010, 142), (1010, 1044, 170), (1044, 1066, 150)]:
        for wy in range(top + 14, g - 14, 20):
            d += [f"M{x},{wy} v8" for x in range(x0 + 10, x1 - 6, 12)]
    d += [f"M{x},{g} V{g - 16} a6,6 0 0 1 12,0 V{g}" for x in range(442, 512, 18)]  # Baptistery arches
    d += ["M440,190 H520", "M445,166 H515"]
    d += [f"M{x},{g} V{g - 20} a8,8 0 0 1 16,0 V{g}" for x in (566, 612, 658)]  # Cathedral portals
    d += ["M565,180 H675", "M590,156 H650"] + [f"M{x},176 v-14" for x in range(572, 672, 10)]
    for y in range(g - 24, 70, -24):  # Tower galleries (follow the tilt)
        off = (g - y) * 10 / (g - 62)
        d.append(f"M{718 + off:.1f},{y} H{746 + off:.1f}")
    d += ["M850,176 V196", "M836,200 a14,14 0 0 1 28,0"]
    return d


def skyline(theme):
    t = THEMES[theme]
    w, h = 1200, 350
    roof = roofline()
    style = f"""
.grow {{ animation: grow 3.2s cubic-bezier(.4,.1,.3,1) 0.2s both; }}
@keyframes grow {{ from {{ width: 0; }} to {{ width: {NOW_X}px; }} }}
.halo {{ transform-box: fill-box; transform-origin: center; animation: halo 2.2s ease-out infinite; }}
@keyframes halo {{ from {{ opacity: 0.6; transform: scale(1); }} to {{ opacity: 0; transform: scale(2.6); }} }}
.ahead {{ animation: ahead 1.6s linear infinite; }}
@keyframes ahead {{ to {{ stroke-dashoffset: -20; }} }}
"""
    parts = [
        f'<clipPath id="past"><rect x="0" y="0" width="{NOW_X}" height="{h}" class="grow"/></clipPath>',
        f'<clipPath id="future"><rect x="{NOW_X}" y="0" width="{w - NOW_X}" height="{h}"/></clipPath>',
        hand(lines(skyline_details(), 0.6, 0.01, "fnt") +
             f'<path d="{roof}" fill="none" stroke="{t["muted"]}" stroke-width="2" stroke-dasharray="4 6" '
             f'stroke-linecap="round" clip-path="url(#future)" class="ahead"/>'
             f'<path d="{roof}" fill="none" stroke="{t["green"]}" stroke-width="3.2" stroke-linejoin="round" '
             f'stroke-linecap="round" clip-path="url(#past)"/>'),
        f'<path d="{river(40, 1160, G + 22, 3, 26)}" fill="none" stroke="{t["soft"]}" stroke-width="2" '
        f'stroke-linecap="round" stroke-dasharray="14 12" class="flow"/>',
    ]
    for i, (x, date, title, detail, state) in enumerate(STOPS):
        delay = 0.3 + i * 0.7
        color = t["muted"] if state == "next" else t["green"]
        if state == "now":
            parts.append(f'<circle cx="{x}" cy="{G}" r="8" fill="{color}" class="halo"/>')
        fill = t["bg"] if state == "next" else color
        parts.append(f'<circle cx="{x}" cy="{G}" r="8" fill="{fill}" stroke="{color}" stroke-width="2.5" '
                     f'class="fade" style="animation-delay:{delay}s"/>')
        anchor = "start" if i == 0 else "end" if i == len(STOPS) - 1 else "middle"
        tx = x - 8 if i == 0 else x + 8 if i == len(STOPS) - 1 else x
        parts.append(f'<g class="fade" style="animation-delay:{delay}s">'
                     f'<text x="{tx}" y="{G + 62}" font-size="14" fill="{color}" text-anchor="{anchor}" class="sans" letter-spacing="1.2">{escape(date)}</text>'
                     f'<text x="{tx}" y="{G + 88}" font-size="21" fill="{t["ink"]}" text-anchor="{anchor}" class="serif">{escape(title)}</text>'
                     f'<text x="{tx}" y="{G + 110}" font-size="14.5" fill="{t["muted"]}" text-anchor="{anchor}" class="sans">{escape(detail)}</text></g>')
    write(f"skyline-{theme}.svg", svg(w, h, "\n".join(parts), style,
                                      "Timeline drawn as the skyline of Pisa along the Arno. 2021: B.Sc. in Computer Engineering starts. "
                                      "2025: B.Sc. degree. 2025: M.Sc. in AI and Data Engineering starts, by the Leaning Tower. "
                                      "Next: still writing it.", t))


# ---------------------------------------------------------------- project illustrations
# Each returns (extra css, svg body) for a 600 x 270 drawing area.

def il_promotion(t):
    stairs = ["M80,250 H520", "M110,250 V215 H190 V180 H250 V145 H310 V110 H400 V250"]
    winner = ["M355,72 v24", "M355,96 l-8,14 M355,96 l8,14", "M355,80 l-12,-12 M355,80 l12,-12"]
    others = ["M150,197 v14", "M150,211 l-6,4 M150,211 l6,4", "M220,162 v14", "M220,176 l-6,4 M220,176 l6,4"]
    bars = ["M440,250 V205 H462 V250", "M472,250 V180 H494 V250", "M504,250 V220 H526 V250"]
    body = hand(lines(stairs) + lines(others, 0.4, cls="mut") + lines(bars, 0.6) +
                '<circle cx="150" cy="189" r="7" class="mut"/><circle cx="220" cy="154" r="7" class="mut"/>'
                + lines(winner, 0.9, cls="acc") + '<circle cx="355" cy="62" r="10" class="acc"/>'
                + f'<g class="bob">{lines(["M483,150 V100", "M471,112 L483,100 L495,112"], 1.1, cls="acc")}</g>')
    return "", body


def il_battery(t):
    panel = ["M70,175 L170,175 L192,130 L92,130 Z", "M103,175 L125,130 M136,175 L158,130", "M81,153 H181",
             "M131,175 V220", "M108,220 H154"]
    battery = ["M262,105 H338 V205 H262 Z", "M287,105 V95 H313 V105"]
    pylon = ["M450,220 L470,82 H490 L510,220", "M440,98 H520", "M460,150 H500 M455,185 H505",
             "M468,104 L496,150 M492,104 L464,150", "M440,98 v10 M520,98 v10"]
    rays = "".join(f'<path d="M{110 + 24 * c:.1f},{62 + 24 * s:.1f} L{110 + 34 * c:.1f},{62 + 34 * s:.1f}" class="acc"/>'
                   for c, s in [(1, 0), (0.707, 0.707), (0, 1), (-0.707, 0.707), (-1, 0), (-0.707, -0.707), (0, -1), (0.707, -0.707)])
    charge = "".join(f'<rect x="274" y="{180 - i * 25}" width="52" height="17" rx="3" fill="{t["green"]}" class="lvl" '
                     f'style="animation-delay:{i * 0.5}s"/>' for i in range(3))
    style = """
.lvl { opacity: 0.15; animation: lvl 3s ease-in-out infinite; }
@keyframes lvl { 0%,15% { opacity: 0.15; } 35%,80% { opacity: 0.9; } 100% { opacity: 0.15; } }
"""
    wires = ('<path d="M190,160 H262" class="acc flow" stroke-dasharray="8 8"/>'
             '<path d="M338,160 H458" class="acc flow" stroke-dasharray="8 8"/>')
    body = hand(lines(["M50,220 H550"]) + lines(panel, 0.2) + lines(battery, 0.5) + lines(pylon, 0.8) +
                f'<g class="spin"><circle cx="110" cy="62" r="15" class="acc"/>{rays}</g>' + wires) + charge
    return style, body


def il_love(t):
    nodes = [(110, 80), (90, 175), (190, 225), (200, 45), (420, 40), (510, 90), (500, 200), (390, 235), (300, 30)]
    edges = [(0, 3), (0, 1), (1, 2), (4, 5), (5, 6), (6, 7), (3, 8), (8, 4)]
    hx, hy = 300, 140
    spokes = "".join(f'<path d="M{x},{y} L{hx},{hy}" class="fnt"/>' for x, y in nodes)
    links = lines([f"M{nodes[a][0]},{nodes[a][1]} L{nodes[b][0]},{nodes[b][1]}" for a, b in edges], 0.2, 0.05, "mut")
    match = (f'<path d="M{nodes[1][0]},{nodes[1][1]} Q200,120 {hx - 32},{hy - 10}" class="acc flow" stroke-dasharray="8 8"/>'
             f'<path d="M{nodes[5][0]},{nodes[5][1]} Q410,130 {hx + 32},{hy - 10}" class="acc flow" stroke-dasharray="8 8"/>')
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{t["bg"]}" class="{"acc" if i in (1, 5) else "ink"}"/>'
                   for i, (x, y) in enumerate(nodes))
    heart = (f'<path d="M300,178 C255,148 250,108 277,102 C290,99 300,110 300,118 C300,110 310,99 323,102 '
             f'C350,108 345,148 300,178 Z" fill="{t["green"]}" fill-opacity="0.18" class="acc beat"/>')
    return "", hand(spokes + links + match + dots + heart)


def il_cloud(t):
    board = ["M140,150 H300 V250 H140 Z", "M140,150 V128 H300 V150",
             "M170,128 L155,150 M210,128 L195,150 M250,128 L235,150 M290,128 L275,150", "M160,190 H280 M160,215 H240"]
    stick = ('<g class="clap"><path d="M140,124 L300,124 L300,104 L140,104 Z" class="ink"/>'
             '<path d="M168,104 L182,124 M208,104 L222,124 M248,104 L262,124" class="ink"/></g>')
    cloud = ["M380,105 C362,105 358,80 380,77 C382,55 410,48 422,64 C432,44 470,50 468,76 C490,76 494,105 472,105 Z"]
    mapred = ["M425,112 L380,160 M425,112 V160 M425,112 L470,160",
              "M380,174 L425,222 M425,174 V222 M470,174 L425,222"]
    star = ('<path d="M425,222 l5,11 12,1 -9,8 3,12 -11,-6 -11,6 3,-12 -9,-8 12,-1 Z" '
            f'fill="{t["green"]}" fill-opacity="0.25" class="acc"/>')
    style = """
.clap { transform-box: fill-box; transform-origin: 0% 100%; animation: clap 2.6s ease-in-out infinite; }
@keyframes clap { 0%,60%,100% { transform: rotate(0); } 70% { transform: rotate(-14deg); } 85% { transform: rotate(0); } }
"""
    flows = "".join(f'<path d="{d}" class="acc flow" stroke-dasharray="7 7"/>' for d in mapred)
    body = hand(lines(["M80,250 H520"]) + lines(board, 0.1) + stick + lines(cloud, 0.5) + flows +
                "".join(f'<circle cx="{x}" cy="167" r="7" fill="{t["bg"]}" class="ink"/>' for x in (380, 425, 470)) + star)
    return style, body


def il_escape(t):
    door = ["M200,250 V60 H350 V250", "M215,250 V75 H335 V250", "M230,95 H320 V150 H230 Z", "M230,170 H320 V230 H230 Z"]
    key = ["M118,210 a14,14 0 1 1 0.1,0", "M132,210 H180", "M166,210 v12 M176,210 v9"]
    ticks = "".join(f'<path d="M{470 + 34 * c:.1f},{110 + 34 * s:.1f} L{470 + 40 * c:.1f},{110 + 40 * s:.1f}" class="ink"/>'
                    for c, s in [(1, 0), (0, 1), (-1, 0), (0, -1)])
    style = """
.hand1 { transform-origin: 470px 110px; animation: tick 5s steps(20) infinite; }
@keyframes tick { to { transform: rotate(360deg); } }
"""
    body = hand(lines(["M60,250 H540"]) + lines(door, 0.1) + '<circle cx="322" cy="160" r="5" class="acc"/>' +
                f'<g class="bob">{lines(key, 0.6, cls="acc")}</g>' +
                f'<circle cx="470" cy="110" r="44" class="ink"/>{ticks}'
                f'<path d="M470,110 V80" class="acc hand1"/><circle cx="470" cy="110" r="3" fill="{t["green"]}"/>'
                '<path d="M350,200 C390,200 420,180 440,150" class="mut flow" stroke-dasharray="6 8"/>')
    return style, body


def il_laureandosi(t):
    cap = ["M100,110 L190,78 L280,110 L190,142 Z", "M140,126 V168 C165,184 215,184 240,168 V126"]
    tassel = f'<g class="swing">{lines(["M190,110 L262,128 V168", "M256,168 H268 L262,182 Z"], 0.6, cls="acc")}</g>'
    paper = ["M385,122 V58 H485 V122", "M400,76 H468 M400,90 H460 M400,104 H468"]
    env = ["M360,122 H520 V222 H360 Z", "M360,122 L440,176 L520,122", "M360,222 L420,170 M520,222 L460,170"]
    style = """
.swing { transform-origin: 190px 110px; animation: swing 3s ease-in-out infinite; }
@keyframes swing { 0%,100% { transform: rotate(0); } 50% { transform: rotate(5deg); } }
"""
    body = hand(lines(["M80,250 H520"]) + lines(cap, 0.1) + tassel + lines(paper, 0.5) + lines(env, 0.7) +
                '<path d="M285,170 C315,195 330,190 352,172" class="acc flow" stroke-dasharray="7 7"/>')
    return style, body


def il_film(t):
    x0, x1, y0, y1 = 50, 400, 85, 195
    holes = "".join(f'<rect x="{x}" y="{y}" width="12" height="9" rx="2" class="ink"/>'
                    for x in range(x0 - 40, x1 + 40, 28) for y in (y0 + 8, y1 - 17))
    frames = "".join(f'<rect x="{x}" y="{y0 + 26}" width="76" height="58" rx="3" class="mut"/>'
                     for x in range(x0 - 40, x1 + 40, 92))
    style = """
.reel { animation: reel 2.2s linear infinite; }
@keyframes reel { to { transform: translateX(28px); } }
"""
    db = ["M435,190 V95", "M535,190 V95", "M435,190 A50,14 0 0 0 535,190",
          "M435,128 A50,14 0 0 0 535,128", "M435,160 A50,14 0 0 0 535,160"]
    body = (f'<clipPath id="strip"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath>' +
            hand(lines(["M80,250 H520", f"M{x0},{y0} H{x1}", f"M{x0},{y1} H{x1}"]) +
                 f'<g clip-path="url(#strip)"><g class="reel">{holes}{frames}</g></g>' +
                 f'<path d="M210,124 V166 L242,145 Z" fill="{t["green"]}" fill-opacity="0.3" class="acc"/>' +
                 '<ellipse cx="485" cy="95" rx="50" ry="14" class="acc"/>' + lines(db, 0.4) +
                 lines(["M400,140 C415,140 420,120 433,118"], 0.9, cls="acc")))
    return style, body


OPEN = {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3), (2, 3), (3, 3)}
NUMS = {(2, 0): "1", (2, 1): "2", (3, 2): "1", (1, 1): "1", (3, 3): "2"}


def il_meadow(t):
    gx, gy, c = 190, 30, 40
    cells = "".join(f'<rect x="{gx + i * c}" y="{gy + j * c}" width="{c}" height="{c}" '
                    + (f'class="fnt"/>' if (i, j) in OPEN else f'class="ink" style="fill:{t["faint"]};fill-opacity:0.45"/>')
                    for i in range(6) for j in range(4))
    nums = "".join(f'<text x="{gx + i * c + 20}" y="{gy + j * c + 27}" font-size="19" text-anchor="middle" '
                   f'fill="{t["green"] if n == "1" else t["ink"]}" class="sans">{n}</text>' for (i, j), n in NUMS.items())
    fx, fy = gx + 4 * c + 13, gy + 2 * c
    flag = (f'<g class="wave"><path d="M{fx},{fy + 33} V{fy + 8}" class="ink"/>'
            f'<path d="M{fx},{fy + 8} L{fx + 17},{fy + 14} L{fx},{fy + 20} Z" fill="{t["green"]}" class="acc"/></g>')

    def flower(x, h, d):
        petals = "".join(f'<circle cx="{x + 7 * dx}" cy="{250 - h + 7 * dy}" r="6" class="acc"/>'
                         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)])
        return (f'<g class="sway" style="animation-delay:{d}s">{lines([f"M{x},250 Q{x - 6},{250 - h / 2} {x},{250 - h}"], d)}'
                f'{petals}<circle cx="{x}" cy="{250 - h}" r="3.5" fill="{t["green"]}"/></g>')
    grass = "".join(f'<path d="M{x},250 l3,-9 M{x + 6},250 l-2,-7" class="mut"/>' for x in range(70, 540, 22))
    style = """
.wave { transform-box: fill-box; transform-origin: 0% 100%; animation: sway 2s ease-in-out infinite; }
.sway { transform-box: fill-box; transform-origin: 50% 100%; animation: sway 3s ease-in-out infinite; }
@keyframes sway { 0%,100% { transform: rotate(-3deg); } 50% { transform: rotate(3deg); } }
"""
    body = hand(cells + nums + flag + lines(["M60,250 H540"]) + grass +
                flower(95, 62, 0.3) + flower(140, 44, 0.5) + flower(470, 54, 0.4) + flower(515, 70, 0.6))
    return style, body


PROJECTS = [  # (slug, title, course, one-line description, illustration)
    ("employee-promotion", "Employee Promotion Prediction", "M.Sc. Data Mining & ML",
     "Who gets promoted? Imbalanced ML with fairness and SHAP / LIME", il_promotion),
    ("smart-battery", "Smart Battery Manager", "M.Sc. Internet of Things",
     "Contiki-NG microgrid with an edge AI actuator, CoAP and MQTT", il_battery),
    ("love-mining", "LoveMining", "M.Sc. Large-Scale Databases",
     "Dating platform on MongoDB and a Neo4j graph of shared interests", il_love),
    ("director-actor", "Director-Actor Partnerships", "M.Sc. Cloud Computing",
     "Best director-actor pairs on 3.6 GB of IMDb with Hadoop and Spark", il_cloud),
    ("escape-room", "Escape Room over TCP", "B.Sc. Computer Networks",
     "Two-player text escape room on a C server over TCP sockets", il_escape),
    ("laureandosi", "Laureandosi", "B.Sc. Software Engineering",
     "Graduation reports as PDFs, emailed to students, designed in UML", il_laureandosi),
    ("filmsphere", "FilmSphere", "B.Sc. Databases",
     "MySQL database for a movie streaming service", il_film),
    ("prato-fiorito", "Prato Fiorito", "B.Sc. Web Design",
     "Minesweeper for the web with accounts and leaderboards", il_meadow),
]


def project(theme, slug, title, course, desc, illustration):
    t = THEMES[theme]
    w, h = 600, 370
    style, art = illustration(t)
    body = f"""
<rect x="5" y="5" width="{w - 10}" height="{h - 10}" rx="16" fill="none" stroke="{t['muted']}" stroke-opacity="0.5" stroke-width="1.5"/>
<g transform="translate(0,12)">{art}</g>
<path d="M40,296 H{w - 40}" stroke="{t['faint']}" stroke-width="1.2"/>
<text x="40" y="326" font-size="22" fill="{t['ink']}" class="serif">{escape(title)}<tspan font-size="14" fill="{t['green']}" class="sans" dx="10">{escape(course)}</tspan></text>
<text x="40" y="350" font-size="15" fill="{t['muted']}" class="sans">{escape(desc)}</text>
"""
    write(f"project-{slug}-{theme}.svg", svg(w, h, body, style, f"{title}. {course}. {desc}.", t))


# ---------------------------------------------------------------- footer
def footer(theme):
    t = THEMES[theme]
    w, h, g = 1200, 100, 66
    tower = [f"M1088,{g} V24 H1108 V{g}", "M1091,24 V16 H1105 V24"] + [f"M1088,{y} H1108" for y in range(g - 10, 26, -10)]
    body = (hand(f'<g transform="rotate(4 1098 {g})">{lines(tower, 0.1, 0.05)}</g>{lines([f"M40,{g} H1160"])}') +
            f'<path d="{river(40, 1160, g + 14)}" fill="none" stroke="{t["green"]}" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-dasharray="18 12" class="flow"/>')
    write(f"footer-{theme}.svg", svg(w, h, body, "", "", t))


# ---------------------------------------------------------------- contact buttons
def button(theme, slug, label, icon):
    t = THEMES[theme]
    w, h = 220, 60
    style = """
.arrow { animation: nudge 2.4s ease-in-out infinite; }
@keyframes nudge { 0%,100% { transform: translate(0,0); } 50% { transform: translate(3px,-3px); } }
"""
    body = (f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="14" fill="none" stroke="{t["green"]}" stroke-width="2"/>'
            + hand(icon(t)) +
            f'<text x="74" y="37" font-size="20" fill="{t["ink"]}" class="serif">{escape(label)}</text>'
            f'<g class="arrow"><path d="M184,36 L196,24 M188,24 H196 V32" class="acc"/></g>')
    write(f"button-{slug}-{theme}.svg", svg(w, h, body, style, label, t))


def icon_linkedin(t):
    return ('<rect x="24" y="16" width="28" height="28" rx="6" class="acc"/>'
            f'<circle cx="31.5" cy="23" r="1.8" fill="{t["green"]}"/>'
            '<path d="M31.5,28 V38 M37,38 V28 M37,32 C37,28 45,27 45,32 V38" class="acc"/>')


def icon_mail(t):
    return '<path d="M22,19 H54 V41 H22 Z" class="acc"/><path d="M22,19 L38,32 L54,19" class="acc"/>'


if __name__ == "__main__":
    for theme in THEMES:
        button(theme, "linkedin", "LinkedIn", icon_linkedin)
        button(theme, "email", "Email", icon_mail)
    for theme in THEMES:
        hero(theme)
        skyline(theme)
        for p in PROJECTS:
            project(theme, *p)
        footer(theme)
