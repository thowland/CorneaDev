# Contributing to CorneaDev Mono

Thanks for your interest. CorneaDev Mono is a **utility font**: a monospace
typeface for code, tuned for legibility at 10–16 pt for developers with aging
near vision. Legibility and disambiguation outrank beauty, and **correctness is
judged visually from rendered specimens** — there is no unit-test suite, because
"does this glyph hold up at 11 pt under blur" isn't something an assertion can
answer.

Please read [`README.md`](README.md) for the design rationale and
[`CLAUDE.md`](CLAUDE.md) for a deeper architecture tour before making changes.

## Development setup

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # fonttools, pillow, ttfautohint-py
.venv/bin/python build_font.py              # builds dist/*.ttf + specimen.png
```

`ttfautohint-py` shells out to a system `ttfautohint` binary
(`apt install ttfautohint` / `brew install ttfautohint`). Without it the build
still works but skips hinting; pass `--no-hint` to skip it deliberately.

## The iteration loop (important)

Every glyph project lives or dies at small sizes. After any change:

1. **Rebuild**, then **actually look at the output** — open `dist/specimen.png`.
2. Judge legibility in the **10–16 pt size waterfall**, not in the large
   display rows. Small sizes are the design target.
3. **Check both weights.** The recurring failure mode is Bold clogging: the
   stroke width swallowing a small ring's counter. Use `capw(w, r)` from
   `cornea/glyphs.py` to cap stroke widths on small-radius rings/bands.
4. For close glyph inspection: `.venv/bin/python debug_render.py --size 72`
   (or `--text "O0o 1lI|"` for a custom row).

If you change a glyph, include **before/after specimen crops** in your pull
request and a sentence on the optical judgement behind it.

## Adding or changing glyphs

- One builder function per glyph in `cornea/glyphs.py` (or the extension
  modules `latin1.py`, `boxdraw.py`, `powerline.py`, `greek.py`), registered
  with `@glyph(name, codepoint)`. It receives the parameter namespace `P` and
  returns contour lists inside the fixed **600-unit cell**.
- Glyphs are unions of overlapping primitives (`rect`, `stroke`, `ellipse`,
  `ring`, `arc_band`) from `cornea/geometry.py`. There are **no boolean ops** —
  positive contours are forced clockwise and merge under nonzero winding;
  counters wind counterclockwise.
- Box-drawing, block, and Powerline glyphs fill the full line box
  (x 0..600, y -250..950) so adjacent cells connect.
- Ligatures go in `cornea/ligatures.py` via `@liga(...)`; their advance must be
  an exact `cells * 600` multiple so editor columns stay aligned.

## Invariants that must not regress

CorneaDev Mono is **strictly monospaced**, and editors/terminals rely on that.
A change must keep:

- every encoded glyph advance exactly **600** (ligatures = exact multiples);
- `post.isFixedPitch = 1`, `OS/2.panose.bProportion = 9`,
  `OS/2.xAvgCharWidth = 600`.

Builds are **reproducible**: identical sources produce byte-identical TTFs
(`head` dates are pinned; honor `SOURCE_DATE_EPOCH`). Don't hand-edit font
timestamps. When your change affects the fonts, **rebuild and commit the
regenerated `dist/*.ttf` and `dist/specimen.png`** so the repo stays in sync.

The user-confirmed design constraints in the README (dotted zero default,
tailed `l`, selective serifs, the core ligature set, true-italic structure,
etc.) should not be changed silently — open an issue to discuss first.

## Quality checks

CI (`.github/workflows/build.yml`) builds all three weights on every push and
pull request. Locally, you're encouraged to run
[fontbakery](https://github.com/fonttools/fontbakery) over `dist/*.ttf` for a
deeper QA pass before submitting.

## Submitting changes

1. Branch off `master`.
2. Make your change; rebuild; **look at the specimen** in both weights.
3. Commit code and the regenerated `dist/` artifacts together.
4. Open a pull request describing the change and the legibility reasoning,
   with specimen crops for any glyph edit.

## Code style

Match the surrounding code. Comments should explain the **why** — the optical
or geometric reason for a magic number — not restate the call. Geometry is
dense; a one-line rationale on an angle or radius saves the next contributor a
render-and-squint cycle.

## Licensing

CorneaDev Mono is released under the [SIL Open Font License 1.1](LICENSE). By
contributing, you agree your contributions are licensed under the same terms.
**CorneaDev Mono** is a Reserved Font Name: a distributed *modified* version must
use a different name.
