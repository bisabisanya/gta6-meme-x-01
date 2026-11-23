#!/usr/bin/env python3
"""Build the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Concept: a fake GTA VI loading screen over a Vice City sunset.
The joke a GTA fan gets in one second: GTA 6 is finally out after
13 years -- but the download still says "13 YEARS REMAINING".
make.fun's ghost mascot sits on the loading bar holding its magenta
star coin, with the make.fun name under it, worked into the scene.

Deterministic: fixed palette, fixed geometry, no randomness, no
network, no timestamps. Run it twice, get byte-identical PNGs.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "meme.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def sparkle_points(cx, cy, r):
    """Four-pointed sparkle (the ghost's eyes)."""
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.28
        ang = math.radians(-90 + i * 45)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts


def draw_ghost(draw, cx, top, w, h, outline=7):
    """make.fun ghost: white body, thick black outline, two black
    four-pointed sparkle eyes, one round little hand, magenta coin
    with a white star held in the hand."""
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = top, top + h
    # Body silhouette: rounded top, straight sides, wavy hem.
    body = []
    steps = 24
    for i in range(steps + 1):  # top semicircle, left -> right
        a = math.pi + math.pi * i / steps
        body.append((cx + (w / 2) * math.cos(a), y0 + (h * 0.42) + (h * 0.42) * math.sin(a)))
    hem_y = y1
    bumps = 3
    for i in range(steps + 1):  # wavy hem, right -> left
        t = i / steps
        x = x1 - t * w
        y = hem_y - (h * 0.09) * abs(math.sin(t * math.pi * bumps))
        body.append((x, y))
    # Black outline pass: same shape, slightly larger.
    big = [(cx + (x - cx) * 1.07, y0 + (y - y0) * 1.045) for (x, y) in body]
    draw.polygon(big, fill=(0, 0, 0))
    draw.polygon(body, fill=(255, 255, 255))
    # Eyes: two black four-pointed sparkles.
    ey, er = y0 + h * 0.40, w * 0.115
    for ex in (cx - w * 0.20, cx + w * 0.20):
        draw.polygon(sparkle_points(ex, ey, er), fill=(0, 0, 0))
    # Little round hand on the right side, holding the coin.
    hx, hy, hr = x1 + w * 0.02, y0 + h * 0.62, w * 0.075
    draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(0, 0, 0))
    draw.ellipse([hx - hr + 2, hy - hr + 2, hx + hr - 2, hy + hr - 2], fill=(255, 255, 255))
    # Magenta coin with a white star, held just above the hand.
    cr = w * 0.17
    ccx, ccy = hx + w * 0.10, hy - h * 0.16
    draw.ellipse([ccx - cr - 3, ccy - cr - 3, ccx + cr + 3, ccy + cr + 3], fill=(0, 0, 0))
    draw.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(255, 46, 136))
    draw.polygon(star_points(ccx, ccy, cr * 0.62, cr * 0.26), fill=(255, 255, 255))


def draw_gator(draw, x, y, s):
    """Small alligator silhouette floating in the ocean -- Leonida energy."""
    col = (26, 11, 46)
    # Body: long ellipse; tail tapering to the left; snout to the right.
    draw.ellipse([x, y, x + s, y + s * 0.26], fill=col)
    draw.polygon([(x + s * 0.02, y + s * 0.08), (x - s * 0.55, y + s * 0.16),
                  (x + s * 0.02, y + s * 0.20)], fill=col)
    draw.polygon([(x + s * 0.92, y + s * 0.04), (x + s * 1.22, y + s * 0.10),
                  (x + s * 1.22, y + s * 0.18), (x + s * 0.92, y + s * 0.20)], fill=col)
    # Eye bumps on top.
    draw.ellipse([x + s * 0.78, y - s * 0.05, x + s * 0.88, y + s * 0.05], fill=col)
    draw.ellipse([x + s * 0.90, y - s * 0.05, x + s * 1.00, y + s * 0.05], fill=col)
    # Back spikes.
    for i, fx in enumerate((0.25, 0.45, 0.65)):
        px = x + s * fx
        draw.polygon([(px, y + s * 0.02), (px + s * 0.05, y - s * 0.08),
                      (px + s * 0.10, y + s * 0.02)], fill=col)


