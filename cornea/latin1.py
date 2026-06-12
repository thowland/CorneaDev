"""Latin-1 Supplement (U+00A0..U+00FF).

Accented letters are composed in outline space: base builder + a diacritic
mark builder. Marks come in a lowercase variant (above x-height) and a
compressed capital variant (above cap height). New glyphs are named uniXXXX.
"""

from .geometry import (stroke, ellipse, dot, ring, arc_band,
                       translate_all, rotate180_all, scale_all)
from .glyphs import (BUILDERS, glyph, vstem, hbar, capw, _i_base, _round_lc,
                     g_A, g_C, g_D, g_E, g_I, g_N, g_O, g_R, g_U, g_Y,
                     g_a, g_c, g_e, g_n, g_o, g_u, g_y,
                     g_question, g_exclam)

# --- diacritic marks ------------------------------------------------------
# Lowercase marks live in 580..710; capital marks are compressed into 745..875.

LC_Y, CAP_Y = 645, 800        # vertical centers of the mark zones


def _mk_acute(P, cy):
    return stroke((235, cy - 62), (372, cy + 62), P.thin + 6)


def _mk_grave(P, cy):
    return stroke((228, cy + 62), (365, cy - 62), P.thin + 6)


def _mk_circumflex(P, cy):
    w = P.ds * 0.9
    return (stroke((300, cy + 62), (172, cy - 58), w)
            + stroke((300, cy + 62), (428, cy - 58), w))


def _mk_dieresis(P, cy):
    r = P.dotr - 6
    return dot(192, cy, r) + dot(408, cy, r)


def _mk_tilde(P, cy):
    w = capw(P.thin, 80)
    c = arc_band(218, cy - 12, 82, 46, w, 155, 25)
    c += arc_band(382, cy + 12, 82, 46, w, 205, 335)
    return c


def _mk_ring(P, cy):
    return ring(300, cy + 8, 78, 78, capw(P.thin, 78))


def _mk_macron(P, cy):
    return hbar(P, cy, 185, 415, P.thin)


def _mk_cedilla(P, cx=300):
    """Hangs below the baseline, attached at x = cx."""
    c = vstem(P, cx, -68, 6, P.thin - 8)
    c += arc_band(cx - 42, -120, 64, 64, capw(P.thin, 64), 18, -150)
    return c


MARKS = {"acute": _mk_acute, "grave": _mk_grave, "circumflex": _mk_circumflex,
         "dieresis": _mk_dieresis, "tilde": _mk_tilde, "ring": _mk_ring,
         "macron": _mk_macron}


def composed(cp, base_fn, mark, cap=False):
    """Register base + above-mark at the right height."""
    cy = CAP_Y if cap else LC_Y
    mark_fn = MARKS[mark]

    def fn(P, base_fn=base_fn, mark_fn=mark_fn, cy=cy):
        return base_fn(P) + mark_fn(P, cy)
    BUILDERS[f"uni{cp:04X}"] = (cp, fn)


# --- accented capitals ----------------------------------------------------

for cp, mark in [(0xC0, "grave"), (0xC1, "acute"), (0xC2, "circumflex"),
                 (0xC3, "tilde"), (0xC4, "dieresis"), (0xC5, "ring")]:
    composed(cp, g_A, mark, cap=True)
for cp, mark in [(0xC8, "grave"), (0xC9, "acute"), (0xCA, "circumflex"),
                 (0xCB, "dieresis")]:
    composed(cp, g_E, mark, cap=True)
for cp, mark in [(0xCC, "grave"), (0xCD, "acute"), (0xCE, "circumflex"),
                 (0xCF, "dieresis")]:
    composed(cp, g_I, mark, cap=True)
composed(0xD1, g_N, "tilde", cap=True)
for cp, mark in [(0xD2, "grave"), (0xD3, "acute"), (0xD4, "circumflex"),
                 (0xD5, "tilde"), (0xD6, "dieresis")]:
    composed(cp, g_O, mark, cap=True)
for cp, mark in [(0xD9, "grave"), (0xDA, "acute"), (0xDB, "circumflex"),
                 (0xDC, "dieresis")]:
    composed(cp, g_U, mark, cap=True)
composed(0xDD, g_Y, "acute", cap=True)

# --- accented lowercase ---------------------------------------------------

for cp, mark in [(0xE0, "grave"), (0xE1, "acute"), (0xE2, "circumflex"),
                 (0xE3, "tilde"), (0xE4, "dieresis"), (0xE5, "ring")]:
    composed(cp, g_a, mark)
for cp, mark in [(0xE8, "grave"), (0xE9, "acute"), (0xEA, "circumflex"),
                 (0xEB, "dieresis")]:
    composed(cp, g_e, mark)
for cp, mark in [(0xEC, "grave"), (0xED, "acute"), (0xEE, "circumflex"),
                 (0xEF, "dieresis")]:
    composed(cp, _i_base, mark)
composed(0xF1, g_n, "tilde")
for cp, mark in [(0xF2, "grave"), (0xF3, "acute"), (0xF4, "circumflex"),
                 (0xF5, "tilde"), (0xF6, "dieresis")]:
    composed(cp, g_o, mark)
