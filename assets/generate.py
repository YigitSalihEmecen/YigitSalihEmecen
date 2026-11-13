"""Generates every SVG graphic used by README.md, in a light and a dark variant.

Run from the repository root:  python3 assets/generate.py
Standard library only. Everything is deterministic.
"""
import math
from pathlib import Path

OUT = Path(__file__).parent
FONT = "'EB Garamond', Garamond, 'Times New Roman', Georgia, serif"
THEMES = {
    "light": {"ink": "#111111", "muted": "#555555", "rule": "#999999", "faint": "#d9d9d9",
              "accent": "#A51C30", "card": "#FAFAFA"},
    "dark": {"ink": "#e8e8e8", "muted": "#a8a8a8", "rule": "#6b6b6b", "faint": "#30363d",
             "accent": "#E8788A", "card": "#161B22"},
}
W = 800


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def small_caps(text, big, small, x, y, fill, spacing="0.6", weight="700", anchor=None):
    """Small caps from two font sizes, so it renders the same everywhere."""
    parts = []
    for i, word in enumerate(text.split(" ")):
        if i:
            parts.append(f'<tspan font-size="{small}"> </tspan>')
        if not word[0].isalnum():
            parts.append(f'<tspan font-size="{small}">{esc(word)}</tspan>')
            continue
        parts.append(f'<tspan font-size="{big}">{esc(word[0].upper())}</tspan>'
                     f'<tspan font-size="{small}">{esc(word[1:].upper())}</tspan>')
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x}" y="{y}"{a} fill="{fill}" font-family="{FONT}" font-weight="{weight}" '
            f'letter-spacing="{spacing}">{"".join(parts)}</text>')


def text(x, y, s, size, fill, style="", anchor=None, weight="400"):
    a = f' text-anchor="{anchor}"' if anchor else ""
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x}" y="{y}"{a} fill="{fill}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}"{st}>{esc(s)}</text>')


def svg(width, height, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title>{body}</svg>\n')


def rule(y, t, width=W):
    return (f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{t["rule"]}" stroke-width="1"/>'
            f'<line x1="0" y1="{y}" x2="56" y2="{y}" stroke="{t["accent"]}" stroke-width="2.5"/>')


# ---------------------------------------------------------------- banner and figures
def header(t):
    name = small_caps("Yiğit Salih Emecen", 42, 33, 0, 92, t["ink"], spacing="1.2")
    body = [name,
            text(2, 124, "Robotics and software engineer", 21, t["muted"], style="italic"),
            small_caps("M.Sc. Manufacturing & Robotics, TU Wien", 14, 11.5, 2, 152, t["muted"],
                       spacing="1", weight="400"),
            rule(190, t)]
    return svg(W, 196, "".join(body), "Yiğit Salih Emecen, robotics and software engineer")


def section(title, t):
    return svg(W, 40, small_caps(title, 22, 17.5, 0, 25, t["ink"], weight="400") + rule(34, t), title)


# ---------------------------------------------------------------- project icons (96 x 96 box)
def icon_polar(t):
    pts = []
    for i in range(0, 721):
        th = math.radians(i / 2)
        r = 40 * math.cos(3 * th) * (0.55 + 0.45 * math.cos(th / 3)) + 0
        pts.append(f"{48 + r * math.cos(th):.1f},{48 + r * math.sin(th):.1f}")
    return (f'<circle cx="48" cy="48" r="44" fill="none" stroke="{t["faint"]}"/>'
            f'<circle cx="48" cy="48" r="22" fill="none" stroke="{t["faint"]}"/>'
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="{t["accent"]}" stroke-width="1.1"/>'
            f'<circle cx="48" cy="48" r="2.5" fill="{t["ink"]}"/>')


def icon_gameboy(t):
    """The YellowBoy handheld as built: squarish body, bezel and screen, two plus-pads, three-slot speaker."""
    def plus(cx, cy, half=7.0, arm=5.0):
        a = arm / 2
        pts = [(-a, -half), (a, -half), (a, -a), (half, -a), (half, a), (a, a), (a, half), (-a, half),
               (-a, a), (-half, a), (-half, -a), (-a, -a)]
        d = " ".join(f"{cx + x:.1f},{cy + y:.1f}" for x, y in pts)
        return (f'<polygon points="{d}" fill="{t["accent"]}" fill-opacity="0.85" stroke="{t["ink"]}" '
                f'stroke-width="1.5" stroke-linejoin="round"/>')

    g = [f'<rect x="12" y="2" width="72" height="92" rx="7" fill="none" stroke="{t["ink"]}" stroke-width="1.6"/>',
         f'<rect x="22" y="8" width="52" height="38" rx="4.5" fill="none" stroke="{t["ink"]}" stroke-width="1.5"/>',
         f'<rect x="27" y="12.5" width="42" height="29" rx="1.5" fill="{t["accent"]}" fill-opacity="0.10" '
         f'stroke="{t["muted"]}" stroke-width="1"/>',
         plus(27, 66), plus(69, 66)]
    for i in range(3):
        g.append(f'<rect x="41" y="{59.3 + i * 5.2:.1f}" width="14" height="3" rx="1.5" fill="none" '
                 f'stroke="{t["ink"]}" stroke-width="1.3"/>')
    return "".join(g)


def icon_cycloid(t):
    R, r, d = 5, 3, 5
    pts = []
    for i in range(0, 1201):
        th = math.radians(i * 0.9) * 2
        x = (R - r) * math.cos(th) + d * math.cos((R - r) / r * th)
        y = (R - r) * math.sin(th) - d * math.sin((R - r) / r * th)
        pts.append(f"{48 + x * 5.6:.1f},{48 + y * 5.6:.1f}")
    return (f'<circle cx="48" cy="48" r="44" fill="none" stroke="{t["faint"]}"/>'
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="{t["accent"]}" stroke-width="1.1"/>'
            f'<circle cx="48" cy="48" r="3" fill="none" stroke="{t["ink"]}" stroke-width="1.4"/>')


def icon_tree(t):
    g = []

    def branch(x, y, ang, ln, depth):
        x2, y2 = x + ln * math.sin(ang), y - ln * math.cos(ang)
        g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{t["ink"]}" '
                 f'stroke-width="{0.6 + depth * 0.45:.2f}" stroke-linecap="round"/>')
        if depth == 0:
            g.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="1.8" fill="{t["accent"]}"/>')
            return
        branch(x2, y2, ang - 0.43, ln * 0.74, depth - 1)
        branch(x2, y2, ang + 0.43, ln * 0.74, depth - 1)

    branch(48, 94, 0.0, 24, 6)
    return "".join(g)


