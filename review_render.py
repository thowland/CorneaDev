#!/usr/bin/env python3
"""Render a UXD review sheet at the three in-practice sizes (12/14/16pt) for
each weight. Produces a native-resolution PNG (the true design target) and a
3x nearest-neighbour upscale so pixel rendering is legible without resampling
blur. Italic is deferred / does not exist, so only the real weights are shown.
"""
import argparse

from PIL import Image, ImageDraw, ImageFont, features

FG = (28, 28, 30)
BG = (255, 255, 255)

# pt -> px at 96 dpi (matches cornea/specimen.py)
SIZES = [(12, 16), (14, 19), (16, 21)]

DISAMBIG = "O0o 1lI| i!j 5S$ 8B& 2Z?7 rn m g9q ., ;: '\"` (){}[]<>"
ALPHA_U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA_L = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789  +-*/=<>%&|^~"
CODE1 = "if (x != y && a >= b) { return list[i] -> 0x1F; }"
CODE2 = "const fn = (a) => a === b ? items[0] : data || {}; // note"
CODE3 = "for (i = 0; i <= n; i++) s += arr[i];  /* sum loop */"
CODE4 = "let Illegal1 = O0 + lI;  // O0o 1lI| disambiguation"
PROSE = "The quick brown fox jumps over the lazy dog. 0123456789"

ROWS = [DISAMBIG, ALPHA_U, ALPHA_L, DIGITS, CODE1, CODE2, CODE3, CODE4, PROSE]

WEIGHTS = [
    ("Regular", "dist/CorneaDevMono-Regular.ttf"),
    ("Bold", "dist/CorneaDevMono-Bold.ttf"),
]


def render(out_path, width=1180, scale=3):
    has_raqm = features.check("raqm")
    layout = ImageFont.Layout.RAQM if has_raqm else ImageFont.Layout.BASIC
    label_font = ImageFont.load_default()

    rows = []  # (kind, text, font, lineheight)
    for wname, ttf in WEIGHTS:
        rows.append(("title", f"{wname}  ({ttf})", None, 24))
        for pt, px in SIZES:
            rows.append(("label", f"-- {pt}pt / {px}px --", None, 20))
            f = ImageFont.truetype(ttf, px, layout_engine=layout)
            for line in ROWS:
                rows.append(("text", line, f, int(px * 1.5)))
        rows.append(("gap", "", None, 14))

    total = sum(h for _, _, _, h in rows) + 32
    img = Image.new("RGB", (width, total), BG)
    d = ImageDraw.Draw(img)
    y = 16
    for kind, text, f, h in rows:
        if kind == "title":
            d.text((16, y + 5), "== " + text + " ==", fill=(160, 30, 30),
                   font=label_font)
        elif kind == "label":
            d.text((16, y + 4), text, fill=(120, 120, 120), font=label_font)
        elif kind == "text":
            d.text((16, y), text, fill=FG, font=f)
        y += h
    img.save(out_path)

    up = img.resize((width * scale, total * scale), Image.NEAREST)
    up_path = out_path.replace(".png", f"_{scale}x.png")
    up.save(up_path)
    return out_path, up_path, has_raqm


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dist/review_sizes.png")
    args = ap.parse_args()
    native, up, raqm = render(args.out)
    print(f"native: {native}")
    print(f"upscaled: {up}")
    print(f"raqm: {raqm}")
