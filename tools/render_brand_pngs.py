# -*- coding: utf-8 -*-
"""Rasterize the brand SVG marks to PNG, so every logo is also downloadable as PNG.

No SVG rasterizer is available on this machine (no cairo, no rsvg-convert, no
Inkscape), and every mark in static/brand/assets/ is geometrically simple —
one or two stroked circles plus one filled rounded rect — so this redraws them
directly with Pillow at 4x supersampling instead of parsing SVG. If a mark's
geometry changes, update the MARKS table below to match its .svg source and
rerun: python tools/render_brand_pngs.py
"""
import io, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "brand", "png")
INK = (0x25, 0x29, 0x2C)
WHITE = (0xFF, 0xFF, 0xFF)
TEAL = (0x0C, 0x87, 0x7A)
SIZES = (1024, 512, 256, 128, 64, 32)

# Each mark as (circles, rect) in the SVG's own 0-100 viewBox coordinates.
# circles: list of (cx, cy, r, stroke_width) ; rect: (x, y, w, h, rx) or None.
MARKS = {
    "mark-steward":  {"circles": [(50, 50, 44, 5), (50, 44, 18, 7)], "rect": (30, 72, 40, 7, 1.5)},
    "mark-a-plinth": {"circles": [(50, 42, 26, 8)], "rect": (8, 80, 84, 10, 1.5)},
    "mark-c-lock":   {"circles": [(50, 46, 26, 8)], "rect": (8, 42, 84, 9, 1.5)},
    "mark-biohackit-sibling": {"circles": [(50, 42, 26, 8)], "rect": (20, 80, 60, 8, 1.5)},
}


def draw_mark(spec, colour, px, supersample=4):
    S = px * supersample
    u = S / 100.0
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for cx, cy, r, sw in spec["circles"]:
        bbox = [(cx - r) * u, (cy - r) * u, (cx + r) * u, (cy + r) * u]
        d.ellipse(bbox, outline=colour, width=max(1, round(sw * u)))
    if spec["rect"]:
        x, y, w, h, rx = spec["rect"]
        d.rounded_rectangle([x * u, y * u, (x + w) * u, (y + h) * u], radius=rx * u, fill=colour)
    return im.resize((px, px), Image.LANCZOS)


def app_icon(spec, px, supersample=4):
    """Dark rounded-square tile, white mark, teal bar — matches biohack.it's app-icon.svg."""
    S = px * supersample
    u = S / 100.0
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=22 * u, fill=INK)
    scale, ox, oy = 0.62, 19, 19
    for cx, cy, r, sw in spec["circles"]:
        cx, cy, r = ox + cx * scale, oy + cy * scale, r * scale
        d.ellipse([(cx - r) * u, (cy - r) * u, (cx + r) * u, (cy + r) * u],
                  outline=WHITE, width=max(1, round(sw * scale * u)))
    if spec["rect"]:
        x, y, w, h, rx = spec["rect"]
        x, y, w, h = ox + x * scale, oy + y * scale, w * scale, h * scale
        d.rounded_rectangle([x * u, y * u, (x + w) * u, (y + h) * u], radius=rx * u, fill=TEAL)
    return im.resize((px, px), Image.LANCZOS)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    written = []
    for name, spec in MARKS.items():
        for colour, suffix in ((INK, ""), (WHITE, "-white")):
            for px in SIZES:
                im = draw_mark(spec, colour, px)
                fn = "%s%s-%d.png" % (name, suffix, px)
                im.save(os.path.join(OUT, fn), optimize=True)
                written.append(fn)
    for px in (512, 192, 180):
        im = app_icon(MARKS["mark-steward"], px)
        fn = "hackingbiology-icon-%d.png" % px
        im.save(os.path.join(OUT, fn), optimize=True)
        written.append(fn)
    print("Written %d PNGs to %s" % (len(written), OUT))