def icon_wave(t):
    pts = []
    for i in range(0, 97):
        x = i
        env = math.sin(math.pi * x / 96) ** 2
        pts.append(f"{x},{48 - 38 * env * math.sin(x / 96 * 2 * math.pi * 6):.1f}")
    return (f'<line x1="0" y1="48" x2="96" y2="48" stroke="{t["faint"]}"/>'
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="{t["accent"]}" stroke-width="1.5" '
            f'stroke-linejoin="round"/>')


def icon_road(t):
    """A straight road running to the horizon under a setting sun."""
    hz = 50
    g = [f'<circle cx="48" cy="{hz}" r="15" fill="{t["accent"]}" fill-opacity="0.85"/>',
         f'<rect x="0" y="{hz}" width="96" height="{96 - hz}" fill="{t["card"]}"/>',
         f'<line x1="0" y1="{hz}" x2="96" y2="{hz}" stroke="{t["ink"]}" stroke-width="1.3"/>',
         f'<path d="M45 {hz} L6 94 M51 {hz} L90 94" stroke="{t["ink"]}" stroke-width="1.6" fill="none"/>']
    for y0, y1 in ((53, 56), (60, 65), (71, 79), (86, 94)):
        g.append(f'<line x1="48" y1="{y0}" x2="48" y2="{y1}" stroke="{t["accent"]}" stroke-width="{0.8 + (y0 - hz) / 20:.2f}" '
                 f'stroke-linecap="round"/>')
    for i, y in enumerate((hz - 7, hz - 3)):
        g.append(f'<line x1="{30 - i * 4}" y1="{y}" x2="{66 + i * 4}" y2="{y}" stroke="{t["card"]}" stroke-width="1.6"/>')
    return "".join(g)


