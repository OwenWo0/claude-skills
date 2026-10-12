"""Tiny helpers for hand-drawn explainer figures.

Usage: copy this file next to your figure script, then

    from svgkit import *
    def fig_example():
        b = head("标题：一句话说清这张图", "副标题：告诉读者该看什么")
        b += R(32, 96, 160, 60, 12, WHITE, LINE, 1) + T(112, 132, "方框", 14, INK, "middle", 600)
        b += arrow(200, 126, 260, 126)
        save("01-example.svg", 800, 200, b, "示例")

All figures share one palette, a light card background (works in Notion light and
dark mode) and a CJK font stack, because SVGs shown as images cannot load web fonts.
"""
import math
import os

OUT = os.environ.get("FIG_OUT", "figs")

BG, INK, MUTE, LINE, CANVAS = "#F5F3EF", "#1A1917", "#7A756C", "#D8D3CA", "#E6E3DD"
ACC, ACC_SOFT, WARN, WHITE = "#2F5BEA", "#DDE5FD", "#B4502E", "#FFFFFF"
FONT = "'PingFang SC','Hiragino Sans GB','Noto Sans SC','Microsoft YaHei','WenQuanYi Zen Hei',sans-serif"
MONO = "'SF Mono',Menlo,Consolas,'WenQuanYi Zen Hei Mono',monospace"


def save(name, w, h, body, title):
    os.makedirs(OUT, exist_ok=True)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         f'font-family="{FONT}">\n<title>{title}</title>\n'
         f'<rect width="{w}" height="{h}" rx="18" fill="{BG}"/>\n{body}\n</svg>\n')
    with open(os.path.join(OUT, name), "w") as f:
        f.write(s)


def T(x, y, s, size=14, fill=INK, anchor="start", weight=400, family=None):
    """Text. anchor: start | middle | end."""
    fam = f' font-family="{family}"' if family else ""
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{fam}>{s}</text>'


def R(x, y, w, h, r=0, fill=INK, stroke="none", sw=1.5, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{op}"/>'


def L(x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}/>'


def C(cx, cy, r, fill=INK, stroke="none", sw=1.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def P(d, fill="none", stroke=INK, sw=2, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{ds}/>'


def diamond(x, y, r=7, fill=INK):
    """Keyframe marker."""
    return f'<path d="M{x} {y - r} L{x + r} {y} L{x} {y + r} L{x - r} {y} Z" fill="{fill}"/>'


def arrow(x1, y1, x2, y2, color=INK, sw=1.8):
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(a), y2 - 9 * math.sin(a)
    p1 = (hx + 5 * math.sin(a), hy - 5 * math.cos(a))
    p2 = (hx - 5 * math.sin(a), hy + 5 * math.cos(a))
    return (L(x1, y1, hx, hy, color, sw) +
            f'<path d="M{x2:.1f} {y2:.1f} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" fill="{color}"/>')


def head(title, sub=None):
    """Figure title (top-left) + one-line subtitle saying what to look at."""
    s = T(32, 42, title, 19, INK, weight=600)
    if sub:
        s += T(32, 66, sub, 13.5, MUTE)
    return s


def pill(x, y, s, highlight=False):
    """Rounded label centred at (x, y); width estimated for mixed CJK/Latin text."""
    w = sum(8.6 if ch.isascii() else 14 for ch in s) + 26
    return (R(x - w / 2, y - 15, w, 30, 15, ACC if highlight else BG, ACC if highlight else LINE, 1) +
            T(x, y + 5, s, 13, WHITE if highlight else INK, "middle", 600))


def spring(t, w, z):
    """Closed-form spring step response (0 -> 1)."""
    if z < 1:
        wd = w * math.sqrt(1 - z * z)
        return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z * w / wd * math.sin(wd * t))
    return 1 - math.exp(-w * t) * (1 + w * t)


def smoother(u):
    u = max(0.0, min(1.0, u))
    return u * u * u * (u * (u * 6 - 15) + 10)


def poly(f, x0, y0, w, h, n=120, tmax=1.0, vmin=0.0, vmax=1.0):
    """Path for y = f(t), t in [0, tmax], drawn in the box (x0, y0, w, h).
    Give vmax > 1 when the curve can overshoot, or it will leave the box."""
    pts = []
    for i in range(n + 1):
        t = i / n
        v = (f(t * tmax) - vmin) / (vmax - vmin)
        pts.append(f"{x0 + t * w:.1f},{y0 + h - v * h:.1f}")
    return "M" + " L".join(pts)
