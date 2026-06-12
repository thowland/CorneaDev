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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", default="Cornea Mono",
                    help="font family name (default: Cornea Mono)")
    ap.add_argument("--weights", default="regular,bold",
                    help="comma list: regular,bold")
    ap.add_argument("--version", default="0.1")
    ap.add_argument("--out", default="dist", help="output directory")
    ap.add_argument("--zero", choices=["dotted", "slashed", "plain"],
                    default="dotted", help="zero disambiguation style")
    ap.add_argument("--seven", choices=["plain", "crossbar"], default="plain",
                    help="digit seven style")
    ap.add_argument("--no-ligatures", action="store_true")
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
        print(f"built {path}  ({len(font.getGlyphOrder())} glyphs)")
        paths.append(path)

    if not args.no_specimen:
        spec = os.path.join(args.out, "specimen.png")
        out, raqm = render(paths, spec)
        note = "" if raqm else "  (no raqm: ligatures not shown in specimen)"
        print(f"specimen {out}{note}")


if __name__ == "__main__":
    main()
