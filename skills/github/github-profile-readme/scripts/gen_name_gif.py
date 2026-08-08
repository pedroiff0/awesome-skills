#!/usr/bin/env python3
"""Generate an animated "name" GIF with a space theme for a profile README footer.

Self-hosted (committed to assets/) so the README doesn't depend on a third-party
GIF service. Twinkling stars + orbiting dot + glowing name + shimmer subtitle.

Usage:
    python3 gen_name_gif.py --text pedroiff0 --out assets/pedroiff0.gif

Requires Pillow:  pip install pillow
"""
import argparse
import math
import os
import random

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow required: pip install pillow")


def _font(sz, path=None):
    if path and os.path.exists(path):
        return ImageFont.truetype(path, sz)
    return ImageFont.load_default()


def build(text, out, w=640, h=200, frames=40, fps=20, font_path=None):
    random.seed(7)
    big = _font(54, font_path)
    small = _font(20, font_path)
    stars = [(random.randint(0, w), random.randint(0, h),
              random.uniform(0.4, 1.6), random.uniform(0.5, 1.0)) for _ in range(120)]
    tw = big.getlength(text)
    tx = (w - tw) / 2
    imgs = []
    for f in range(frames):
        t = f / frames
        img = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(img)
        for y in range(h):
            r = int(8 + 6 * math.sin(y / h * math.pi))
            g = int(10 + 6 * math.sin(y / h * math.pi + 1))
            b = int(26 + 14 * math.cos(y / h * math.pi))
            d.line([(0, y), (w, y)], fill=(r, g, b))
        for (sx, sy, sr, base) in stars:
            twk = base * (0.5 + 0.5 * math.sin(t * math.pi * 2 * 3 + sx))
            c = min(255, int(180 * twk) + 40)
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(c, c, min(255, c + 30)))
        px = w / 2 + math.cos(t * math.pi * 2) * 150
        py = h / 2 + math.sin(t * math.pi * 2) * 60
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(180, 140, 255))
        for ox, oy in [(-2, -2), (2, 2), (-2, 2), (2, -2), (0, 0)]:
            fill = (120, 80, 220) if (ox, oy) != (0, 0) else (230, 240, 255)
            d.text((tx + ox, h / 2 - 30 + oy), text, font=big, fill=fill)
        sub = "between code and cosmos"
        sw = small.getlength(sub)
        d.text(((w - sw) / 2, h - 34), sub, font=small, fill=(150, 170, 220))
        imgs.append(img)
    imgs[0].save(out, save_all=True, append_images=imgs[1:],
                 duration=int(1000 / fps), loop=0, optimize=True)
    return os.path.getsize(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default="pedroiff0")
    ap.add_argument("--out", default="assets/pedroiff0.gif")
    ap.add_argument("--font", default=None, help="path to a .ttf for nicer text")
    args = ap.parse_args()
    size = build(args.text, args.out, font_path=args.font)
    print(f"wrote {args.out} ({size} bytes, animated GIF)")


if __name__ == "__main__":
    main()
