"""
Hand-drawn SVG illustrations: anatomical heart, ECG monitor, stethoscope, blood cells,
botanical sprigs and small icon tiles. Embedded as base64 <img> tags, so no image files
are needed. To use a real photo instead, drop `hero.jpg` (or .png/.webp) into /assets
and the Home page will show it automatically.
"""
from __future__ import annotations

import base64
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

_DEFS = """
<defs>
  <radialGradient id="body" cx="42%" cy="32%" r="78%">
    <stop offset="0" stop-color="#F26B6B"/><stop offset="0.38" stop-color="#D62839"/>
    <stop offset="0.75" stop-color="#9E1420"/><stop offset="1" stop-color="#5E0B14"/>
  </radialGradient>
  <linearGradient id="vessel" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#EF4B55"/><stop offset="1" stop-color="#8F1220"/>
  </linearGradient>
  <linearGradient id="vein" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#B3202F"/><stop offset="1" stop-color="#5E0B14"/>
  </linearGradient>
  <radialGradient id="shine" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="halo" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#F9A8A0" stop-opacity=".75"/><stop offset=".6" stop-color="#FAD1CB" stop-opacity=".35"/>
    <stop offset="1" stop-color="#FFF1EE" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cell" cx="40%" cy="35%" r="75%">
    <stop offset="0" stop-color="#F58B8B"/><stop offset=".6" stop-color="#D62839"/><stop offset="1" stop-color="#8F1220"/>
  </radialGradient>
  <linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#9CBF9B"/><stop offset="1" stop-color="#4F7A57"/>
  </linearGradient>
  <linearGradient id="tile" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFE3DE"/><stop offset="1" stop-color="#F9B8B0"/>
  </linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F4DAD6"/><stop offset=".5" stop-color="#B98B8E"/><stop offset="1" stop-color="#6B3B43"/>
  </linearGradient>
  <linearGradient id="ecgfade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff" stop-opacity="1"/>
    <stop offset=".88" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
"""


def _svg(view_box: str, body: str, style: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}"><style>{style}</style>{_DEFS}{body}</svg>')


def img(svg: str, width: str = "100%", extra_style: str = "", alt: str = "illustration") -> str:
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return (f'<img alt="{alt}" src="data:image/svg+xml;base64,{b64}" '
            f'style="width:{width};max-width:100%;height:auto;{extra_style}"/>')


def photo_or(fallback_svg_html: str, name: str = "hero") -> str:
    """Return an <img> of assets/<name>.(jpg|jpeg|png|webp) if present, else the fallback html."""
    for ext, mime in (("jpg", "jpeg"), ("jpeg", "jpeg"), ("png", "png"), ("webp", "webp")):
        p = ASSETS / f"{name}.{ext}"
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode("ascii")
            return (f'<img alt="{name}" src="data:image/{mime};base64,{b64}" '
                    f'style="width:100%;border-radius:28px;box-shadow:0 30px 70px rgba(122,17,19,.28);object-fit:cover"/>')
    return fallback_svg_html


# ------------------------------------------------------------------------------ the heart
BODY_PATH = ("M214 392 C130 330 66 262 66 188 C66 130 108 96 156 104 C186 109 204 126 216 146 "
             "C232 118 262 100 300 106 C352 114 378 164 366 214 C352 280 290 338 214 392 Z")
AORTA_PATH = "M236 152 C238 94 252 54 292 52 C326 50 342 84 334 124"
PULM_PATH = "M198 142 C184 98 162 76 126 78"
VENA_PATH = "M264 122 C272 92 274 66 270 34"


