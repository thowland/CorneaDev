# Cornea Mono

A monospaced font built as a *tool*: a utility typeface for software
development, optimized for readability at 10–16pt — particularly for
developers whose close-up vision isn't what it used to be. Grotesque
(Helvetica-flavored) skeleton with deliberate serif cues only where they
disambiguate.

## Design decisions

| Decision | Choice |
|---|---|
| Advance | 600/1000 em, strictly monospaced (all glyphs, ligatures = exact cell multiples) |
| x-height | 540 (tall) — legibility from large lowercase bodies, not from width |
| Zero | Dotted (default; `--zero slashed` available) |
| 1 / l / I / \| | 1 = flag + foot serif; l = curved tail; I = top/bottom serifs; \| = full-height bar |
| i / j | Top-left flag serif + foot, distinct from l |
| Brackets/braces | Exaggerated: extra tall, long flanges, prominent brace beak |
| Backtick vs quote | Backtick heavy and clearly slanted; quotes vertical |
| Ligatures | Core set via `liga`+`calt`: `-> <- => == === != !== >= <= && \|\| :: ...` |
| Weights | Regular (400) + Bold (700), same advance, generated from shared parametric skeletons |
| Format | TTF (UPM 1000, quadratic outlines via cu2qu) |

Deferred: italic, small caps. Planned coverage phases: Latin-1/Western
European, box drawing + blocks, Powerline glyphs, Greek + common math.

## Building

```sh
python3 -m venv .venv
.venv/bin/pip install fonttools pillow

.venv/bin/python build_font.py                 # builds dist/*.ttf + specimen.png
.venv/bin/python build_font.py --help          # all options
.venv/bin/python build_font.py --zero slashed --seven crossbar
.venv/bin/python build_font.py --family "My Mono" --weights regular
.venv/bin/python build_font.py --no-ligatures
```

Every build regenerates `dist/specimen.png`, a waterfall at 10–16pt plus
large rows — judge changes there, at target sizes, not at display sizes.

For close inspection of individual glyphs:

```sh
.venv/bin/python debug_render.py --size 72                       # full sheet
.venv/bin/python debug_render.py --text "O0o 1lI|" --size 96     # custom row
.venv/bin/python debug_render.py --font dist/CorneaMono-Bold.ttf
```

## Code layout

- `build_font.py` — CLI entry point
- `cornea/params.py` — per-weight design parameters (stems, x-height, etc.)
- `cornea/geometry.py` — path primitives (stems, bars, rings, arc bands);
  overlapping positive contours merge under nonzero winding, no booleans
- `cornea/glyphs.py` — one builder per glyph, registered with its codepoint;
  new coverage = new builders registering into `BUILDERS`
- `cornea/ligatures.py` — ligature glyphs + generated FEA feature code
- `cornea/builder.py` — fontTools assembly (tables, metrics, monospace flags)
- `cornea/specimen.py` — specimen sheet rendering
