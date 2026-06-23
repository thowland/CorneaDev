# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Cornea Mono: a programmatically generated monospace TTF for software development,
optimized for readability at 10–16pt (target user: older developers, small point
sizes). It is a utility font — legibility and disambiguation outrank beauty.
There is no unit-test suite or linter; correctness is judged visually from
rendered specimens. CI (`.github/workflows/build.yml`) builds all weights on
every push as a regression check.

## Commands

Everything runs through the venv (no system pip):

```sh
.venv/bin/python build_font.py            # build dist/*.ttf + dist/specimen.png
.venv/bin/python build_font.py --help     # variants: --zero, --seven, --family,
                                          #   --weights, --no-ligatures, --no-hint
.venv/bin/python debug_render.py --size 72                    # big glyph sheet
.venv/bin/python debug_render.py --text "O0o 1lI|" --size 96  # single custom row
.venv/bin/python debug_render.py --font dist/CorneaMono-Bold.ttf
```

The build runs a ttfautohint pass over each weight (TrueType instructions for
even cap height / baseline below 12pt, where the unhinted rasterizer rounds
glyphs to different pixel heights). Box-drawing/blocks (U+2500–259F) and
Powerline (U+E0A0–E0B3) get their instructions stripped afterwards so they
still fill the cell edge-to-edge and connect. `--no-hint` skips the pass; the
build also degrades to a warning if ttfautohint isn't installed.

If `.venv` is missing: `python3 -m venv .venv && .venv/bin/pip install
fonttools pillow ttfautohint-py`. `ttfautohint-py` shells out to a system
`ttfautohint` binary (`apt install ttfautohint`); without it, builds still work
but skip hinting.

## Iteration workflow (important)

After any glyph change: rebuild, then **render and actually look at the output**
(Read the PNG). Judge legibility in `dist/specimen.png` at the 10–16pt waterfall,
not in the large debug rows — small sizes are the design target. Always check
both weights: the recurring failure mode is Bold clogging (stroke width
swallowing a small ring's counter). Use `capw(w, r)` from `cornea/glyphs.py`
to cap stroke widths on small-radius rings/bands.

## Architecture

One parametric pipeline, per weight:

1. `cornea/params.py` — shared vertical scheme (UPM 1000, advance 600, cap 720,
   x-height 540) plus per-weight stroke widths (`stem`, `thin`, `ds`, `dotr`).
   Regular and Bold are the *same glyph code* run with different parameters;
   a new weight is a new parameter set, nothing else. Italic adds a `slant`
   (degrees) + `slant_pivot` (shear pivot y) + `italic_bit`; `builder.py`
   shears every contour by `tan(slant)` about the pivot, except full-cell
   glyphs (box/block/Powerline, which must stay axis-aligned to connect).
2. `cornea/geometry.py` — `Path` (cubic contours) and primitives: `rect`,
   `stroke`, `ellipse`, `ring`, `arc_band` (a curved stroke = annular sector).
   Glyphs are unions of overlapping primitives; there are **no boolean ops** —
   overlapping contours merge because all positive contours are forced clockwise
   (TrueType nonzero winding). Counters (ring interiors) wind counterclockwise.
   Mixing orientations creates holes; `Path.oriented()` handles this.
3. `cornea/glyphs.py` — one builder function per glyph, registered via
   `@glyph(name, codepoint)` into `BUILDERS`. Builders take the param namespace
   `P` and return contour lists inside the fixed 600-unit cell. Build-time
   variants (`P.zero_style`, `P.seven_style`) are set on `P` by the CLI.
   True-italic replacement shapes (single-story `a`, cursive descending `f`)
   register via `@italic_glyph(name)` into `ITALIC_BUILDERS`; they are drawn
   upright and the build slants them like everything else.
   Extension modules (`latin1.py`, `boxdraw.py`, `powerline.py`, `greek.py`)
   register more builders on import (imported in `builder.py`); codepoints
   that share an existing glyph (NBSP, Greek Alpha→A, …) go in each module's
   `EXTRA_CMAP`. New glyphs are named `uniXXXX`. Box/block/Powerline glyphs
   fill the full line box (x 0..600, y -250..950) so cells connect.
4. `cornea/ligatures.py` — ligature glyphs registered via `@liga(name, cells,
   components)`. Each is a single unencoded glyph whose advance is `cells * 600`
   (exact multiples keep editor columns aligned). `feature_text()` generates the
   FEA source for `liga` + `calt` from the registry, longest sequence first.
5. `cornea/builder.py` — fontTools `FontBuilder` assembly: cubic→quadratic via
   `Cu2QuPen`, metrics, name table, and the monospace-detection flags that must
   not regress: `post.isFixedPitch=1`, `OS/2.panose.bProportion=9`,
   `xAvgCharWidth=600`, every encoded glyph advance exactly 600.
6. `cornea/specimen.py` / `debug_render.py` — PIL rendering of the built TTFs
   (RAQM layout so ligatures actually shape). `specimen.py` builds the README
   poster (header, character set, disambiguation + ligature showcase, a
   syntax-highlighted code sample that uses the Bold/Italic faces inline, a
   weight comparison) and ends with the native 10–16pt size waterfall that is
   still the legibility-judging target. Re-render it standalone, without
   rebuilding the fonts, via `.venv/bin/python -m cornea.specimen`.

## Design constraints (user-confirmed; do not silently change)

- Dotted zero by default; tailed `l`; serifed `I`, `1`, `i`/`j` flags; heavy
  slanted backtick vs vertical quotes; exaggerated brackets/braces.
- Strict monospace, 600/1000 advance everywhere; tall x-height (540), normal
  width — density comes from line height, not condensing.
- Core ligature set only (`-> <- => == === != !== >= <= && || :: ...`).
- TTF output. Small caps deferred. Italic is a true italic — a uniform ~10°
  slope plus single-story `a` and cursive descending `f`; box-drawing, blocks
  and Powerline are excluded from the slope so cells still connect. Bold (700)
  must stay a true
  same-advance weight, since IDEs rely on it for cues.