def heart(bpm: int = 72, width_class: str = "") -> str:
    """Anatomical-style heart that beats at the given BPM."""
    dur = max(0.4, min(60 / max(bpm, 30), 1.6))
    style = (f".beat{{transform-box:fill-box;transform-origin:50% 55%;animation:beat {dur:.2f}s ease-in-out infinite}}"
             f".halo{{transform-box:fill-box;transform-origin:center;animation:halo {dur:.2f}s ease-in-out infinite}}"
             "@keyframes beat{0%,100%{transform:scale(1)}14%{transform:scale(1.055)}28%{transform:scale(1)}"
             "42%{transform:scale(1.035)}56%{transform:scale(1)}}"
             "@keyframes halo{0%,100%{transform:scale(.96);opacity:.7}14%{transform:scale(1.08);opacity:1}"
             "28%{transform:scale(.98);opacity:.8}}")
    body = f"""
    <circle class="halo" cx="220" cy="220" r="205" fill="url(#halo)"/>
    <ellipse cx="220" cy="418" rx="130" ry="11" fill="#7B1113" fill-opacity=".22" filter="url(#soft)"/>
    <g class="beat">
      <path d="{VENA_PATH}" fill="none" stroke="url(#vein)" stroke-width="24" stroke-linecap="round"/>
      <path d="{PULM_PATH}" fill="none" stroke="url(#vessel)" stroke-width="30" stroke-linecap="round"/>
      <path d="{AORTA_PATH}" fill="none" stroke="url(#vessel)" stroke-width="40" stroke-linecap="round"/>
      <path d="{AORTA_PATH}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="9" stroke-linecap="round" transform="translate(-7 -4)"/>
      <path d="M334 124 L334 150" stroke="url(#vessel)" stroke-width="30" stroke-linecap="round" fill="none" opacity=".0"/>
      <path d="{BODY_PATH}" fill="url(#body)"/>
      <path d="M216 148 C204 205 208 270 214 372" fill="none" stroke="#5E0B14" stroke-opacity=".35" stroke-width="5" stroke-linecap="round"/>
      <path d="M152 112 C118 146 108 204 128 262 M130 262 C150 292 176 316 200 340" fill="none" stroke="#FF9F94" stroke-opacity=".85" stroke-width="4" stroke-linecap="round"/>
      <path d="M300 112 C342 146 350 206 330 262 M330 262 C312 292 268 322 230 352" fill="none" stroke="#FF9F94" stroke-opacity=".85" stroke-width="4" stroke-linecap="round"/>
      <path d="M126 182 C150 176 170 186 184 206 M340 190 C316 186 296 198 284 220 M148 230 C170 224 188 236 198 256" fill="none" stroke="#FF9F94" stroke-opacity=".6" stroke-width="3" stroke-linecap="round"/>
      <ellipse cx="130" cy="150" rx="46" ry="26" transform="rotate(-38 130 150)" fill="url(#shine)"/>
      <ellipse cx="318" cy="156" rx="26" ry="14" transform="rotate(-36 318 156)" fill="url(#shine)" opacity=".6"/>
    </g>
    <g fill="#fff" fill-opacity=".0"><circle cx="0" cy="0" r="1"/></g>
    """
    return _svg("0 0 440 440", body, style)


def pulse_heart_icon() -> str:
    """Small flat heart with an ECG line, used as the brand logo."""
    body = """
    <path d="M60 104 C24 78 10 56 10 36 C10 18 24 8 40 8 C50 8 57 13 60 21 C63 13 70 8 80 8 C96 8 110 18 110 36 C110 56 96 78 60 104 Z" fill="url(#body)"/>
    <polyline points="14,54 40,54 50,38 62,76 72,48 80,54 106,54" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    """
    return _svg("0 0 120 112", body)


# ------------------------------------------------------------------------------ ECG strip
def ecg_strip(color: str = "#C1121F", height: int = 140) -> str:
    """Scrolling monitor-style ECG trace (PQRST complex repeated)."""
    period = 300
    seg = ("l 40 0 c 6 -14 22 -14 28 0 l 18 0 l 8 8 l 8 -62 l 10 78 l 8 -24 l 22 0 "
           "c 8 -20 34 -20 42 0 l 66 0")
    # segment above totals 40+28+18+8+8+10+8+22+42+66 = 250 -> pad to 300
    path = "M0 70 " + (seg + " l 50 0 ") * 8
    mid = height / 2
    body = f"""
    <defs><mask id="m"><rect width="1200" height="{height}" fill="url(#ecgfade)"/></mask></defs>
    <g mask="url(#m)">
      <line x1="0" y1="{mid}" x2="1200" y2="{mid}" stroke="#F2B5AE" stroke-opacity=".5" stroke-dasharray="3 9"/>
      <g class="scroll"><path d="{path}" transform="translate(0 {mid - 70})" fill="none" stroke="{color}" stroke-opacity=".28" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="{path}" transform="translate(0 {mid - 70})" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></g>
    </g>
    """
    style = f".scroll{{animation:sc 7s linear infinite}}@keyframes sc{{from{{transform:translateX(0)}}to{{transform:translateX(-{period}px)}}}}"
    return _svg(f"0 0 1200 {height}", body, style)


