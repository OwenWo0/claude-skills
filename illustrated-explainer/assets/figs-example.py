"""Generate the SVG illustrations for the beginner guide -> guide/figs/*.svg"""
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "guide", "figs")
os.makedirs(OUT, exist_ok=True)

BG, INK, MUTE, LINE, CANVAS = "#F5F3EF", "#1A1917", "#7A756C", "#D8D3CA", "#E6E3DD"
ACC, ACC_SOFT, WHITE = "#2F5BEA", "#DDE5FD", "#FFFFFF"
FONT = "'PingFang SC','Hiragino Sans GB','Noto Sans SC','Microsoft YaHei','WenQuanYi Zen Hei',sans-serif"
MONO = "'SF Mono',Menlo,Consolas,'WenQuanYi Zen Hei Mono',monospace"


def svg(name, w, h, body, title):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         f'font-family="{FONT}">\n<title>{title}</title>\n'
         f'<rect width="{w}" height="{h}" rx="18" fill="{BG}"/>\n{body}\n</svg>\n')
    open(os.path.join(OUT, name), "w").write(s)


def T(x, y, s, size=14, fill=INK, anchor="start", weight=400, family=None):
    fam = f' font-family="{family}"' if family else ""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{fam}>{s}</text>'


def R(x, y, w, h, r=0, fill=INK, stroke="none", sw=1.5, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{op}"/>'


def L(x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>'


def C(cx, cy, r, fill=INK, stroke="none", sw=1.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def P(d, fill="none", stroke=INK, sw=2, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{ds}/>'


def arrow(x1, y1, x2, y2, color=INK, sw=1.8):
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(a), y2 - 9 * math.sin(a)
    p1 = (hx + 5 * math.sin(a), hy - 5 * math.cos(a))
    p2 = (hx - 5 * math.sin(a), hy + 5 * math.cos(a))
    return (L(x1, y1, hx, hy, color, sw) +
            f'<path d="M{x2:.1f} {y2:.1f} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" fill="{color}"/>')


def head(title, sub=None):
    s = T(32, 42, title, 19, INK, weight=600)
    if sub:
        s += T(32, 66, sub, 13.5, MUTE)
    return s


def spring(t, w, z):
    if z < 1:
        wd = w * math.sqrt(1 - z * z)
        return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z * w / wd * math.sin(wd * t))
    return 1 - math.exp(-w * t) * (1 + w * t)


def smoother(u):
    u = max(0, min(1, u))
    return u * u * u * (u * (u * 6 - 15) + 10)


def poly(f, x0, y0, w, h, n=120, tmax=1.0, vmin=0.0, vmax=1.0):
    pts = []
    for i in range(n + 1):
        t = i / n
        v = (f(t * tmax) - vmin) / (vmax - vmin)
        pts.append(f"{x0 + t * w:.1f},{y0 + h - v * h:.1f}")
    return "M" + " L".join(pts)


# ---------------------------------------------------------------- 1. frames
def fig_frames():
    b = head("动画 = 一张张静止的画，快速翻过去", "每秒 60 张。这支 14 秒的动画，其实是 840 张图片。")
    b += R(24, 88, 752, 196, 10, INK)
    for i in range(24):
        b += R(36 + i * 31.2, 96, 16, 10, 3, "#3A3835")
        b += R(36 + i * 31.2, 266, 16, 10, 3, "#3A3835")
    labels = [("第 0 帧", "0.00 s"), ("第 60 帧", "1.00 s"), ("第 90 帧", "1.50 s"),
              ("第 138 帧", "2.30 s"), ("第 168 帧", "2.80 s"), ("第 240 帧", "4.00 s")]
    for i, (a, t) in enumerate(labels):
        x, y = 40 + i * 122, 116
        b += R(x, y, 110, 140, 6, CANVAS)
        cx, cy = x + 55, y + 62
        if i == 0:
            b += R(cx - 38, cy - 12, 76, 24, 12, INK) + R(cx - 22, cy - 2, 44, 4, 2, WHITE)
        elif i == 1:
            b += R(cx - 33, cy - 11, 66, 22, 11, INK)
        elif i == 2:
            b += C(cx, cy, 17) + P(f"M{cx} {cy - 10} A10 10 0 0 1 {cx + 10} {cy}", stroke=WHITE, sw=3)
        elif i == 3:
            b += C(cx, cy, 17) + P(f"M{cx - 7} {cy} L{cx - 2} {cy + 5} L{cx + 8} {cy - 5}", stroke=WHITE, sw=3)
        elif i == 4:
            b += R(cx - 44, cy - 11, 88, 22, 11, INK) + R(cx - 38, cy - 7, 14, 14, 4, "#555")
            for k in range(4):
                hh = [8, 12, 6, 10][k]
                b += R(cx + 22 + k * 5, cy - hh / 2, 2.5, hh, 1, WHITE)
        else:
            b += R(cx - 44, cy - 30, 88, 60, 8, WHITE, LINE, 1)
            b += R(cx - 36, cy - 22, 20, 20, 4, INK) + R(cx - 10, cy - 18, 34, 4, 2, INK) + R(cx - 10, cy - 10, 22, 3, 1.5, MUTE)
            b += R(cx - 36, cy + 8, 72, 3, 1.5, LINE) + R(cx - 36, cy + 8, 26, 3, 1.5, INK) + C(cx, cy + 20, 5)
        b += T(cx, y + 116, a, 12.5, INK, "middle", 600)
        b += T(cx, y + 132, t, 11.5, MUTE, "middle", family=MONO)
    b += T(400, 312, "相邻两帧只差一点点，眼睛就会把它们连成运动。", 13.5, MUTE, "middle")
    svg("01-frames.svg", 800, 330, b, "动画由帧组成")


# ---------------------------------------------------------------- 2. keyframes + interpolation
def fig_keyframes():
    b = head("关键帧：你只定两头，中间交给电脑", "按钮（宽 140）要在 0.5 秒内变成圆（宽 48）。中间每一帧的宽度，都是算出来的。")
    us = [0, .25, .5, .75, 1]
    ys = 150
    for u in us:
        x = 120 + u * 520
        w = 140 + (48 - 140) * u
        key = u in (0, 1)
        if key:
            b += R(x - w / 2, ys - 24, w, 48, 24, INK)
        else:
            b += R(x - w / 2, ys - 24, w, 48, 24, ACC_SOFT, ACC, 1.5, "5 4")
        b += T(x, ys + 46, f"宽 {w:.0f}", 12.5, INK if key else ACC, "middle", family=MONO)
    b += T(120, 104, "关键帧 A（你定）", 13, INK, "middle", 600)
    b += T(640, 104, "关键帧 B（你定）", 13, INK, "middle", 600)
    b += T(380, 104, "中间帧（电脑算）", 13, ACC, "middle", 600)
    ty = 232
    b += L(100, ty, 660, ty, LINE, 3)
    for u in us:
        x = 120 + u * 520
        if u in (0, 1):
            b += f'<path d="M{x} {ty - 9} L{x + 9} {ty} L{x} {ty + 9} L{x - 9} {ty} Z" fill="{INK}"/>'
        else:
            b += C(x, ty, 5, ACC)
        b += T(x, ty + 28, f"u = {u:g}", 12, MUTE, "middle", family=MONO)
    b += T(676, ty + 4, "进度", 12, MUTE)
    b += R(150, 286, 500, 58, 12, WHITE, LINE, 1)
    b += T(400, 310, "值 = A + (B − A) × u", 16, INK, "middle", 600, MONO)
    b += T(400, 332, "u = 0.5 时：140 + (48 − 140) × 0.5 = 94", 12.5, MUTE, "middle", family=MONO)
    svg("02-keyframes.svg", 800, 364, b, "关键帧与插值")


# ---------------------------------------------------------------- 3. easing
def fig_easing():
    b = head("缓动：同样 1 秒，「怎么走」决定了手感", "上排的点按相同时间间隔取样：点越稀，说明那一段越快。")
    cases = [
        ("匀速", lambda t: t, "机械、像机器人", MUTE),
        ("缓入缓出", smoother, "自然，起步和停下都柔和", INK),
        ("弹簧（克制）", lambda t: spring(t, 9, .86), "本项目的手感：快出、轻落", ACC),
        ("弹簧（过头）", lambda t: spring(t, 12, .3), "像玩具，晃个不停", "#B4502E"),
    ]
    for i, (name, f, note, col) in enumerate(cases):
        x0 = 32 + i * 188
        b += T(x0, 104, name, 14.5, INK, weight=600)
        # dot trail
        b += L(x0, 126, x0 + 132, 126, LINE, 1.5) + L(x0 + 132, 118, x0 + 132, 134, ACC, 1.5)
        for k in range(11):
            v = f(k / 10)
            b += C(x0 + 132 * v, 126, 4, col)
        # plot
        px, py, pw, ph = x0, 148, 164, 130
        b += R(px, py, pw, ph, 6, WHITE, LINE, 1)
        lo, hi = -0.05, 1.75
        ty_ = py + 10 + (ph - 28) * (1 - (1 - lo) / (hi - lo))
        b += L(px + 6, ty_, px + pw - 6, ty_, LINE, 1, "3 4") + T(px + pw - 8, ty_ - 4, "终点", 10, MUTE, "end")
        b += P(poly(f, px + 6, py + 10, pw - 12, ph - 28, vmin=lo, vmax=hi), stroke=col, sw=2.5)
        b += T(px + 6, py + ph - 6, "时间 →", 10.5, MUTE)
        b += T(x0, 304, note, 12.5, MUTE)
    b += T(32, 340, "规律：真实世界的东西不会瞬间到达满速，也不会急刹。给运动加上「速度的形状」，它就活了。", 13.5, INK)
    svg("03-easing.svg", 800, 362, b, "缓动曲线对比")


# ---------------------------------------------------------------- 4. spring knobs
def fig_spring():
    b = head("弹簧：只有两个旋钮", "把 UI 元素想成挂在弹簧上的小方块，被拉向目标位置。")
    # physical diagram
    y = 160
    b += R(40, 110, 10, 100, 2, INK)
    zz = "M50 150 " + " ".join(f"L{62 + k * 14} {150 + (-12 if k % 2 == 0 else 12)}" for k in range(10)) + " L210 150"
    b += P(zz, stroke=INK, sw=2)
    b += P("M50 182 L110 182 M110 172 L110 192 M104 172 L150 172 L150 192 L104 192 M150 182 L210 182", stroke=MUTE, sw=2)
    b += R(210, 136, 56, 56, 8, INK)
    b += L(330, 112, 330, 214, ACC, 2, "5 5") + T(330, 104, "目标", 12.5, ACC, "middle", 600)
    b += arrow(272, 164, 320, 164, ACC)
    b += T(130, 124, "弹簧 → 走得多快（ω）", 12.5, INK, "middle", 600)
    b += T(130, 214, "阻尼器 → 晃不晃（ζ）", 12.5, INK, "middle", 600)
    b += T(238, 236, "UI 元素", 12.5, INK, "middle", 600)
    # 2x2 grid
    gx, gy, cw, ch = 372, 96, 150, 84
    cols = [(10, "ω = 10（慢）"), (28, "ω = 28（快）")]
    rows = [(.35, "ζ = 0.35（弹）"), (.9, "ζ = 0.9（稳）")]
    for ci, (w, wl) in enumerate(cols):
        b += T(gx + 70 + ci * (cw + 12) + cw / 2, gy - 8, wl, 12.5, INK, "middle", 600)
    for ri, (z, zl) in enumerate(rows):
        b += T(gx + 62, gy + ri * (ch + 12) + ch / 2 + 4, zl, 12, INK, "end", 600)
        for ci, (w, _) in enumerate(cols):
            x0, y0 = gx + 70 + ci * (cw + 12), gy + ri * (ch + 12)
            good = (z, w) == (.9, 28)
            b += R(x0, y0, cw, ch, 8, WHITE, ACC if good else LINE, 2 if good else 1)
            lo, hi = 0, 1.45
            yt = y0 + 8 + (ch - 16) * (1 - 1 / hi)
            b += L(x0 + 8, yt, x0 + cw - 8, yt, LINE, 1, "3 4")
            b += P(poly(lambda t: spring(t, w, z), x0 + 8, y0 + 8, cw - 16, ch - 16, tmax=0.9, vmin=lo, vmax=hi), stroke=ACC if good else INK, sw=2.2)
    b += T(gx + 70 + cw + 12 + cw / 2, gy + 2 * ch + 12 + 20, "↑ UI 常用：快且稳", 12.5, ACC, "middle", 600)
    b += T(32, 318, "ω 越大越快；ζ 越小越晃。ζ = 1 刚好不过冲。好的界面动效几乎不晃：ζ 常在 0.8–1 之间。", 13.5, INK)
    svg("04-spring.svg", 800, 340, b, "弹簧的两个参数")


# ---------------------------------------------------------------- 5. seek(t)
def fig_seek():
    b = head("这支动画的核心想法：把画面写成「时间的函数」", "不是「播放」动画，而是「问」它：第 t 秒长什么样？")
    # left: tape
    b += R(32, 92, 352, 212, 14, WHITE, LINE, 1)
    b += T(52, 122, "录像带思维（常见做法）", 14.5, INK, weight=600)
    for k in range(5):
        x = 56 + k * 64
        b += R(x, 150, 44, 44, 6, CANVAS) + T(x + 22, 177, f"{k + 1}", 13, MUTE, "middle", family=MONO)
        if k < 4:
            b += arrow(x + 46, 172, x + 62, 172, MUTE, 1.5)
    b += T(52, 228, "第 5 帧要靠第 4 帧推出来，", 13, MUTE)
    b += T(52, 248, "想看第 500 帧，得从头放到那里。", 13, MUTE)
    b += T(52, 282, "✕ 难跳转　✕ 难并行　✕ 难循环", 13, "#B4502E", weight=600)
    # right: function
    b += R(416, 92, 352, 212, 14, WHITE, ACC, 2)
    b += T(436, 122, "计算器思维（本项目）", 14.5, ACC, weight=600)
    b += R(436, 150, 92, 44, 8, ACC_SOFT) + T(482, 177, "t = 8.30", 13, ACC, "middle", 600, MONO)
    b += arrow(530, 172, 556, 172, ACC)
    b += R(558, 150, 84, 44, 8, ACC) + T(600, 177, "seek(t)", 13.5, WHITE, "middle", 600, MONO)
    b += arrow(644, 172, 670, 172, ACC)
    b += R(672, 146, 76, 52, 6, CANVAS) + R(686, 160, 48, 24, 12, INK) + C(722, 172, 9, WHITE)
    b += T(436, 228, "任何时刻都能直接算出画面，", 13, MUTE)
    b += T(436, 248, "和前一帧无关。", 13, MUTE)
    b += T(436, 282, "✓ 随意跳转　✓ 4 核并行　✓ 无缝循环", 13, ACC, weight=600)
    svg("05-seek.svg", 800, 326, b, "seek(t) 思维")


# ---------------------------------------------------------------- 6. one shape, eleven roles
def fig_states():
    b = head("一个形状，十一种身份（按真实比例）", "全程只有一个圆角矩形。它只改了 4 个属性：宽、高、圆角、颜色。")
    st = [("按钮", 300, 92, 46, 0), ("加载", 92, 92, 46, 0), ("灵动岛", 380, 84, 42, 0), ("展开", 600, 168, 56, 0),
          ("播放器", 640, 400, 40, 255), ("音量", 600, 88, 44, 255), ("开关", 184, 104, 52, 214), ("标签", 540, 100, 50, 0),
          ("图表", 760, 580, 40, 0), ("⌘K", 640, 400, 28, 255), ("提示", 420, 88, 44, 0)]
    s = 0.105
    gap = 12
    total = sum(w * s for _, w, *_ in st) + gap * (len(st) - 1)
    x = (800 - total) / 2
    base = 168
    for name, w, h, r, g in st:
        ww, hh = w * s, h * s
        col = f"rgb({g},{g},{g})"
        b += R(x, base - hh / 2, ww, hh, r * s, col, LINE if g > 200 else "none", 1)
        b += T(x + ww / 2, base + 52, name, 11.5, INK, "middle", 600)
        x += ww + gap
    b += L(32, 236, 768, 236, LINE, 1)
    items = [("宽 / 高", "从 92 到 760"), ("圆角", "圆 ↔ 卡片"), ("颜色", "黑 ↔ 白 ↔ 灰"), ("内容", "文字图标模糊切换")]
    for i, (a, c) in enumerate(items):
        xx = 32 + i * 186
        b += T(xx, 262, a, 13.5, ACC, weight=600) + T(xx, 282, c, 12.5, MUTE)
    svg("06-states.svg", 800, 304, b, "一个形状的十一种状态")


# ---------------------------------------------------------------- 7. beat grid
def fig_beats():
    b = head("跟着音乐走：120 BPM = 每 0.5 秒一拍", "7 小节 × 4 拍 = 28 拍 = 14 秒。每一拍都安排一件事，重拍放重要的动作。")
    x0, x1 = 40, 760
    sx = (x1 - x0) / 14
    seg = [(0, 1, "按钮"), (1, 2, "加载"), (2, 2.5, "✓"), (2.5, 3.5, "灵动岛"), (3.5, 6, "播放器"), (6, 7.5, "音量"),
           (7.5, 8.5, "开关"), (8.5, 10, "标签"), (10, 12, "图表"), (12, 13, "⌘K"), (13, 13.5, "提示"), (13.5, 14, "按钮")]
    for i, (a, c, n) in enumerate(seg):
        fill = INK if i % 2 == 0 else "#4A4743"
        b += R(x0 + a * sx + 1, 96, (c - a) * sx - 2, 34, 6, fill)
        b += T(x0 + (a + c) / 2 * sx, 118, n, 11.5 if (c - a) >= 1 else 10.5, WHITE, "middle", 600)
    ty = 176
    b += L(x0, ty, x1, ty, LINE, 2)
    for k in range(29):
        x = x0 + k * 0.5 * sx
        down = k % 4 == 0
        b += L(x, ty - (14 if down else 7), x, ty + (14 if down else 7), INK if down else MUTE, 2 if down else 1.2)
    for bar in range(7):
        b += T(x0 + (bar * 2 + 1) * sx, ty + 34, f"第 {bar + 1} 小节", 11.5, MUTE, "middle")
    clicks = [1, 4, 8, 9, 9.5]
    for c in clicks:
        b += C(x0 + c * sx, ty - 26, 6, ACC)
    for a, c in [(5, 5.5), (6.5, 7.25)]:
        b += R(x0 + a * sx, ty - 31, (c - a) * sx, 10, 5, ACC)
    for k in [12, 12.5, 12.625, 12.75, 13]:
        b += R(x0 + k * sx - 3.5, ty - 30, 7, 8, 2, "#B4502E")
    ly = 252
    b += C(48, ly, 6, ACC) + T(60, ly + 4, "点击", 12.5)
    b += R(110, ly - 5, 26, 10, 5, ACC) + T(144, ly + 4, "拖拽", 12.5)
    b += R(196, ly - 4, 7, 8, 2, "#B4502E") + T(210, ly + 4, "按键", 12.5)
    b += L(268, ly - 8, 268, ly + 8, INK, 2) + T(278, ly + 4, "重拍（每小节第一拍）", 12.5)
    b += T(760, ly + 4, "开关在第 8 秒的重拍上打开", 12.5, ACC, "end", 600)
    svg("07-beats.svg", 800, 276, b, "节拍表")


# ---------------------------------------------------------------- 8. render pipeline
def fig_pipeline():
    b = head("从网页到视频：四步流水线", "网页本身不是视频。要靠「自动截图 + 拼接」把它变成 mp4。")
    boxes = [("① 浏览器", "Chromium 打开网页", "调用 seek(t)"), ("② 截图", "Playwright", "每帧拍 4 张"),
             ("③ 混合", "ffmpeg tmix", "4 张叠成 1 张"), ("④ 编码", "ffmpeg x264", "得到 mp4")]
    for i, (a, c, d) in enumerate(boxes):
        x = 32 + i * 190
        b += R(x, 92, 160, 92, 12, WHITE, LINE, 1)
        b += T(x + 16, 120, a, 15, INK, weight=600) + T(x + 16, 146, c, 12.5, ACC, family=MONO) + T(x + 16, 168, d, 12.5, MUTE)
        if i < 3:
            b += arrow(x + 162, 138, x + 188, 138)
    b += R(222, 214, 350, 58, 12, ACC_SOFT)
    b += T(240, 240, "♪ 音频：歌曲片段 + 合成的点击音", 13.5, ACC, weight=600)
    b += T(240, 260, "每个音效的峰值对齐到动作发生的那一刻", 12.5, MUTE)
    b += arrow(574, 243, 640, 243, ACC) + P("M640 243 L700 243 L700 186", stroke=ACC, sw=1.8)
    b += f'<path d="M700 184 L695 194 L705 194 Z" fill="{ACC}"/>'
    b += T(768, 304, "画面 + 声音封装在一起 → motion.mp4", 13, INK, "end", 600)
    # motion blur inset
    b += R(32, 300, 300, 86, 12, WHITE, LINE, 1)
    b += T(48, 324, "为什么拍 4 张？—— 运动模糊", 13.5, INK, weight=600)
    for k in range(4):
        b += C(64 + k * 14, 356, 12, INK) if False else f'<circle cx="{64 + k * 14}" cy="356" r="12" fill="{INK}" opacity="0.28"/>'
    b += arrow(140, 356, 176, 356, MUTE, 1.5)
    b += f'<rect x="188" y="344" width="66" height="24" rx="12" fill="{INK}" opacity="0.85"/>'
    b += T(264, 360, "像相机", 12, MUTE)
    b += T(264, 376, "拖出影子", 12, MUTE)
    svg("08-pipeline.svg", 800, 404, b, "渲染流水线")


# ---------------------------------------------------------------- 9. tool map
def fig_tools():
    b = head("做 Motion 的工具地图", "横轴：拖拽着做 ↔ 写代码做。纵轴：平面 2D ↔ 立体 3D。没有最好的工具，只有合适的格子。")
    x0, y0, w, h = 100, 92, 660, 360
    mx, my = x0 + w / 2, y0 + h / 2
    b += R(x0, y0, w, h, 14, WHITE, LINE, 1)
    b += L(mx, y0 + 12, mx, y0 + h - 12, LINE, 1.5) + L(x0 + 12, my, x0 + w - 12, my, LINE, 1.5)
    b += T(x0 + 14, y0 + h + 24, "← 可视化：拖拽、关键帧面板", 12.5, MUTE)
    b += T(x0 + w - 14, y0 + h + 24, "写代码：精确、可复用 →", 12.5, MUTE, "end")
    b += T(70, y0 + 40, "3D", 15, INK, "middle", 700) + T(70, y0 + h - 30, "2D", 15, INK, "middle", 700)

    def pill(x, y, s, hl=False):
        wd = 14 * len(s) * (0.62 if s.isascii() else 1) + 26
        return (R(x - wd / 2, y - 15, wd, 30, 15, ACC if hl else BG, ACC if hl else LINE, 1) +
                T(x, y + 5, s, 13, WHITE if hl else INK, "middle", 600))
    b += T(x0 + 18, y0 + 26, "3D · 可视化", 12, MUTE, weight=600)
    b += pill(x0 + 120, y0 + 66, "Blender") + pill(x0 + 270, y0 + 106, "Spline") + pill(x0 + 110, y0 + 140, "Cinema 4D")
    b += T(mx + 18, y0 + 26, "3D · 代码", 12, MUTE, weight=600)
    b += pill(mx + 110, y0 + 70, "Three.js") + pill(mx + 220, y0 + 124, "React Three Fiber")
    b += T(x0 + 18, my + 26, "2D · 可视化", 12, MUTE, weight=600)
    b += pill(x0 + 110, my + 64, "After Effects") + pill(x0 + 250, my + 98, "Rive") + pill(x0 + 120, my + 134, "Figma 原型")
    b += T(mx + 18, my + 26, "2D · 代码", 12, MUTE, weight=600)
    b += pill(mx + 90, my + 60, "CSS / SVG", True) + pill(mx + 230, my + 60, "GSAP")
    b += pill(mx + 100, my + 104, "Motion") + pill(mx + 230, my + 104, "Remotion")
    b += pill(mx + 120, my + 148, "Motion Canvas")
    b += T(mx + 160, my + 30, "← 我们在这里", 12, ACC, weight=600)
    b += pill(x0 + 268, my + 60, "Lottie")
    svg("09-tools.svg", 800, 490, b, "动效工具地图")


# ---------------------------------------------------------------- 10a/b/c blender
def phone(x, y, s=1.0, screen=True):
    pts = [(x, y), (x + 70 * s, y - 24 * s), (x + 110 * s, y + 150 * s), (x + 40 * s, y + 174 * s)]
    d = "M" + " L".join(f"{a:.1f} {c:.1f}" for a, c in pts) + " Z"
    out = P(d, fill=INK, stroke=INK, sw=6)
    if screen:
        sp = [(x + 6 * s, y + 6 * s), (x + 66 * s, y - 15 * s), (x + 102 * s, y + 144 * s), (x + 42 * s, y + 165 * s)]
        out += P("M" + " L".join(f"{a:.1f} {c:.1f}" for a, c in sp) + " Z", fill=CANVAS, stroke="none", sw=0)
        cx, cy = x + 54 * s, y + 75 * s
        out += f'<rect x="{cx - 22 * s:.1f}" y="{cy - 8 * s:.1f}" width="{44 * s:.1f}" height="{16 * s:.1f}" rx="{8 * s:.1f}" fill="{INK}" transform="rotate(-19 {cx} {cy}) skewY(8)"/>'
    return out


def fig_blender_a():
    b = head("接法 A：把做好的动画「装进」3D 手机里", "Dribbble 上最常见的展示方式。2D 动画当屏幕，Blender 负责手机、灯光和镜头。")
    b += R(32, 120, 120, 84, 10, INK) + R(44, 132, 96, 60, 4, CANVAS) + R(70, 154, 44, 16, 8, INK)
    b += T(92, 226, "motion.mp4", 13, INK, "middle", 600, MONO)
    b += arrow(160, 162, 220, 162)
    b += T(190, 148, "当贴图", 12, MUTE, "middle")
    b += phone(250, 102, 1.0)
    b += T(305, 304, "Blender 里的手机模型", 12.5, INK, "middle", 600)
    # camera
    cx, cy = 520, 150
    b += R(cx, cy, 52, 36, 6, INK) + f'<path d="M{cx + 52} {cy + 8} L{cx + 72} {cy - 2} L{cx + 72} {cy + 38} L{cx + 52} {cy + 28} Z" fill="{INK}"/>'
    b += P(f"M{cx - 80} 250 Q {cx + 20} 300 {cx + 110} 230", stroke=ACC, sw=2, dash="6 6")
    for px_, py_ in [(cx - 80, 250), (cx + 14, 272), (cx + 110, 230)]:
        b += f'<path d="M{px_} {py_ - 7} L{px_ + 7} {py_} L{px_} {py_ + 7} L{px_ - 7} {py_} Z" fill="{ACC}"/>'
    b += T(cx + 16, 214, "相机", 12.5, INK, "middle", 600)
    b += T(cx + 16, 318, "相机沿路径移动（关键帧◆）", 12.5, ACC, "middle")
    b += arrow(680, 168, 730, 168)
    b += T(746, 160, "渲染", 13, INK, "middle", 600) + T(746, 180, "成视频", 13, INK, "middle", 600)
    svg("10a-blender-mockup.svg", 800, 340, b, "Blender 接法 A：3D 样机")


def fig_blender_b():
    b = head("接法 B：Blender 做 3D 小元素，叠进 2D 动画", "比如在「对勾」出现时飞出一个 3D 奖杯。关键是渲染成「带透明背景」的图片。")
    # checker
    x, y = 32, 96
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                b += R(x + i * 20, y + j * 20, 20, 20, 0, "#E2DED7")
    b += R(x, y, 160, 160, 8, "none", LINE, 1)
    cx, cy = x + 80, y + 82
    b += P(f"M{cx} {cy - 44} L{cx + 40} {cy - 22} L{cx} {cy} L{cx - 40} {cy - 22} Z", fill="#4A4743", stroke=INK, sw=1.5)
    b += P(f"M{cx - 40} {cy - 22} L{cx} {cy} L{cx} {cy + 46} L{cx - 40} {cy + 24} Z", fill=INK, stroke=INK, sw=1.5)
    b += P(f"M{cx + 40} {cy - 22} L{cx} {cy} L{cx} {cy + 46} L{cx + 40} {cy + 24} Z", fill="#2E2C29", stroke=INK, sw=1.5)
    b += T(x + 80, 282, "PNG 序列（透明背景）", 12.5, INK, "middle", 600)
    b += T(232, 182, "+", 34, MUTE, "middle", 300)
    b += R(272, 96, 160, 160, 8, CANVAS) + C(352, 176, 26) + P("M341 176 L349 184 L364 168", stroke=WHITE, sw=4)
    b += T(352, 282, "2D 动画的一帧", 12.5, INK, "middle", 600)
    b += T(472, 182, "=", 34, MUTE, "middle", 300)
    b += R(512, 96, 160, 160, 8, CANVAS) + C(592, 186, 26) + P("M581 186 L589 194 L604 178", stroke=WHITE, sw=4)
    sx, sy = 632, 130
    b += P(f"M{sx} {sy - 22} L{sx + 20} {sy - 11} L{sx} {sy} L{sx - 20} {sy - 11} Z", fill="#4A4743", stroke=INK, sw=1)
    b += P(f"M{sx - 20} {sy - 11} L{sx} {sy} L{sx} {sy + 23} L{sx - 20} {sy + 12} Z", fill=INK, stroke=INK, sw=1)
    b += P(f"M{sx + 20} {sy - 11} L{sx} {sy} L{sx} {sy + 23} L{sx + 20} {sy + 12} Z", fill="#2E2C29", stroke=INK, sw=1)
    b += T(592, 282, "合成结果", 12.5, ACC, "middle", 600)
    b += R(688, 112, 96, 128, 10, WHITE, LINE, 1)
    b += T(736, 140, "合成工具", 12, MUTE, "middle")
    b += T(736, 166, "ffmpeg", 12.5, INK, "middle", 600, MONO)
    b += T(736, 186, "overlay", 12.5, INK, "middle", 600, MONO)
    b += T(736, 214, "或剪映 / PR", 12, MUTE, "middle")
    svg("10b-blender-overlay.svg", 800, 304, b, "Blender 接法 B：透明素材叠加")


def fig_blender_c():
    b = head("接法 C：同一张节拍表，同时指挥网页和 Blender", "beatgrid.json 记录了每一拍在第几秒。Blender 也能读它，在同样的拍子上打关键帧。")
    b += R(300, 92, 200, 62, 12, ACC)
    b += T(400, 118, "beatgrid.json", 14, WHITE, "middle", 600, MONO)
    b += T(400, 140, "120 BPM · 每拍 0.5 秒", 12.5, WHITE, "middle")
    rows = [(196, "网页 motion.html", "单位：秒", lambda k: f"{k * 0.5:g}s"), (276, "Blender 时间轴", "单位：帧（60 fps → 每拍 30 帧）", lambda k: f"{k * 30}")]
    for y, name, unit, lab in rows:
        b += T(32, y - 18, name, 13.5, INK, weight=600) + T(32 + 14 * len(name) * 0.8 + 30, y - 18, unit, 12, MUTE)
        b += L(32, y, 768, y, LINE, 2)
        for k in range(9):
            x = 60 + k * 86
            b += f'<path d="M{x} {y - 7} L{x + 7} {y} L{x} {y + 7} L{x - 7} {y} Z" fill="{INK if k % 4 == 0 else MUTE}"/>'
            b += T(x, y + 24, lab(k), 11.5, MUTE, "middle", family=MONO)
    for k in range(9):
        x = 60 + k * 86
        b += L(x, 230, x, 246, ACC, 1.2, "3 4")
    svg("10c-blender-sync.svg", 800, 320, b, "Blender 接法 C：节拍同步")


# ---------------------------------------------------------------- 11. scenarios
def fig_scenarios():
    b = head("学会这一套，还能用在哪？", "每张卡片：场景 · 常用工具 · 能直接复用这次学到的哪一招。")
    cards = [
        ("App 引导页", "Lottie · Rive", "弹簧、内容切换", "onb"),
        ("产品发布视频", "Remotion · AE · Blender", "节拍表、渲染流水线", "launch"),
        ("数据动画", "D3 · Motion Canvas", "线条画出、插值", "data"),
        ("Logo 动效", "AE · Rive · SVG", "缓动、无缝循环", "logo"),
        ("讲解视频", "Manim · Motion Canvas", "seek(t)、时间轴", "edu"),
        ("音乐可视化", "代码 + 音频分析", "BPM、峰值对齐", "music"),
        ("交互原型", "Figma · ProtoPie · Framer", "拖拽跟手、回弹", "proto"),
        ("3D 产品展示", "Blender · Spline · Three.js", "镜头、运动模糊", "3d"),
    ]
    for i, (name, tools, reuse, ic) in enumerate(cards):
        col, row = i % 4, i // 4
        x, y = 32 + col * 186, 92 + row * 196
        b += R(x, y, 172, 182, 12, WHITE, LINE, 1)
        ix, iy = x + 18, y + 18
        if ic == "onb":
            b += R(ix, iy, 30, 46, 6, INK) + C(ix + 15, iy + 22, 7, WHITE) + R(ix + 38, iy + 18, 18, 8, 4, ACC)
        elif ic == "launch":
            b += R(ix, iy + 6, 56, 36, 6, INK) + P(f"M{ix + 22} {iy + 16} L{ix + 36} {iy + 24} L{ix + 22} {iy + 32} Z", fill=WHITE, stroke=WHITE, sw=1)
        elif ic == "data":
            b += P(f"M{ix} {iy + 42} L{ix + 14} {iy + 30} L{ix + 28} {iy + 36} L{ix + 42} {iy + 12} L{ix + 56} {iy + 18}", stroke=ACC, sw=3)
            b += L(ix, iy + 48, ix + 56, iy + 48, INK, 2)
        elif ic == "logo":
            b += C(ix + 22, iy + 24, 20) + C(ix + 22, iy + 24, 8, WHITE) + C(ix + 50, iy + 8, 6, ACC)
        elif ic == "edu":
            b += R(ix, iy + 4, 56, 40, 6, CANVAS, LINE, 1) + P(f"M{ix + 8} {iy + 34} Q {ix + 28} {iy - 4} {ix + 48} {iy + 30}", stroke=INK, sw=2)
            b += T(ix + 28, iy + 58, "f(x)", 10, MUTE, "middle", family=MONO)
        elif ic == "music":
            for k in range(7):
                hh = [12, 30, 20, 40, 26, 16, 34][k]
                b += R(ix + k * 8, iy + 44 - hh, 5, hh, 2, ACC if k == 3 else INK)
        elif ic == "proto":
            b += R(ix, iy, 34, 50, 6, INK) + R(ix + 6, iy + 30, 22, 6, 3, CANVAS) + R(ix + 6, iy + 30, 12, 6, 3, ACC)
            b += P(f"M{ix + 40} {iy + 34} L{ix + 40} {iy + 52} L{ix + 45} {iy + 47} L{ix + 49} {iy + 55}", stroke=INK, sw=2)
        else:
            b += P(f"M{ix + 28} {iy} L{ix + 54} {iy + 14} L{ix + 28} {iy + 28} L{ix + 2} {iy + 14} Z", fill="#4A4743", stroke=INK, sw=1)
            b += P(f"M{ix + 2} {iy + 14} L{ix + 28} {iy + 28} L{ix + 28} {iy + 54} L{ix + 2} {iy + 40} Z", fill=INK, stroke=INK, sw=1)
            b += P(f"M{ix + 54} {iy + 14} L{ix + 28} {iy + 28} L{ix + 28} {iy + 54} L{ix + 54} {iy + 40} Z", fill="#2E2C29", stroke=INK, sw=1)
        b += T(x + 18, y + 98, name, 15, INK, weight=600)
        b += T(x + 18, y + 122, tools, 11.5, MUTE)
        b += L(x + 18, y + 136, x + 154, y + 136, LINE, 1)
        b += T(x + 18, y + 158, "复用：" + reuse, 12, ACC, weight=600)
    svg("11-scenarios.svg", 800, 500, b, "应用场景")


# ---------------------------------------------------------------- 12. roadmap
def fig_roadmap():
    b = head("建议的学习路线", "先练眼睛，再练手感，最后选一个方向深入。每一站都做出一个小作品。")
    stops = [(70, 230, "① 看", "逐帧拆别人的动效", "1–2 周"), (195, 160, "② 调", "用现成库调弹簧手感", "2–4 周"),
             (320, 230, "③ 写", "自己写插值和弹簧", "1–2 周"), (445, 160, "④ 编排", "做一个 3 状态小循环", "2–3 周")]
    b += P("M70 230 C 130 230, 135 160, 195 160 S 260 230, 320 230 S 385 160, 445 160 S 510 230, 540 230", stroke=LINE, sw=6)
    for x, y, a, c, d in stops:
        b += C(x, y, 14, INK) + C(x, y, 5, WHITE)
        ty = y + 38 if y > 200 else y - 52
        b += T(x, ty, a, 15, INK, "middle", 600) + T(x, ty + 20, c, 12.5, MUTE, "middle") + T(x, ty + 38, d, 11.5, ACC, "middle", family=MONO)
    branches = [(140, "UI 动效", "Motion · Rive · Figma"), (230, "视频 / 讲解", "Remotion · Motion Canvas"), (320, "3D", "Blender · Three.js")]
    for y, a, c in branches:
        b += P(f"M540 230 C 590 230, 580 {y}, 620 {y}", stroke=ACC, sw=3)
        b += C(620, y, 7, ACC) + T(634, y - 2, a, 13.5, INK, weight=600) + T(634, y + 16, c, 11.5, MUTE)
    b += T(540, 268, "⑤ 选方向", 13.5, ACC, "middle", 600)
    svg("12-roadmap.svg", 800, 356, b, "学习路线")


for f in [fig_frames, fig_keyframes, fig_easing, fig_spring, fig_seek, fig_states, fig_beats, fig_pipeline,
          fig_tools, fig_blender_a, fig_blender_b, fig_blender_c, fig_scenarios, fig_roadmap]:
    f()
print(sorted(os.listdir(OUT)))
