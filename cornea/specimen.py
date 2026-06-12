"""Render specimen sheets with the freshly built TTFs so changes are judged
at actual IDE sizes (10-16pt), not at display sizes."""

import os

from PIL import Image, ImageDraw, ImageFont, features

FG = (28, 28, 30)
BG = (255, 255, 255)

DISAMBIG = "O0o 1lI| i!j 5S$ 8B& 2Z?7 rn m g9q ., ;: '\"` (){}[]<>"
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789"
SYMS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
CODE1 = "if (x != y && a >= b) { return list[i] -> 0x1F; }"
CODE2 = "const fn = (a) => a === b ? items[0] : data || {}; // note"
CODE3 = "while (i <= n) { s += arr[i]; i++; } ... :: != !=="

# pt -> px at 96 dpi
SIZES = [(10, 13), (11, 15), (12, 16), (13, 17), (14, 19), (16, 21)]


def render(ttf_paths, out_path, width=1280):
    has_raqm = features.check("raqm")
    layout = ImageFont.Layout.RAQM if has_raqm else ImageFont.Layout.BASIC

    rows = []
    for ttf in ttf_paths:
        label = os.path.basename(ttf)
        rows.append(("title", label, None))
        # big row for shape inspection
        big = ImageFont.truetype(ttf, 44, layout_engine=layout)
        rows.append(("text", DISAMBIG, big))
        rows.append(("text", ALPHA, big))
        rows.append(("text", SYMS, big))
        for pt, px in SIZES:
            f = ImageFont.truetype(ttf, px, layout_engine=layout)
            rows.append(("label", f"-- {pt}pt --", None))
            for line in (DISAMBIG, ALPHA, CODE1, CODE2, CODE3):
                rows.append(("text", line, f))

    label_font = ImageFont.load_default()
    pad, y = 16, 16
    heights = []
    for kind, text, f in rows:
        if kind in ("title", "label"):
            heights.append(22)
        else:
            heights.append(int(f.size * 1.45))
    total = sum(heights) + 2 * pad

    img = Image.new("RGB", (width, total), BG)
    d = ImageDraw.Draw(img)
    for (kind, text, f), h in zip(rows, heights):
        if kind == "title":
            d.text((pad, y + 4), "== " + text + " ==", fill=(160, 30, 30),
                   font=label_font)
        elif kind == "label":
            d.text((pad, y + 4), text, fill=(120, 120, 120), font=label_font)
        else:
            d.text((pad, y), text, fill=FG, font=f)
        y += h
    img.save(out_path)
    return out_path, has_raqm