def blood_cells() -> str:
    def cell(cx, cy, r, rot=0, op=1):
        return (f'<g transform="translate({cx} {cy}) rotate({rot})" opacity="{op}">'
                f'<ellipse rx="{r}" ry="{r * .92}" fill="url(#cell)"/>'
                f'<ellipse rx="{r * .5}" ry="{r * .42}" fill="#7B1113" fill-opacity=".38"/>'
                f'<ellipse cx="{-r * .25}" cy="{-r * .38}" rx="{r * .3}" ry="{r * .14}" fill="#fff" fill-opacity=".35" transform="rotate(-30)"/></g>')
    cells = "".join(cell(*c) for c in [(60, 70, 34, 10), (150, 120, 26, -20, .9), (230, 60, 30, 30, .95), (110, 190, 22, 5, .85),
                                       (210, 170, 36, -10), (290, 130, 20, 40, .8), (40, 160, 18, 0, .8)])
    return _svg("0 0 330 230", cells + '<style>g{}</style>')


def stethoscope() -> str:
    body = """
    <circle cx="150" cy="130" r="118" fill="url(#halo)"/>
    <path d="M60 30 V92 C60 128 84 148 112 148 C140 148 164 128 164 92 V30" fill="none" stroke="#6B3B43" stroke-width="9" stroke-linecap="round"/>
    <circle cx="60" cy="26" r="9" fill="url(#steel)"/><circle cx="164" cy="26" r="9" fill="url(#steel)"/>
    <path d="M112 148 V176 C112 214 146 232 182 220 C216 208 232 176 220 150" fill="none" stroke="#6B3B43" stroke-width="9" stroke-linecap="round"/>
    <circle cx="224" cy="132" r="30" fill="url(#steel)" stroke="#6B3B43" stroke-width="6"/>
    <circle cx="224" cy="132" r="17" fill="#F9D7D2"/><circle cx="224" cy="132" r="9" fill="#C1121F"/>
    """
    return _svg("0 0 300 260", body)