def main():
    img = Image.new("RGB", (W, H), (20, 8, 32))
    d = ImageDraw.Draw(img)

    # --- Vice City sunset sky (gradient) ---
    stops = [(0.00, (43, 16, 85)), (0.35, (123, 47, 145)),
             (0.62, (255, 107, 157)), (0.85, (255, 167, 81)), (1.00, (255, 209, 148))]
    sky_h = 560
    for y in range(sky_h):
        t = y / sky_h
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                d.line([(0, y), (W, y)], fill=lerp(c0, c1, (t - t0) / (t1 - t0)))
                break
    # Stars in the upper sky.
    for (sx, sy, sr) in [(80, 40, 3), (200, 90, 2), (330, 30, 3), (700, 55, 2),
                         (820, 35, 3), (930, 100, 2), (120, 150, 2), (880, 170, 2)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))

    # --- Retro striped sun ---
    sun_cx, sun_cy, sun_r = 512, 470, 165
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=(255, 214, 90))
    for i, yy in enumerate(range(sun_cy + 12, sun_cy + sun_r, 24)):
        gap = 5 + i * 2
        # sky colour at that height
        t = yy / sky_h
        col = (255, 167, 81) if yy < 500 else (255, 190, 120)
        d.rectangle([sun_cx - sun_r - 2, yy, sun_cx + sun_r + 2, yy + gap], fill=col)

    # --- Skyline silhouette ---
    buildings = [(0, 470, 90, 560), (90, 430, 170, 560), (170, 490, 240, 560),
                 (240, 410, 330, 560), (330, 480, 400, 560), (400, 440, 470, 560),
                 (560, 450, 640, 560), (640, 480, 720, 560), (720, 420, 800, 560),
                 (800, 490, 880, 560), (880, 440, 960, 560), (960, 480, 1024, 560)]
    for (x0, y0, x1, y1) in buildings:
        d.rectangle([x0, y0, x1, y1], fill=(26, 11, 46))
    # A few lit windows.
    for (wx, wy) in [(120, 460), (150, 500), (270, 440), (300, 480), (430, 470),
                     (600, 480), (760, 450), (790, 500), (910, 470)]:
        d.rectangle([wx, wy, wx + 12, wy + 16], fill=(255, 214, 90))

    # --- Ocean strip ---
    for y in range(560, 640):
        t = (y - 560) / 80
        d.line([(0, y), (W, y)], fill=lerp((255, 120, 110), (120, 40, 110), t))
    for wy in (580, 600, 620):
        for wx in range(0, W, 90):
            d.arc([wx, wy - 6, wx + 60, wy + 6], 200, 340, fill=(255, 220, 200), width=3)

    # --- Alligator cruising the ocean (Leonida energy) ---
    draw_gator(d, 700, 596, 130)

    # --- Headline ---
    def text_c(y, s, fnt, fill, stroke=4, sw=0):
        tw = d.textlength(s, font=fnt)
        d.text(((W - tw) / 2 + sw, y), s, font=fnt, fill=fill,
               stroke_width=stroke, stroke_fill=(0, 0, 0))

    text_c(36, "GTA 6 IS OUT!", font(BOLD, 96), (255, 255, 255), stroke=6)
    text_c(150, "AFTER 13 YEARS OF \u201cSOON\u201d", font(BOLD, 44),
           (255, 209, 102), stroke=4)

    # --- Dark UI panel ---
    d.rectangle([0, 640, W, H], fill=(16, 12, 28))
    d.line([(0, 640), (W, 640)], fill=(255, 46, 136), width=5)

    # Download labels above the bar.
    d.text((92, 668), "DOWNLOADING", font=font(BOLD, 38), fill=(255, 255, 255),
           stroke_width=3, stroke_fill=(0, 0, 0))
    sz = d.textlength("214 GB", font=font(BOLD, 38))
    d.text((W - 92 - sz, 668), "214 GB", font=font(BOLD, 38), fill=(255, 255, 255),
           stroke_width=3, stroke_fill=(0, 0, 0))

    # Loading bar, 99% full.
    bx0, bx1, by0, by1 = 90, 934, 736, 806
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=18, outline=(255, 255, 255), width=5)
    fill_w = int((bx1 - bx0 - 10) * 0.99)
    d.rounded_rectangle([bx0 + 5, by0 + 5, bx0 + 5 + fill_w, by1 - 5], radius=13,
                        fill=(255, 46, 136))
    pct = "99%"
    pw = d.textlength(pct, font=font(BOLD, 40))
    d.text((bx1 - 24 - pw, by0 + 12), pct, font=font(BOLD, 40), fill=(255, 255, 255),
           stroke_width=3, stroke_fill=(0, 0, 0))

    # --- make.fun ghost sitting on the loading bar ---
    draw_ghost(d, cx=512, top=596, w=150, h=150)

    # Punchline lines.
    text_c(836, "TIME REMAINING: 13 YEARS", font(BOLD, 48), (255, 209, 102), stroke=4)
    text_c(906, "WORTH EVERY SECOND OF THE WAIT.", font(BOLD, 38),
           (255, 255, 255), stroke=3)
    text_c(962, "make.fun", font(BOLD, 34), (255, 46, 136), stroke=3)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
