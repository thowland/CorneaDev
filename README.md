# CorneaDev Mono

[![build](https://github.com/thowland/CorneaDev/actions/workflows/build.yml/badge.svg)](https://github.com/thowland/CorneaDev/actions/workflows/build.yml)

A monospaced font built as a *tool*: a utility typeface for software
development, optimized for readability at 10–16pt — particularly for
developers whose close-up vision isn't what it used to be. Grotesque
(Helvetica-flavored) skeleton with deliberate serif cues only where they
disambiguate.

![CorneaDev Mono specimen](dist/specimen.png)

## Why it looks the way it does

CorneaDev Mono is designed for one reader: a developer with **presbyopia** — the
age-related loss of near focus that sets in around 40. The screen image isn't
cropped, it's *blurred*, so the whole design problem is keeping letters
distinguishable when the picture is slightly out of focus. Every unusual-looking
choice follows from that:

- **Open apertures** (the "funny" `a`, `e`, `c`) — closed openings fill in and
  smear into neighbours under blur and crowding; open ones hold their identity.
  This is the single best-supported decision in the font.
- **Disambiguated confusables** (`0`/`O`, `1`/`l`/`I`/`|`, `8`/`B`, `rn`/`m`, …)
  — the look-alikes that cause real bugs, shaped per-glyph rather than uniformly.
- **Selective serifs** on the troublemakers only (`I`, foot of `l`, `i`/`j`) —
  serifs help where stroke contrast is uniform (as in a monospace) and at the
  vertical extremes of letters; they go nowhere else.
- **Tall x-height + generous, even spacing** — the lever that actually buys blur
  tolerance at a given point size; monospace's roomy spacing is a bonus for
  degraded reading.
- **Mid-range weight; italic as the weakest channel** — heavy strokes close
  counters and work against the open-aperture strategy, and slant is the hardest
  style for these eyes, so the italic stays gentle and leans on weight/colour.

Two companion documents in [`docs/`](docs/) go deeper:

- [**Legibility Assessment & Design Rationale**](docs/CorneaDevMono_Legibility_Assessment.md)
  — a research-grounded evaluation mapping each decision to its evidence basis
  and a confidence rating, with honest caveats and references.
- [**Plain-Language Guide**](docs/CorneaDevMono_Plain_Language_Guide.md)
  — the same reasoning without the type-design vocabulary.

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
| Italic | True italic (~10° slope) with single-story `a` and cursive descending `f`; box-drawing, blocks and Powerline stay upright so cells still connect |
| Format | TTF (UPM 1000, quadratic outlines via cu2qu) |

Deferred: small caps.

## Coverage

- Full ASCII (U+0020–007E)
- Latin-1 Supplement (U+00A0–00FF): composed diacritics, Ð ð Þ þ ß Æ æ Ø ø,
  currency, ordinals, superscripts, fractions
- Greek (U+0391–03C9; identical capitals alias Latin glyphs)
- Common math: − ≈ ≠ ≤ ≥ ∞ √ (plus ± × ÷ from Latin-1)
- General punctuation: – — ‘ ’ “ ” • … and arrows ← ↑ → ↓
- Box Drawing (U+2500–257F) and Block Elements (U+2580–259F), spanning the
  full line box so cells connect in terminals
- Powerline separators/symbols (U+E0A0–E0A2, E0B0–E0B3)

## Installing

Grab the `.ttf` files from [`dist/`](dist/) (or a tagged release), then:

- **macOS** — double-click each `.ttf` and click *Install Font*, or copy them
  to `~/Library/Fonts`.
- **Windows** — right-click each `.ttf` and choose *Install*, or copy them to
  `C:\Windows\Fonts`.
- **Linux** — copy them to `~/.local/share/fonts` and run `fc-cache -f`.

Then set your editor/terminal font to **CorneaDev Mono** (use the **Bold** weight
for bold cues and **Italic** for italics — IDEs pick these up automatically).
Don't have it yet? Build from source below.

## Building

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt      # fonttools, pillow, ttfautohint-py

.venv/bin/python build_font.py                 # builds dist/*.ttf + specimen.png
.venv/bin/python build_font.py --help          # all options
.venv/bin/python build_font.py --zero slashed --seven crossbar
.venv/bin/python build_font.py --family "My Mono" --weights regular
.venv/bin/python build_font.py --no-ligatures
```

Every build regenerates `dist/specimen.png` (shown above): a full specimen
sheet — character set, disambiguation and ligature showcase, a
syntax-highlighted code sample (keywords in Bold, comments in Italic), a
weight comparison, and a 10–16pt size waterfall. Judge legibility in that
waterfall, at target sizes, not in the large display rows.

To redesign or re-render the specimen poster without rebuilding the fonts:

```sh
.venv/bin/python -m cornea.specimen            # re-renders dist/specimen.png
```

For close inspection of individual glyphs:

```sh
.venv/bin/python debug_render.py --size 72                       # full sheet
.venv/bin/python debug_render.py --text "O0o 1lI|" --size 96     # custom row
.venv/bin/python debug_render.py --font dist/CorneaDevMono-Bold.ttf
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
- `cornea/specimen.py` — specimen sheet rendering (poster + size waterfall;
  runnable standalone via `python -m cornea.specimen`)

## License

CorneaDev Mono is licensed under the [SIL Open Font License 1.1](LICENSE) — free
to use, study, modify, and redistribute (including bundled with software);
it just can't be sold on its own and must stay under the OFL. **CorneaDev Mono**
is a Reserved Font Name: if you distribute a modified version, give it a
different name.
