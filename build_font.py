#!/usr/bin/env python3
"""Build the developer font. Re-run with different flags as the design
evolves.

Examples:
    .venv/bin/python build_font.py
    .venv/bin/python build_font.py --weights regular --zero slashed
    .venv/bin/python build_font.py --family "My Mono" --seven crossbar
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cornea import params
from cornea.builder import build_weight
from cornea.specimen import render


def autohint(path):
    """Run ttfautohint over a built TTF in place. This adds the TrueType
    instructions the parametric pipeline doesn't emit, which is what keeps cap
    height / baseline consistent across glyphs below 12pt (the unhinted
    rasterizer otherwise rounds different glyphs to different pixel heights).
    Degrades to a no-op warning if ttfautohint-py isn't installed."""
    try:
        from ttfautohint import ttfautohint
    except ImportError:
        print(f"  (skip hinting: ttfautohint-py not installed; "
              f"`.venv/bin/pip install ttfautohint-py`)")
        return False
    with open(path, "rb") as fh:
        data = fh.read()
    # 8..50 ppem covers 10-16pt @96dpi with margin; increase_x_height snaps the
    # tall x-height onto the pixel grid at small sizes for an even baseline.
    out = ttfautohint(in_buffer=data, hinting_range_min=8,
                      hinting_range_max=50, increase_x_height=14,
                      no_info=True)
    # Box-drawing/blocks (U+2500-259F) and Powerline (U+E0A0-E0B3) fill the
    # full cell so adjacent cells connect; grid-fitting their stems pulls the
    # fill inward and opens seams. Strip their instructions so they fall back
    # to the raw full-cell outline while text glyphs stay hinted.
    from io import BytesIO
    from fontTools.ttLib import TTFont
    from fontTools.ttLib.tables import ttProgram
    font = TTFont(BytesIO(out))
    glyf = font["glyf"]
    fullcell = [name for cp, name in font.getBestCmap().items()
                if 0x2500 <= cp <= 0x259F or 0xE0A0 <= cp <= 0xE0B3]
    for name in fullcell:
        g = glyf[name]
        if hasattr(g, "program"):
            g.program = ttProgram.Program()
            g.program.fromBytecode(b"")
    font.save(path)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", default="Cornea Mono",
                    help="font family name (default: Cornea Mono)")
    ap.add_argument("--weights", default="regular,bold,italic",
                    help="comma list: regular,bold,italic")
    ap.add_argument("--version", default="0.1")
    ap.add_argument("--out", default="dist", help="output directory")
    ap.add_argument("--zero", choices=["dotted", "slashed", "plain"],
                    default="dotted", help="zero disambiguation style")
    ap.add_argument("--seven", choices=["plain", "crossbar"], default="plain",
                    help="digit seven style")
    ap.add_argument("--no-ligatures", action="store_true")
    ap.add_argument("--no-hint", action="store_true",
                    help="skip the ttfautohint pass (small-size grid fitting)")
    ap.add_argument("--no-specimen", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    paths = []
    for wname in [w.strip() for w in args.weights.split(",") if w.strip()]:
        P = params.weight(wname)
        P.zero_style = args.zero
        P.seven_style = args.seven
        font = build_weight(P, args.family, args.version,
                            enable_ligatures=not args.no_ligatures)
        fname = f"{args.family.replace(' ', '')}-{P.subfamily}.ttf"
        path = os.path.join(args.out, fname)
        font.save(path)
        hinted = autohint(path) if not args.no_hint else False
        tag = "  [autohinted]" if hinted else ""
        print(f"built {path}  ({len(font.getGlyphOrder())} glyphs){tag}")
        paths.append(path)

    if not args.no_specimen:
        spec = os.path.join(args.out, "specimen.png")
        out, raqm = render(paths, spec)
        note = "" if raqm else "  (no raqm: ligatures not shown in specimen)"
        print(f"specimen {out}{note}")


if __name__ == "__main__":
    main()
