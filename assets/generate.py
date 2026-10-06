"""Generates every SVG graphic used by README.md, in a light and a dark variant.

Run from the repository root:  python3 assets/generate.py
Standard library only. Everything is deterministic (fixed random seeds).
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).parent
FONT = "'EB Garamond', Garamond, 'Times New Roman', Georgia, serif"
THEMES = {
    "light": {"ink": "#111111", "muted": "#555555", "rule": "#999999", "faint": "#d9d9d9",
              "accent": "#A51C30", "card": "#FAFAFA", "bg": "#FFFFFF"},
    "dark": {"ink": "#e8e8e8", "muted": "#a8a8a8", "rule": "#6b6b6b", "faint": "#30363d",
             "accent": "#E8788A", "card": "#161B22", "bg": "#0D1117"},
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


# ---------------------------------------------------------------- LiDAR scene
def lidar_scene(cx, cy, R, t, n=170, rings=4, sweep=True, seed=7):
    """A 2D LiDAR scan: range rings, a wobbly room, three obstacles, a sweeping beam."""
    rnd = random.Random(seed)
    g = []
    for i in range(1, rings + 1):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{R * i / rings:.1f}" fill="none" '
                 f'stroke="{t["faint"]}" stroke-width="0.8"/>')
    for k in range(12):
        a = math.radians(k * 30)
        g.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + R * math.cos(a):.1f}" y2="{cy + R * math.sin(a):.1f}" '
                 f'stroke="{t["faint"]}" stroke-width="0.6"/>')
    obstacles = [(0.45 * R, math.radians(40), 0.14 * R), (0.5 * R, math.radians(215), 0.12 * R),
                 (0.3 * R, math.radians(300), 0.10 * R)]
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        r = R * (0.80 + 0.10 * math.sin(3 * th + 0.6) + 0.05 * math.sin(7 * th)) + rnd.uniform(-0.8, 0.8)
        hit = False
        for od, oa, orad in obstacles:
            ox, oy = od * math.cos(oa), od * math.sin(oa)
            dx, dy = math.cos(th), math.sin(th)
            b = dx * ox + dy * oy
            disc = b * b - (ox * ox + oy * oy - orad * orad)
            if disc >= 0:
                s = b - math.sqrt(disc)
                if 0 < s < r:
                    r, hit = s, True
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th), hit))
    if sweep:
        a1, a2 = math.radians(-62), math.radians(-28)
        p1 = (cx + R * math.cos(a1), cy + R * math.sin(a1))
        p2 = (cx + R * math.cos(a2), cy + R * math.sin(a2))
        g.append(f'<path d="M{cx} {cy} L{p1[0]:.1f} {p1[1]:.1f} A{R} {R} 0 0 1 {p2[0]:.1f} {p2[1]:.1f} Z" '
                 f'fill="{t["accent"]}" fill-opacity="0.13"/>')
        g.append(f'<line x1="{cx}" y1="{cy}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{t["accent"]}" '
                 f'stroke-width="1.2"/>')
    pr = max(1.0, R / 52)
    for x, y, hit in pts:
        c, o = (t["accent"], 0.95) if hit else (t["ink"], 0.55)
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pr:.1f}" fill="{c}" fill-opacity="{o}"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{max(2.2, R / 28):.1f}" fill="{t["accent"]}"/>')
    return "".join(g)


# ---------------------------------------------------------------- banner and figures
def header(t):
    name = small_caps("Yiğit Salih Emecen", 42, 33, 0, 92, t["ink"], spacing="1.2")
    body = [name,
            text(2, 124, "Robotics and software engineer", 21, t["muted"], style="italic"),
            small_caps("M.Sc. Manufacturing & Robotics, TU Wien", 14, 11.5, 2, 152, t["muted"],
                       spacing="1", weight="400"),
            lidar_scene(660, 94, 86, t),
            rule(190, t)]
    return svg(W, 196, "".join(body), "Yiğit Salih Emecen, robotics and software engineer")


X0, X1 = 2020.5, 2027.0  # timeline axis, in years


def tx(year):
    return (year - X0) / (X1 - X0) * W


def timeline(t):
    """Education, work and projects on one time axis. Bars that are still running fade out to the right."""
    bg = t["bg"]
    g = [f'<defs><linearGradient id="fa" x1="0" x2="1"><stop offset="0.7" stop-color="{t["accent"]}"/>'
         f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0.35"/></linearGradient>'
         f'<linearGradient id="fi" x1="0" x2="1"><stop offset="0.7" stop-color="{t["ink"]}"/>'
         f'<stop offset="1" stop-color="{t["ink"]}" stop-opacity="0.35"/></linearGradient></defs>']
    for yr in range(2021, 2027):
        x = tx(yr)
        g.append(f'<line x1="{x:.1f}" y1="26" x2="{x:.1f}" y2="176" stroke="{t["faint"]}" stroke-width="0.8"/>')
        g.append(text(f"{x:.1f}", 194, str(yr), 12.5, t["muted"], anchor="middle"))
    g.append(f'<line x1="0" y1="176" x2="{W}" y2="176" stroke="{t["rule"]}"/>')

    def bar(y, h, a, b, fill, label=None, lab_fill=None):
        out = [f'<rect x="{tx(a):.1f}" y="{y}" width="{tx(b) - tx(a):.1f}" height="{h}" rx="3" fill="{fill}"/>']
        if label:
            centered = tx(b) - tx(a) > 300
            lx = (tx(a) + tx(b)) / 2 if centered else tx(a) + 10
            out.append(text(f"{lx:.1f}", y + h / 2 + 4.3, label, 12.5, lab_fill or bg,
                            anchor="middle" if centered else "start", weight="500"))
        return "".join(out)

    # education
    g.append(bar(34, 24, 2020.58, 2025.58, t["ink"], "B.Sc. Electrical & Electronics Engineering, İstanbul Ticaret"))
    g.append(bar(34, 24, 2026.17, X1, "url(#fi)", "M.Sc. TU Wien"))
    # work
    g.append(text(f"{tx(2024.08) - 8:.1f}", 83, "Exchange, FH Technikum", 12.5, t["muted"], anchor="end", style="italic"))
    g.append(bar(66, 24, 2024.08, 2024.58, t["muted"]))
    g.append(text(f"{tx(2025.5) - 8:.1f}", 83, "Robotics intern", 12.5, t["muted"], anchor="end", style="italic"))
    g.append(bar(66, 24, 2025.5, 2025.67, t["muted"]))
    g.append(bar(66, 24, 2025.75, X1, "url(#fa)", "TU Wien IFT"))
    # projects: running bars, then single-moment dots
    for a, b, label in [(2024.67, 2025.92, "Open LiDAR"), (2026.33, X1, "YellowBoy")]:
        g.append(bar(100, 8, a, b, t["accent"] if b == X1 else t["muted"]))
        g.append(text(f"{tx(a) + 2:.1f}", 126, label, 12.5, t["ink"]))
    for yr, label in [(2023.42, "Wireless MIDI"), (2025.5, "Milestone Award"), (2026.67, "PolarBot")]:
        x = tx(yr)
        g.append(f'<circle cx="{x:.1f}" cy="146" r="4.5" fill="{bg}" stroke="{t["accent"]}" stroke-width="2"/>')
        g.append(text(f"{x:.1f}", 166, label, 12.5, t["ink"], anchor="middle"))
    now = tx(2026.77)
    g.append(f'<line x1="{now:.1f}" y1="22" x2="{now:.1f}" y2="112" stroke="{t["accent"]}" stroke-width="1" '
             f'stroke-dasharray="3 3"/>')
    g.append(small_caps("Now", 12, 10, f"{now:.1f}", 14, t["accent"], spacing="1", anchor="middle"))
    alt = ("Timeline: B.Sc. at Istanbul Ticaret 2020 to 2025, exchange semester at FH Technikum Wien 2024, "
           "robotics internship 2025, TU Wien IFT since Oct 2025, M.Sc. at TU Wien since Mar 2026; projects "
           "Wireless MIDI 2023, Open LiDAR 2024 to 2025, Milestone Award 2025, YellowBoy 2026, PolarBot 2026")
    return svg(W, 204, "".join(g), alt)


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
    rnd = random.Random(3)
    g = [f'<rect x="21" y="4" width="54" height="88" rx="5" fill="none" stroke="{t["ink"]}" stroke-width="1.5"/>',
         f'<rect x="27" y="10" width="42" height="34" rx="2" fill="none" stroke="{t["muted"]}"/>']
    for gx in range(7):
        for gy in range(5):
            if rnd.random() < 0.42:
                g.append(f'<rect x="{29 + gx * 5.6:.1f}" y="{12.5 + gy * 6.2:.1f}" width="4.6" height="5.2" '
                         f'fill="{t["accent"]}"/>')
    g += [f'<rect x="30" y="62" width="16" height="4.5" fill="{t["ink"]}"/>',
          f'<rect x="35.75" y="56.25" width="4.5" height="16" fill="{t["ink"]}"/>',
          f'<circle cx="58" cy="68" r="4" fill="none" stroke="{t["ink"]}" stroke-width="1.4"/>',
          f'<circle cx="67" cy="61" r="4" fill="none" stroke="{t["ink"]}" stroke-width="1.4"/>',
          f'<line x1="32" y1="82" x2="40" y2="78" stroke="{t["muted"]}" stroke-width="1.6"/>',
          f'<line x1="44" y1="82" x2="52" y2="78" stroke="{t["muted"]}" stroke-width="1.6"/>']
    return "".join(g)


def icon_lidar(t):
    return lidar_scene(48, 48, 44, t, n=90, rings=3, seed=11)


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


def icon_midi(t):
    g = [f'<g transform="rotate(-24 48 66)"><rect x="30" y="56" width="36" height="20" rx="3" fill="none" '
         f'stroke="{t["ink"]}" stroke-width="1.5"/><circle cx="40" cy="66" r="2" fill="{t["ink"]}"/>'
         f'<circle cx="56" cy="66" r="2" fill="{t["ink"]}"/></g>']
    for i, r in enumerate((14, 26, 38)):
        a1, a2 = math.radians(-135), math.radians(-45)
        p1 = (48 + r * math.cos(a1), 44 + r * math.sin(a1))
        p2 = (48 + r * math.cos(a2), 44 + r * math.sin(a2))
        g.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{r} {r} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" fill="none" '
                 f'stroke="{t["accent"]}" stroke-width="1.6" stroke-linecap="round"/>')
    g.append(f'<circle cx="48" cy="44" r="2.5" fill="{t["accent"]}"/>')
    return "".join(g)


def icon_ransac(t):
    rnd = random.Random(5)
    g = [f'<polygon points="4,78 4,58 92,22 92,42" fill="{t["accent"]}" fill-opacity="0.10"/>',
         f'<line x1="4" y1="68" x2="92" y2="32" stroke="{t["accent"]}" stroke-width="1.6"/>']
    for _ in range(26):
        x = rnd.uniform(6, 90)
        y = 68 - (x - 4) * 36 / 88 + rnd.uniform(-7, 7)
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{t["accent"]}"/>')
    for _ in range(9):
        g.append(f'<circle cx="{rnd.uniform(6, 90):.1f}" cy="{rnd.uniform(6, 90):.1f}" r="2" fill="none" '
                 f'stroke="{t["muted"]}" stroke-width="1.1"/>')
    return "".join(g)


CARDS = [
    ("polarbot", "PolarBot", "ESP8266 · JavaScript", icon_polar,
     ["A €5 WiFi plotter with polar", "kinematics and fully 3D-printed", "parts. Browser control panel."]),
    ("yellowboy", "YellowBoy", "C++ · ESP32", icon_gameboy,
     ["A Game Boy emulator that fits in", "the ESP32's internal SRAM, no", "PSRAM. Analog audio, SD ROMs."]),
    ("open-lidar", "Open LiDAR", "Python · C++", icon_lidar,
     ["Open source 360° LiDAR and robot", "platform. 240 Hz real-time", "mapping, slip ring removed."]),
    ("cycloidal", "Cycloidal Gear Generator", "JavaScript · live demo", icon_cycloid,
     ["Design a cycloidal reduction by", "tuning every parameter, right", "in the browser."]),
    ("tree-gen", "Tree-Gen", "JavaScript · live demo", icon_tree,
     ["Generates a wide variety of tree", "models you can download.", "Free, runs in the browser."]),
    ("engine-sim", "Engine Sim", "JavaScript · live demo", icon_wave,
     ["A realistic engine sound", "simulator that runs in your", "browser."]),
    ("midi", "Wireless MIDI Control", "C++ · ESP8266", icon_midi,
     ["Tilt-sensing device that streams", "MIDI over WiFi (RTP-MIDI) to", "control guitar effects."]),
    ("ransac", "RANSAC Visualiser", "C#", icon_ransac,
     ["Shows how RANSAC works on", "simulated LiDAR point-cloud", "data."]),
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


SECTIONS = ["Timeline", "Profile", "Currently", "Selected Projects", "More Projects", "Technical Skills",
            "Background", "Recognition", "Beyond Code"]


def slug(s):
    return s.lower().replace(" & ", "-").replace(" ", "-")


for old in OUT.glob("*.svg"):
    old.unlink()
for mode, t in THEMES.items():
    (OUT / f"header-{mode}.svg").write_text(header(t), encoding="utf-8")
    (OUT / f"career-{mode}.svg").write_text(timeline(t), encoding="utf-8")
    (OUT / f"stack-{mode}.svg").write_text(stack(t), encoding="utf-8")
    for s in SECTIONS:
        (OUT / f"{slug(s)}-{mode}.svg").write_text(section(s, t), encoding="utf-8")
    for spec in CARDS:
        (OUT / f"card-{spec[0]}-{mode}.svg").write_text(card(spec, t), encoding="utf-8")
