"""Generates the SVG graphics used by README.md (light and dark variants).

Run from the repository root:  python3 assets/generate.py
"""
from pathlib import Path

OUT = Path(__file__).parent
FONT = "'EB Garamond', Garamond, 'Times New Roman', Georgia, serif"
THEMES = {
    "light": {"ink": "#111111", "muted": "#555555", "rule": "#999999"},
    "dark": {"ink": "#e8e8e8", "muted": "#a8a8a8", "rule": "#6b6b6b"},
}
WIDTH = 800


def small_caps(text, big, small, x, y, fill, spacing="0.6", weight="700"):
    """Small caps built from two font sizes, so it renders the same everywhere."""
    parts = []
    for i, word in enumerate(text.split(" ")):
        if i:
            parts.append(f'<tspan font-size="{small}"> </tspan>')
        if word == "&":
            parts.append(f'<tspan font-size="{small}">&amp;</tspan>')
            continue
        parts.append(f'<tspan font-size="{big}">{word[0].upper()}</tspan>'
                     f'<tspan font-size="{small}">{word[1:].upper()}</tspan>')
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{FONT}" font-weight="{weight}" '
            f'letter-spacing="{spacing}">{"".join(parts)}</text>')


def svg(width, height, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def header(t):
    name = small_caps("Yiğit Salih Emecen", 40, 31, WIDTH / 2, 52, t["ink"], spacing="1.2")
    name = name.replace("<text ", '<text text-anchor="middle" ', 1)
    sub = (f'<text x="{WIDTH / 2}" y="82" text-anchor="middle" fill="{t["muted"]}" '
           f'font-family="{FONT}" font-style="italic" font-size="17">'
           f'Robotics and software engineer, Vienna, Austria</text>')
    return svg(WIDTH, 98, name + sub, "Yiğit Salih Emecen")


def section(title, t):
    text = small_caps(title, 21, 16.5, 0, 24, t["ink"], weight="400")
    rule = f'<line x1="0" y1="33" x2="{WIDTH}" y2="33" stroke="{t["rule"]}" stroke-width="1"/>'
    return svg(WIDTH, 38, text + rule, title)


SECTIONS = ["Profile", "Education", "Experience", "Selected Projects",
            "More Projects", "Awards & Publications", "Technical Skills",
            "Languages & Interests"]


def slug(s):
    return s.lower().replace(" & ", "-").replace(" ", "-")


for mode, t in THEMES.items():
    (OUT / f"header-{mode}.svg").write_text(header(t), encoding="utf-8")
    for s in SECTIONS:
        (OUT / f"{slug(s)}-{mode}.svg").write_text(section(s, t), encoding="utf-8")
