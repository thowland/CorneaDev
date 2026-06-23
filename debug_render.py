#!/usr/bin/env python3
"""Render big glyph rows for visual debugging. Usage:
   .venv/bin/python debug_render.py [--font dist/CorneaDevMono-Regular.ttf]
                                    [--size 64] [--text "custom"] [--out f.png]
"""
import argparse

from PIL import Image, ImageDraw, ImageFont

ROWS = [
    "ABCDEFGHIJKLM",
    "NOPQRSTUVWXYZ",
    "abcdefghijklm",
    "nopqrstuvwxyz",
    "0123456789",
    "!\"#$%&'()*+,-.",
    "/:;<=>?@[\\]^_",
    "`{|}~ S s $ 5",
    "-> => == === !=",
    "!== >= <= && ||",
    ":: ... <- O0 1lI|",
    "àéîõü ÇßÆæØð ¼½¾",
    "αβγδεπφω ΓΔΣΨΩ",
    "≈≠≤≥∞√ ‘’“”–— ←↑→↓",
    "┌─┬┐ ╔═╦╗ ╰─╯ ░▒▓ ▁▃▅█",
]

ap = argparse.ArgumentParser()
ap.add_argument("--font", default="dist/CorneaDevMono-Regular.ttf")
ap.add_argument("--size", type=int, default=64)
ap.add_argument("--text", default=None, help="custom single row")
ap.add_argument("--out", default="dist/debug.png")
args = ap.parse_args()

rows = [args.text] if args.text else ROWS
f = ImageFont.truetype(args.font, args.size,
                       layout_engine=ImageFont.Layout.RAQM)
lh = int(args.size * 1.5)
w = max(int(f.getlength(r)) for r in rows) + 40
img = Image.new("RGB", (w, lh * len(rows) + 20), (255, 255, 255))
d = ImageDraw.Draw(img)
for i, r in enumerate(rows):
    d.text((20, 10 + i * lh), r, fill=(20, 20, 20), font=f)
img.save(args.out)
print(args.out, img.size)