CARDS = [
    ("polarbot", "PolarBot", "ESP8266 · JavaScript", icon_polar,
     ["A €5 WiFi plotter with polar", "kinematics and fully 3D-printed", "parts. Browser control panel."]),
    ("yellowboy", "YellowBoy", "C++ · ESP32", icon_gameboy,
     ["A Game Boy emulator that fits in", "the ESP32's internal SRAM, no", "PSRAM. Analog audio, SD ROMs."]),
    ("cycloidal", "Cycloidal Gear Generator", "JavaScript · live demo", icon_cycloid,
     ["Design a cycloidal reduction by", "tuning every parameter, right", "in the browser."]),
    ("tree-gen", "Tree-Gen", "JavaScript · live demo", icon_tree,
     ["Generates a wide variety of tree", "models you can download.", "Free, runs in the browser."]),
    ("engine-sim", "Engine Sim", "JavaScript · live demo", icon_wave,
     ["A realistic engine sound", "simulator that runs in your", "browser."]),
    ("horizon", "To The Horizon", "JavaScript · live demo", icon_road,
     ["An endless procedural driving", "simulator with realistic engine", "sounds."]),
]


def card(spec, t):
    _, name, sub, icon, lines = spec
    cw, ch = 396, 124
    g = [f'<rect x="0.5" y="0.5" width="{cw - 1}" height="{ch - 1}" rx="6" fill="{t["card"]}" '
         f'stroke="{t["faint"]}"/>',
         f'<g transform="translate(14,14)">{icon(t)}</g>',
         text(126, 33, name, 19 if len(name) <= 16 else 16.5, t["ink"], weight="700"),
         f'<line x1="126" y1="41" x2="150" y2="41" stroke="{t["accent"]}" stroke-width="2"/>',
         text(126, 58, sub, 13, t["muted"], style="italic")]
    for i, ln in enumerate(lines):
        g.append(text(126, 79 + i * 16, ln, 13, t["ink"]))
    return svg(cw, ch, "".join(g), f"{name}: {' '.join(lines)}")


# ---------------------------------------------------------------- skills
STACK = [
    ("Robotics", ["ROS 2", "Gazebo", "RViz", "MoveIt", "URDF", "Digital twins", "5G teleoperation"]),
    ("Perception", ["OpenCV", "Point clouds", "Ensenso 3D", "LiDAR", "ToF sensing"]),
    ("Embedded", ["NVIDIA Jetson", "STM32", "ESP32 / ESP8266", "FreeRTOS", "I2C / SPI", "PID control",
                  "Verilog / VHDL"]),
    ("Programming", ["Python", "C++", "C", "C#", "JavaScript", "MATLAB / Simulink", "Bash"]),
    ("Tooling", ["Linux", "Docker", "Git", "CMake", "PlatformIO", "GitHub Actions", "Autodesk Fusion",
                 "3D printing", "Unity 3D"]),
]


def stack(t):
    g, y = [], 8
    label_w, x0, pill_h, gap = 120, 120, 26, 8
    for label, items in STACK:
        row_y = y
        x = x0
        g.append(small_caps(label, 15, 12, 0, y + 18, t["accent"], spacing="0.9"))
        for it in items:
            w = len(it) * 6.9 + 22
            if x + w > W:
                x = x0
                y += pill_h + gap
            g.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{pill_h}" rx="13" fill="none" '
                     f'stroke="{t["rule"]}"/>')
            g.append(text(f"{x + w / 2:.1f}", y + 18, it, 14, t["ink"], anchor="middle"))
            x += w + gap
        y += pill_h + 14
        g.append(f'<line x1="0" y1="{y - 7}" x2="{W}" y2="{y - 7}" stroke="{t["faint"]}" stroke-width="0.8"/>')
    alt = "; ".join(f"{a}: {', '.join(b)}" for a, b in STACK)
    return svg(W, y, "".join(g), alt)


SECTIONS = ["Profile", "Currently", "Selected Projects", "More Projects", "Technical Skills",
            "Background", "Beyond Code"]


def slug(s):
    return s.lower().replace(" & ", "-").replace(" ", "-")


for old in OUT.glob("*.svg"):
    old.unlink()
for mode, t in THEMES.items():
    (OUT / f"header-{mode}.svg").write_text(header(t), encoding="utf-8")
    (OUT / f"stack-{mode}.svg").write_text(stack(t), encoding="utf-8")
    for s in SECTIONS:
        (OUT / f"{slug(s)}-{mode}.svg").write_text(section(s, t), encoding="utf-8")
    for spec in CARDS:
        (OUT / f"card-{spec[0]}-{mode}.svg").write_text(card(spec, t), encoding="utf-8")