for cp, mark in [(0xF9, "grave"), (0xFA, "acute"), (0xFB, "circumflex"),
                 (0xFC, "dieresis")]:
    composed(cp, g_u, mark)
composed(0xFD, g_y, "acute")
composed(0xFF, g_y, "dieresis")


# --- special letters ------------------------------------------------------

@glyph("uni00C7", 0xC7)
def g_Ccedilla(P):
    return g_C(P) + _mk_cedilla(P, 330)


@glyph("uni00E7", 0xE7)
def g_ccedilla(P):
    return g_c(P) + _mk_cedilla(P, 330)


@glyph("uni00D0", 0xD0)
def g_Eth(P):
    return g_D(P) + hbar(P, 372, 25, 235)


@glyph("uni00F0", 0xF0)
def g_eth(P):
    # bowl + ascender curve rising from the bowl's top right, bending left,
    # with the diagonal cross tick
    c = ring(300, 235, P.lc_rx - 15, 247, P.stem)
    c += arc_band(300, 460, 162, 250, P.stem - 8, -8, 128)
    c += stroke((212, 580), (408, 688), P.thin + 2)
    return c


@glyph("uni00DE", 0xDE)
def g_Thorn(P):
    x = 100
    c = vstem(P, x, 0, P.cap)
    c += hbar(P, 560, x, 330) + hbar(P, 200, x, 330)
    c += arc_band(330, 380, 165, 168, P.stem - 4, 90, -90)
    return c


@glyph("uni00FE", 0xFE)
def g_thorn(P):
    m = _round_lc(P)
    c = vstem(P, P.lc_stem_l, P.desc, P.asc)
    c += ring(m["cx"], m["cy"], m["rx"], m["ry"], P.stem)
    return c


@glyph("uni00DF", 0xDF)
def g_germandbls(P):
    c = vstem(P, 120, 0, 600)
    c += arc_band(295, 600, 175, 110, P.stem - 6, 180, 0)
    c += arc_band(395, 405, 105, 92, P.stem - 6, 90, -90)
    c += arc_band(370, 180, 130, 132, P.stem - 6, 70, -110)
    return c


@glyph("uni00C6", 0xC6)
def g_AE(P):
    c = stroke((60, 0), (322, P.cap - 20), P.ds)
    c += vstem(P, 322, 0, P.cap)
    c += hbar(P, P.cap - P.thin / 2, 322, 545)
    c += hbar(P, 380, 322, 510)
    c += hbar(P, P.thin / 2, 322, 545)
    c += hbar(P, 230, 128, 322)
    return c


@glyph("uni00E6", 0xE6)
def g_ae(P):
    a = scale_all(g_a(P), 0.60, 1.0, 0, 0)
    e = scale_all(g_e(P), 0.60, 1.0, 600, 0)
    return translate_all(a, 10, 0) + translate_all(e, -10, 0)


@glyph("uni00D8", 0xD8)
def g_Oslash(P):
    return g_O(P) + stroke((148, -28), (452, P.cap + 28), P.thin)


@glyph("uni00F8", 0xF8)
def g_oslash(P):
    return g_o(P) + stroke((155, -40), (445, P.xh + 40), P.thin)


# --- symbols --------------------------------------------------------------

@glyph("uni00A1", 0xA1)
def g_exclamdown(P):
    return rotate180_all(g_exclam(P), 300, 295)


@glyph("uni00BF", 0xBF)
def g_questiondown(P):
    return rotate180_all(g_question(P), 300, 295)


@glyph("uni00AB", 0xAB)
def g_guillemotleft(P):
    w = P.ds - 8
    c = (stroke((265, 520), (105, 330), w) + stroke((105, 330), (265, 140), w)
         + stroke((495, 520), (335, 330), w)
         + stroke((335, 330), (495, 140), w))
    return c


@glyph("uni00BB", 0xBB)
def g_guillemotright(P):
    return [c.scaled(-1, 1, 300, 0) for c in g_guillemotleft(P)]


@glyph("uni00A6", 0xA6)
def g_brokenbar(P):
    w = P.stem - 6
    return vstem(P, 300, -150, 240, w) + vstem(P, 300, 400, 770, w)


@glyph("uni00AC", 0xAC)
def g_logicalnot(P):
    return hbar(P, 400, 105, 495, P.thin + 6) + vstem(P, 495 - (P.thin + 6) / 2, 245, 400, P.thin + 6)


@glyph("uni00B7", 0xB7)
def g_periodcentered(P):
    return dot(300, 330, P.dotr + 4)


@glyph("uni00B0", 0xB0)
def g_degree(P):
    return ring(300, 628, 84, 84, capw(P.thin, 84))


@glyph("uni00B1", 0xB1)
def g_plusminus(P):
    c = hbar(P, 400, 115, 485, P.thin + 6)
    c += vstem(P, 300, 230, 570, P.thin + 6)
    c += hbar(P, 90, 115, 485, P.thin + 6)
    return c


@glyph("uni00D7", 0xD7)
def g_multiply(P):
    w = P.thin + 6
    return (stroke((165, 195), (435, 465), w)
            + stroke((435, 195), (165, 465), w))


