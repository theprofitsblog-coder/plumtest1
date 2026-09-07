# -*- coding: utf-8 -*-
"""
Generates real PNG favicons (512x512, 32x32, 180x180 apple-touch-icon).

    python3 src/make_favicon.py

Drawn with PIL only — no external assets, no inline SVG data URI. The mark is a
water droplet over a pipe run, which still reads at 16px.
"""

import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "public", "img")

NAVY = (14, 43, 69, 255)
NAVY_D = (9, 28, 46, 255)
ACCENT = (228, 118, 27, 255)
WHITE = (255, 255, 255, 255)

S = 1024  # master canvas, supersampled then downscaled


def rounded_square(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def droplet_path(cx, cy_top, r):
    """Teardrop: circle of radius r with apex at (cx, cy_top)."""
    pts = []
    # circular part
    for i in range(0, 73):
        a = math.radians(90 + i * (270 / 72.0))       # 90deg -> 360deg
        pts.append((cx + r * math.cos(a), cy_top + r * (1 + math.sin(a) + 1)))
    return pts


def build_master():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # background: navy rounded tile with a subtle vertical gradient
    grad = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(S):
        t = y / float(S)
        col = (int(NAVY[0] + (NAVY_D[0] - NAVY[0]) * t),
               int(NAVY[1] + (NAVY_D[1] - NAVY[1]) * t),
               int(NAVY[2] + (NAVY_D[2] - NAVY[2]) * t), 255)
        gd.line([(0, y), (S, y)], fill=col)

    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, S, S], radius=int(S * 0.22), fill=255)
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)

    # ---- pipe run: a horizontal bar with two elbows, drawn in accent ----
    bar_h = int(S * 0.115)
    y_bar = int(S * 0.665)
    inset = int(S * 0.17)

    # main horizontal run
    d.rounded_rectangle([inset, y_bar, S - inset, y_bar + bar_h],
                        radius=int(bar_h * 0.42), fill=ACCENT)
    # left elbow going down
    d.rounded_rectangle([inset, y_bar, inset + bar_h, y_bar + int(S * 0.155)],
                        radius=int(bar_h * 0.42), fill=ACCENT)
    # right elbow going up
    d.rounded_rectangle([S - inset - bar_h, y_bar - int(S * 0.115), S - inset, y_bar + bar_h],
                        radius=int(bar_h * 0.42), fill=ACCENT)

    # coupling rings (navy notches) so it reads as pipe, not just a bar
    d.rectangle([int(S * 0.42), y_bar - int(bar_h * 0.14),
                 int(S * 0.455), y_bar + bar_h + int(bar_h * 0.14)], fill=NAVY_D)

    # ---- droplet above the pipe ----
    cx = int(S * 0.5)
    r = int(S * 0.185)
    top = int(S * 0.135)
    cy_circle = top + int(r * 1.55)

    # apex triangle blended into the circle
    d.polygon([(cx, top),
               (cx - int(r * 0.92), cy_circle - int(r * 0.15)),
               (cx + int(r * 0.92), cy_circle - int(r * 0.15))],
              fill=WHITE)
    d.ellipse([cx - r, cy_circle - r, cx + r, cy_circle + r], fill=WHITE)

    # inner highlight so the droplet has volume
    hi = int(r * 0.30)
    d.ellipse([cx - int(r * 0.42), cy_circle - int(r * 0.55),
               cx - int(r * 0.42) + hi, cy_circle - int(r * 0.55) + hi * 1.6],
              fill=(214, 231, 244, 255))

    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    master = build_master()

    targets = [
        ("favicon-512.png", 512, False),
        ("favicon-32.png", 32, True),
        ("apple-touch-icon.png", 180, True),
    ]

    for name, size, pad in targets:
        img = master
        if pad:
            # small sizes need optical padding: shrink the mark inside a tile
            inner = int(size * 0.94)
            small = master.resize((inner, inner), Image.LANCZOS)
            canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            off = (size - inner) // 2
            canvas.paste(small, (off, off), small)
            img = canvas
        else:
            img = master.resize((size, size), Image.LANCZOS)
        path = os.path.join(OUT, name)
        img.save(path, "PNG", optimize=True)
        print("wrote %s  (%dx%d, %d bytes)" % (path, size, size, os.path.getsize(path)))


if __name__ == "__main__":
    main()