def leaf_sprig(flip: bool = False) -> str:
    leaves = ""
    for i, (x, y, r, s) in enumerate([(50, 150, -40, 1), (70, 118, 30, .95), (84, 92, -35, .9), (98, 66, 28, .8), (110, 40, -30, .7)]):
        leaves += (f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M0 0 C18 -34 56 -34 76 0 C56 34 18 34 0 0 Z" fill="url(#leaf)"/>'
                   f'<path d="M4 0 L70 0" stroke="#fff" stroke-opacity=".45" stroke-width="2"/></g>')
    body = f'<g transform="{"scale(-1 1) translate(-160 0)" if flip else ""}"><path d="M40 190 C60 130 90 80 122 18" fill="none" stroke="#4F7A57" stroke-width="4" stroke-linecap="round"/>{leaves}</g>'
    return _svg("0 0 160 200", body)


# ------------------------------------------------------------------------------ icon tiles
def _tile(inner: str) -> str:
    return _svg("0 0 96 96", f'<rect width="96" height="96" rx="26" fill="url(#tile)"/>{inner}')


def icon(name: str) -> str:
    R, D = "#C1121F", "#7B1113"
    icons = {
        "form": f'<rect x="28" y="20" width="40" height="56" rx="7" fill="#fff" stroke="{R}" stroke-width="4"/><rect x="38" y="14" width="20" height="12" rx="4" fill="{R}"/>'
                f'<path d="M48 60 C36 52 36 42 43 42 C46 42 48 44 48 46 C48 44 50 42 53 42 C60 42 60 52 48 60Z" fill="{R}"/>',
        "ai": f'<circle cx="48" cy="48" r="24" fill="#fff" stroke="{R}" stroke-width="4"/><polyline points="26,50 40,50 45,38 52,62 57,48 70,48" fill="none" stroke="{R}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
        "report": f'<rect x="26" y="18" width="44" height="60" rx="7" fill="#fff" stroke="{R}" stroke-width="4"/><rect x="34" y="30" width="28" height="5" rx="2.5" fill="{D}" opacity=".5"/>'
                  f'<rect x="34" y="42" width="20" height="5" rx="2.5" fill="{D}" opacity=".5"/><path d="M36 62 L44 70 L60 54" fill="none" stroke="{R}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
        "drop": f'<path d="M48 18 C48 18 28 42 28 56 C28 68 37 76 48 76 C59 76 68 68 68 56 C68 42 48 18 48 18Z" fill="{R}"/><ellipse cx="40" cy="54" rx="5" ry="9" fill="#fff" opacity=".45" transform="rotate(20 40 54)"/>',
        "apple": f'<path d="M48 32 C38 24 24 30 24 48 C24 64 36 78 44 78 C47 78 48 77 48 77 C48 77 49 78 52 78 C60 78 72 64 72 48 C72 30 58 24 48 32Z" fill="{R}"/><path d="M48 32 C48 24 52 18 60 16" stroke="#4F7A57" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M56 22 C62 14 70 16 70 16 C70 16 68 26 56 22Z" fill="#6B9A6F"/>',
        "moon": f'<path d="M60 20 C42 22 30 36 30 52 C30 68 42 78 58 78 C66 78 72 75 76 71 C58 70 48 60 48 46 C48 34 52 26 60 20Z" fill="{R}"/><circle cx="68" cy="30" r="3" fill="{D}"/><circle cx="76" cy="44" r="2" fill="{D}"/>',
        "bolt": f'<path d="M54 14 L28 54 H46 L40 82 L68 40 H50 Z" fill="{R}" stroke="{D}" stroke-width="2" stroke-linejoin="round"/>',
        "smoke": f'<rect x="20" y="56" width="42" height="11" rx="3" fill="#fff" stroke="{R}" stroke-width="3"/><rect x="50" y="56" width="12" height="11" rx="3" fill="{R}"/>'
                 f'<path d="M70 52 C64 44 76 40 70 30 M80 54 C74 46 86 42 80 32" fill="none" stroke="{D}" stroke-opacity=".7" stroke-width="3.5" stroke-linecap="round"/>',
        "scale": f'<rect x="22" y="28" width="52" height="44" rx="10" fill="#fff" stroke="{R}" stroke-width="4"/><path d="M34 46 A14 14 0 0 1 62 46" fill="none" stroke="{R}" stroke-width="4" stroke-linecap="round"/><line x1="48" y1="46" x2="55" y2="38" stroke="{D}" stroke-width="3.5" stroke-linecap="round"/>',
        "run": f'<circle cx="58" cy="26" r="7" fill="{R}"/><path d="M52 40 L42 54 L28 56 M52 40 L62 52 L72 50 M46 50 L50 66 L38 78 M50 66 L64 72" fill="none" stroke="{R}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>',
        "family": f'<circle cx="34" cy="34" r="8" fill="{R}"/><circle cx="62" cy="34" r="8" fill="{D}" opacity=".8"/><circle cx="48" cy="52" r="6" fill="{R}" opacity=".7"/><path d="M20 76 C20 62 48 62 48 76 M48 76 C48 62 76 62 76 76" fill="none" stroke="{R}" stroke-width="5" stroke-linecap="round"/>',
        "heart": f'<path d="M48 76 C26 60 20 48 20 38 C20 28 28 22 36 22 C42 22 46 25 48 30 C50 25 54 22 60 22 C68 22 76 28 76 38 C76 48 70 60 48 76Z" fill="{R}"/><ellipse cx="36" cy="36" rx="6" ry="4" fill="#fff" opacity=".4" transform="rotate(-30 36 36)"/>',
    }
    return _svg("0 0 96 96", f'<rect width="96" height="96" rx="26" fill="url(#tile)"/>{icons[name]}')