@glyph("uni00F7", 0xF7)
def g_divide(P):
    r = P.dotr - 2
    return (hbar(P, 330, 105, 495, P.thin + 6)
            + dot(300, 500, r) + dot(300, 160, r))


@glyph("uni00B5", 0xB5)
def g_micro(P):
    from .glyphs import g_u
    return g_u(P) + vstem(P, P.lc_stem_l, -200, 200)


@glyph("uni00A2", 0xA2)
def g_cent(P):
    return g_c(P) + vstem(P, 320, -50, 590, P.thin - 10)


@glyph("uni00A3", 0xA3)
def g_sterling(P):
    c = vstem(P, 215, 60, 460)
    c += arc_band(352, 500, 138, 160, P.stem - 6, 180, 30)
    c += hbar(P, 320, 110, 430)
    c += hbar(P, P.thin / 2 + 30, 100, 500)
    return c


@glyph("uni00A5", 0xA5)
def g_yen(P):
    c = stroke((95, P.cap), (300, 400), P.ds)
    c += stroke((505, P.cap), (300, 400), P.ds)
    c += vstem(P, 300, 0, 420)
    c += hbar(P, 320, 130, 470) + hbar(P, 185, 130, 470)
    return c


@glyph("uni00A4", 0xA4)
def g_currency(P):
    w = capw(P.thin, 125)
    c = ring(300, 330, 128, 128, w)
    out = []
    for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        out += stroke((300 + dx * 105, 330 + dy * 105),
                      (300 + dx * 195, 330 + dy * 195), w)
    return c + out


@glyph("uni00A7", 0xA7)
def g_section(P):
    w = capw(P.stem - 10, 95)
    c = arc_band(300, 540, 118, 96, w, 40, 230)
    c += arc_band(300, 120, 118, 96, w, 220, 50)
    c += ring(300, 330, 130, 122, w)
    return c


@glyph("uni00B6", 0xB6)
def g_paragraph(P):
    c = [e for e in ellipse(245, 520, 155, 200)]
    c += vstem(P, 340, -60, 720, P.thin)
    c += vstem(P, 470, -60, 720, P.thin)
    c += hbar(P, 720 - P.thin / 2, 245, 470)
    return c


@glyph("uni00A9", 0xA9)
def g_copyright(P):
    # ring kept thin even in bold so the inner letter stays separated
    c = ring(300, 360, 235, 235, min(P.thin, 76))
    c += scale_all(g_C(P), 0.40, 0.40, 300, 360)
    return c


@glyph("uni00AE", 0xAE)
def g_registered(P):
    c = ring(300, 360, 235, 235, min(P.thin, 76))
    c += scale_all(g_R(P), 0.40, 0.40, 300, 360)
    return c


@glyph("uni00A8", 0xA8)
def g_dieresis_sp(P):
    return _mk_dieresis(P, LC_Y)


@glyph("uni00B4", 0xB4)
def g_acute_sp(P):
    return _mk_acute(P, LC_Y)


@glyph("uni00AF", 0xAF)
def g_macron_sp(P):
    return _mk_macron(P, LC_Y)


@glyph("uni00B8", 0xB8)
def g_cedilla_sp(P):
    return _mk_cedilla(P, 300)


# --- super/subscripts, ordinals, fractions --------------------------------

def _scaled_digit(P, name, s, cx, base_y):
    """A digit builder result scaled to s, recentered at cx, baseline base_y."""
    cp, fn = BUILDERS[name]
    return translate_all(scale_all(fn(P), s, s, 300, 0), cx - 300, base_y)


@glyph("uni00B9", 0xB9)
def g_onesuperior(P):
    return _scaled_digit(P, "one", 0.58, 300, 300)


@glyph("uni00B2", 0xB2)
def g_twosuperior(P):
    return _scaled_digit(P, "two", 0.58, 300, 300)


@glyph("uni00B3", 0xB3)
def g_threesuperior(P):
    return _scaled_digit(P, "three", 0.58, 300, 300)


@glyph("uni00AA", 0xAA)
def g_ordfeminine(P):
    return translate_all(scale_all(g_a(P), 0.56, 0.56, 300, 0), 0, 330)


@glyph("uni00BA", 0xBA)
def g_ordmasculine(P):
    return translate_all(scale_all(g_o(P), 0.56, 0.56, 300, 0), 0, 330)


def _fraction(P, num_name, den_name):
    c = _scaled_digit(P, num_name, 0.50, 152, 360)
    c += _scaled_digit(P, den_name, 0.50, 448, 0)
    c += stroke((205, -10), (395, 730), P.thin - 6)
    return c


@glyph("uni00BC", 0xBC)
def g_onequarter(P):
    return _fraction(P, "one", "four")


@glyph("uni00BD", 0xBD)
def g_onehalf(P):
    return _fraction(P, "one", "two")


@glyph("uni00BE", 0xBE)
def g_threequarters(P):
    return _fraction(P, "three", "four")


# --- spaces & soft hyphen (share existing glyphs via cmap) ----------------

EXTRA_CMAP = {0xA0: "space", 0xAD: "hyphen"}
