"""ASCII glyph constructions.

Every builder takes the weight parameter namespace P and returns a list of
geometry.Path contours positioned in a fixed 600-unit advance. Builders are
registered in BUILDERS with their Unicode codepoint, so coverage can grow by
adding modules that register more builders.

Design intent: grotesque/Helvetica-flavored monospace, tall x-height, with
deliberate disambiguation cues (dotted zero, tailed l, serifed i/I/1,
exaggerated brackets and braces).
"""

from .geometry import (poly, rect, stroke, ellipse, dot, ring, arc_band,
                       translate_all)

BUILDERS = {}   # glyph name -> (codepoint or None, fn)
ITALIC_BUILDERS = {}   # glyph name -> fn, used in place of BUILDERS for italic


def glyph(name, cp):
    def deco(fn):
        BUILDERS[name] = (cp, fn)
        return fn
    return deco


def italic_glyph(name):
    """Register a true-italic replacement shape for an existing glyph. Drawn
    upright in normal coordinates; the build applies the slant uniformly."""
    def deco(fn):
        ITALIC_BUILDERS[name] = fn
        return fn
    return deco


# --- small helpers --------------------------------------------------------

def capw(w, r):
    """Cap a stroke width so a ring/band of radius r keeps an open counter."""
    return min(w, r * 0.62)


def vstem(P, x, y0, y1, w=None):
    w = w or P.stem
    return rect(x - w / 2, y0, x + w / 2, y1)


def hbar(P, y, x0, x1, h=None):
    h = h or P.thin
    return rect(x0, y - h / 2, x1, y + h / 2)


# =========================================================================
# Uppercase
# =========================================================================

@glyph("A", 0x41)
def g_A(P):
    apex = (P.mid, P.cap + 6)
    c = stroke((78, 0), apex, P.ds) + stroke((522, 0), apex, P.ds)
    c += hbar(P, 230, 140, 460)
    return c


@glyph("B", 0x42)
def g_B(P):
    x = 95
    c = vstem(P, x, 0, P.cap)
    c += hbar(P, P.cap - P.thin / 2, x, 330)
    c += hbar(P, 384, x, 330)
    c += hbar(P, P.thin / 2, x, 330)
    # two bowls on the right
    c += arc_band(330, 558, 152, 130, P.thin + 8, 90, -90)
    c += arc_band(330, 196, 175, 162, P.thin + 8, 90, -90)
    return c


@glyph("C", 0x43)
def g_C(P):
    # centerline radii derived from O's OUTER radii so C matches O exactly
    return arc_band(300, P.cap / 2, 228 - P.stem / 2,
                    P.cap / 2 + P.ot - P.stem / 2, P.stem, 42, 318)


@glyph("D", 0x44)
def g_D(P):
    x = 95
    c = vstem(P, x, 0, P.cap)
    c += hbar(P, P.cap - P.thin / 2, x, 310)
    c += hbar(P, P.thin / 2, x, 310)
    # bowl rx pulled in (210->198) so the right edge clears the cell wall:
    # at 600 advance the old 562 right extent crowded the next cap (e.g. DE).
    c += arc_band(310, P.cap / 2, 198, P.cap / 2 - P.thin / 2 + 4,
                  P.stem, 90, -90)
    return c


@glyph("E", 0x45)
def g_E(P):
    x = 100
    c = vstem(P, x, 0, P.cap)
    c += hbar(P, P.cap - P.thin / 2, x, 515)
    c += hbar(P, 380, x, 480)
    c += hbar(P, P.thin / 2, x, 515)
    return c


@glyph("F", 0x46)
def g_F(P):
    x = 100
    c = vstem(P, x, 0, P.cap)
    c += hbar(P, P.cap - P.thin / 2, x, 515)
    c += hbar(P, 380, x, 480)
    return c


@glyph("G", 0x47)
def g_G(P):
    c = arc_band(300, P.cap / 2, 228 - P.stem / 2,
                 P.cap / 2 + P.ot - P.stem / 2, P.stem, 36, 318)
    c += hbar(P, 300, 310, 524)
    c += vstem(P, 524 - P.stem / 2, 110, 300)   # spur
    return c


@glyph("H", 0x48)
def g_H(P):
    c = vstem(P, 100, 0, P.cap) + vstem(P, 500, 0, P.cap)
    c += hbar(P, 372, 100, 500)
    return c


@glyph("I", 0x49)
def g_I(P):
    # serifed I: a deliberate cue vs l and 1
    c = vstem(P, P.mid, 0, P.cap)
    c += hbar(P, P.cap - P.thin / 2, 150, 450)
    c += hbar(P, P.thin / 2, 150, 450)
    return c


@glyph("J", 0x4A)
def g_J(P):
    c = vstem(P, 430, 170, P.cap)
    c += arc_band(245, 170, 185, 165, P.stem, 0, -180)
    c += hbar(P, P.cap - P.thin / 2, 260, 472)
    return c


@glyph("K", 0x4B)
def g_K(P):
    c = vstem(P, 105, 0, P.cap)
    c += stroke((118, 330), (505, P.cap - 26), P.ds)
    c += stroke((230, 420), (520, 0), P.ds)
    return c


@glyph("L", 0x4C)
def g_L(P):
    return vstem(P, 105, 0, P.cap) + hbar(P, P.thin / 2, 105, 520)


@glyph("M", 0x4D)
def g_M(P):
    # stems pulled in (85/515 -> 92/508) to even the sidebearings with the
    # rest of the caps; previously M crowded its neighbours (e.g. MNO).
    s = P.stem * 0.92
    d = P.ds * 0.88
    c = vstem(P, 92, 0, P.cap, s) + vstem(P, 508, 0, P.cap, s)
    c += stroke((99, P.cap - 16), (300, 200), d)
    c += stroke((501, P.cap - 16), (300, 200), d)
    return c


@glyph("N", 0x4E)
def g_N(P):
    c = vstem(P, 95, 0, P.cap) + vstem(P, 505, 0, P.cap)
    c += stroke((105, P.cap - 30), (495, 30), P.ds)
    return c


@glyph("O", 0x4F)
def g_O(P):
    return ring(300, P.cap / 2, 228, P.cap / 2 + P.ot, P.stem)


@glyph("P", 0x50)
def g_P(P):
    x = 100
    c = vstem(P, x, 0, P.cap)
    c += hbar(P, P.cap - P.thin / 2, x, 330)
    c += hbar(P, 332, x, 330)
    c += arc_band(330, 526, 165, 162, P.stem - 4, 90, -90)
    return c


@glyph("Q", 0x51)
def g_Q(P):
    c = ring(300, P.cap / 2, 228, P.cap / 2 + P.ot, P.stem)
    # tail end pulled in (530->513) so it no longer poked past the cell wall
    # and crowded the next cap (e.g. QR).
    c += stroke((330, 170), (513, -60), P.ds)
    return c


@glyph("R", 0x52)
def g_R(P):
    c = g_P(P)
    c += stroke((300, 340), (515, 0), P.ds)
    return c


def _s_shape(P, h, rx=152):
    """S as two arcs joined by a short spine. Upper arc exits lower-left
    heading right-down; lower arc is entered at the matching tangent, so the
    spine connects them smoothly."""
    import math
    cx = P.mid
    w = min(P.stem, 116)
    cy_top, cy_bot = h * 0.75, h * 0.25
    ry = (h + P.ot) - cy_top - w / 2
    c = arc_band(cx, cy_top, rx, ry, w, 30, 245)
    c += arc_band(cx, cy_bot, rx, ry, w, 65, -115)
    p_top = (cx + rx * math.cos(math.radians(245)),
             cy_top + ry * math.sin(math.radians(245)))
    p_bot = (cx + rx * math.cos(math.radians(65)),
             cy_bot + ry * math.sin(math.radians(65)))
    c += stroke(p_top, p_bot, w)
    return c


@glyph("S", 0x53)
def g_S(P):
    return _s_shape(P, P.cap)


@glyph("T", 0x54)
def g_T(P):
    c = hbar(P, P.cap - P.thin / 2, 70, 530)
    c += vstem(P, P.mid, 0, P.cap)
    return c


@glyph("U", 0x55)
def g_U(P):
    c = vstem(P, 95, 195, P.cap) + vstem(P, 505, 195, P.cap)
    c += arc_band(300, 200, 205, 200 + P.ot - P.stem / 2, P.stem, 180, 360)
    return c


@glyph("V", 0x56)
def g_V(P):
    return (stroke((80, P.cap), (300, 0), P.ds)
            + stroke((520, P.cap), (300, 0), P.ds))


@glyph("W", 0x57)
def g_W(P):
    d = P.ds * 0.8
    return (stroke((62, P.cap), (172, 0), d) + stroke((172, 0), (300, 500), d)
            + stroke((300, 500), (428, 0), d)
            + stroke((428, 0), (538, P.cap), d))


@glyph("X", 0x58)
def g_X(P):
    return (stroke((88, P.cap), (512, 0), P.ds)
            + stroke((512, P.cap), (88, 0), P.ds))


@glyph("Y", 0x59)
def g_Y(P):
    c = stroke((78, P.cap), (300, 330), P.ds)
    c += stroke((522, P.cap), (300, 330), P.ds)
    c += vstem(P, 300, 0, 360)
    return c


@glyph("Z", 0x5A)
def g_Z(P):
    c = hbar(P, P.cap - P.thin / 2, 95, 505)
    c += hbar(P, P.thin / 2, 95, 505)
    c += stroke((468, P.cap - P.thin), (132, P.thin), P.ds)
    return c


# =========================================================================
# Lowercase
# =========================================================================

@glyph("a", 0x61)
def g_a(P):
    # two-story a: hook runs from the stem over the top and down the left
    # into the bowl; the bowl ring's top edge forms the middle bar. The hook's
    # outer-left extremum is solved to land exactly on the bowl's, so the top
    # never overhangs the bottom.
    w = P.stem - 14
    hook_cy = 420
    hook_ry = (P.xh + P.ot) - hook_cy - w / 2
    bowl_cx, bowl_rx = 295, 186
    bowl_left = bowl_cx - bowl_rx
    hook_cx = (P.lc_stem_r + bowl_left + w / 2) / 2
    c = vstem(P, P.lc_stem_r, 0, P.xh - 25)
    c += arc_band(hook_cx, hook_cy, P.lc_stem_r - hook_cx, hook_ry, w, 0, 205)
    c += ring(bowl_cx, 153, bowl_rx, 165, P.stem)
    return c


# --- true-italic replacement shapes (drawn upright; slanted at build time) --

@italic_glyph("a")
def g_a_italic(P):
    # single-story a: round bowl with a straight stem on its right edge and a
    # small exit tail at the baseline -- the defining italic substitution.
    bowl_cx, bowl_rx = 278, 192
    c = ring(bowl_cx, P.xh / 2, bowl_rx, P.xh / 2 + P.ot, P.stem)
    c += vstem(P, P.lc_stem_r, 0, P.xh)
    c += arc_band(P.lc_stem_r - 66, 78, 66, 70, P.stem - 14, -88, -8)
    return c


@italic_glyph("f")
def g_f_italic(P):
    # cursive f: the stem descends below the baseline and hooks left, the
    # second hallmark of a true italic.
    c = vstem(P, 288, -118, 600)
    c += arc_band(408, 600, 120, 100, P.stem - 6, 180, 64)    # top ear
    c += arc_band(206, -118, 84, 96, P.stem - 6, 0, -158)     # descender hook
    c += hbar(P, P.xh - P.thin / 2, 138, 470)                 # crossbar
    return c


def _round_lc(P):
    """Shared metrics for o-like bowls: OUTER radii, centered in the cell.
    Every round lowercase (o b d p q c e g) uses exactly these extents."""
    return dict(cx=300, cy=P.xh / 2, rx=P.lc_rx, ry=P.xh / 2 + P.ot)


def _arch(P, cy, w=None):
    """n/h/u arch between the shared lowercase stems; returns (cx, rx, ry)
    with ry computed so the outer edge lands exactly on x-height+overshoot."""
    w = w or P.stem
    cx = (P.lc_stem_l + P.lc_stem_r) / 2
    rx = (P.lc_stem_r - P.lc_stem_l) / 2
    ry = (P.xh + P.ot) - cy - w / 2
    return cx, rx, ry


@glyph("b", 0x62)
def g_b(P):
    m = _round_lc(P)
    c = vstem(P, P.lc_stem_l, 0, P.asc)
    c += ring(m["cx"], m["cy"], m["rx"], m["ry"], P.stem)
    return c


@glyph("c", 0x63)
def g_c(P):
    m = _round_lc(P)
    return arc_band(m["cx"], m["cy"], m["rx"] - P.stem / 2,
                    m["ry"] - P.stem / 2, P.stem, 40, 320)


@glyph("d", 0x64)
def g_d(P):
    m = _round_lc(P)
    c = vstem(P, P.lc_stem_r, 0, P.asc)
    c += ring(m["cx"], m["cy"], m["rx"], m["ry"], P.stem)
    return c


@glyph("e", 0x65)
def g_e(P):
    m = _round_lc(P)
    c = arc_band(m["cx"], m["cy"], m["rx"] - P.stem / 2,
                 m["ry"] - P.stem / 2, P.stem, -25, 298)
    c += hbar(P, m["cy"] + 35, 95, 505)
    return c


@glyph("f", 0x66)
def g_f(P):
    c = vstem(P, 265, 0, 620)
    c += arc_band(385, 620, 120, 100, P.stem - 6, 180, 64)
    c += hbar(P, P.xh - P.thin / 2, 120, 445)
    return c


@glyph("g", 0x67)
def g_g(P):
    m = _round_lc(P)
    c = ring(m["cx"], m["cy"], m["rx"], m["ry"], P.stem)
    c += vstem(P, P.lc_stem_r, -75, P.xh)
    c += arc_band(P.lc_stem_r - 162, -75, 162, 125, P.stem, 0, -195)
    return c


@glyph("h", 0x68)
def g_h(P):
    cx, rx, ry = _arch(P, 380)
    c = vstem(P, P.lc_stem_l, 0, P.asc)
    c += arc_band(cx, 380, rx, ry, P.stem, 0, 180)
    c += vstem(P, P.lc_stem_r, 0, 388)
    return c


def _i_base(P):
    """Dotless i: stem + flag + foot, shared by i and the accented forms."""
    c = vstem(P, 300, 0, P.xh)
    c += rect(185, P.xh - 70, 300, P.xh)            # top-left flag
    c += hbar(P, P.thin / 2, 175, 425)              # foot
    return c


@glyph("i", 0x69)
def g_i(P):
    # serif flag + foot: strong cue vs l, 1, |
    return _i_base(P) + dot(300, P.xh + 130, P.dotr)


@glyph("j", 0x6A)
def g_j(P):
    c = vstem(P, 350, -100, P.xh)
    c += rect(235, P.xh - 70, 350, P.xh)
    c += arc_band(238, -98, 113, 105, P.stem, 0, -150)
    c += dot(350, P.xh + 130, P.dotr)
    return c


@glyph("k", 0x6B)
def g_k(P):
    c = vstem(P, P.lc_stem_l, 0, P.asc)
    c += stroke((P.lc_stem_l + 13, 230), (480, P.xh - 14), P.ds)
    c += stroke((255, 330), (500, 0), P.ds)
    return c


@glyph("l", 0x6C)
def g_l(P):
    # tailed l: unmistakable vs 1, I, |
    c = vstem(P, 275, 120, P.asc)
    c += arc_band(380, 122, 105, 90, P.stem, 180, 295)
    return c


@glyph("m", 0x6D)
def g_m(P):
    s = P.stem * 0.86
    xl, xr = 95, 505
    cy = 400
    ry = (P.xh + P.ot) - cy - s / 2
    rx = (300 - xl) / 2
    c = vstem(P, xl, 0, P.xh, s)
    c += vstem(P, 300, 0, cy + 8, s)
    c += vstem(P, xr, 0, cy + 8, s)
    c += arc_band(xl + rx, cy, rx, ry, s, 0, 180)
    c += arc_band(300 + rx, cy, rx, ry, s, 0, 180)
    return c


@glyph("n", 0x6E)
def g_n(P):
    cx, rx, ry = _arch(P, 380)
    c = vstem(P, P.lc_stem_l, 0, P.xh)
    c += arc_band(cx, 380, rx, ry, P.stem, 0, 180)
    c += vstem(P, P.lc_stem_r, 0, 388)
    return c


@glyph("o", 0x6F)
def g_o(P):
    m = _round_lc(P)
    return ring(m["cx"], m["cy"], m["rx"], m["ry"], P.stem)


@glyph("p", 0x70)
def g_p(P):
    m = _round_lc(P)
    c = vstem(P, P.lc_stem_l, P.desc, P.xh)
    c += ring(m["cx"], m["cy"], m["rx"], m["ry"], P.stem)
    return c


@glyph("q", 0x71)
def g_q(P):
    m = _round_lc(P)
    c = vstem(P, P.lc_stem_r, P.desc, P.xh)
    c += ring(m["cx"], m["cy"], m["rx"], m["ry"], P.stem)
    return c


@glyph("r", 0x72)
def g_r(P):
    w = P.stem - 4
    cy = 385
    ry = (P.xh + P.ot) - cy - w / 2
    c = vstem(P, P.lc_stem_l + 15, 0, P.xh)
    c += arc_band(310, cy, 175, ry, w, 180, 50)
    return c


@glyph("s", 0x73)
def g_s(P):
    return _s_shape(P, P.xh, rx=148)


@glyph("t", 0x74)
def g_t(P):
    c = vstem(P, 270, 110, 680)
    c += hbar(P, P.xh - P.thin / 2, 115, 460)
    c += arc_band(372, 112, 102, 90, P.stem, 180, 290)
    return c


@glyph("u", 0x75)
def g_u(P):
    cx = (P.lc_stem_l + P.lc_stem_r) / 2
    rx = (P.lc_stem_r - P.lc_stem_l) / 2
    cy = 165
    ry = cy + P.ot - P.stem / 2     # outer edge exactly at baseline overshoot
    c = vstem(P, P.lc_stem_l, 160, P.xh) + vstem(P, P.lc_stem_r, 0, P.xh)
    c += arc_band(cx, cy, rx, ry, P.stem, 180, 360)
    return c


@glyph("v", 0x76)
def g_v(P):
    return (stroke((85, P.xh), (300, 0), P.ds)
            + stroke((515, P.xh), (300, 0), P.ds))


@glyph("w", 0x77)
def g_w(P):
    d = P.ds * 0.8
    return (stroke((58, P.xh), (170, 0), d) + stroke((170, 0), (300, 460), d)
            + stroke((300, 460), (430, 0), d)
            + stroke((430, 0), (542, P.xh), d))


@glyph("x", 0x78)
def g_x(P):
    return (stroke((95, P.xh), (505, 0), P.ds)
            + stroke((505, P.xh), (95, 0), P.ds))


@glyph("y", 0x79)
def g_y(P):
    return (stroke((85, P.xh), (310, 22), P.ds)
            + stroke((515, P.xh), (186, P.desc), P.ds))


@glyph("z", 0x7A)
def g_z(P):
    c = hbar(P, P.xh - P.thin / 2, 105, 495)
    c += hbar(P, P.thin / 2, 105, 495)
    c += stroke((462, P.xh - P.thin), (138, P.thin), P.ds)
    return c


# =========================================================================
# Digits (cap height)
# =========================================================================

@glyph("zero", 0x30)
def g_zero(P):
    c = ring(300, P.cap / 2, 212, P.cap / 2 + P.ot, P.stem)
    style = getattr(P, "zero_style", "dotted")
    if style == "dotted":
        c += dot(300, P.cap / 2, P.dotr - 4)
    elif style == "slashed":
        c += stroke((205, 140), (395, P.cap - 140), P.thin - 8)
    return c


@glyph("one", 0x31)
def g_one(P):
    c = vstem(P, 300, 0, P.cap)
    c += stroke((140, 545), (300 - P.stem / 2 + 20, P.cap - 22), P.ds)
    c += hbar(P, P.thin / 2, 150, 450)   # foot serif
    return c


@glyph("two", 0x32)
def g_two(P):
    cy = 522
    ry = (P.cap + P.ot) - cy - P.stem / 2
    c = arc_band(298, cy, 186, ry, P.stem, 170, -2)
    c += stroke((478, 480), (118, P.thin + 16), P.ds + 6)
    c += hbar(P, P.thin / 2, 92, 508)
    return c


@glyph("three", 0x33)
def g_three(P):
    cy_t, cy_b = 540, 188
    ry_t = (P.cap + P.ot) - cy_t - P.stem / 2
    ry_b = cy_b + P.ot - P.stem / 2
    c = arc_band(282, cy_t, 178, ry_t, P.stem, 152, -64)
    c += arc_band(282, cy_b, 196, ry_b, P.stem, 116, -152)
    return c


@glyph("four", 0x34)
def g_four(P):
    c = vstem(P, 392, 0, P.cap)
    c += stroke((392, P.cap - 18), (108, 232), P.ds)
    c += hbar(P, 232, 62, 538)
    return c


@glyph("five", 0x35)
def g_five(P):
    c = hbar(P, P.cap - P.thin / 2, 112, 492)
    c += vstem(P, 112, 408, P.cap)
    c += hbar(P, 432, 112, 330)
    cy = 235
    c += arc_band(300, cy, 188, cy + P.ot - P.stem / 2, P.stem, 96, -158)
    return c


@glyph("six", 0x36)
def g_six(P):
    cy = 222
    tail_ry = (P.cap + P.ot) - cy - P.stem / 2
    c = ring(300, cy, 208, 232, P.stem)
    c += arc_band(300, cy, 208 - P.stem / 2, tail_ry, P.stem, 90, 158)
    return c


@glyph("seven", 0x37)
def g_seven(P):
    c = hbar(P, P.cap - P.thin / 2, 92, 508)
    c += stroke((492, P.cap - P.thin), (205, 0), P.ds + 4)
    if getattr(P, "seven_style", "plain") == "crossbar":
        c += hbar(P, 360, 160, 440)
    return c


@glyph("eight", 0x38)
def g_eight(P):
    c = ring(300, 536, 178, (P.cap + P.ot) - 536, P.stem)
    c += ring(300, 184, 205, 184 + P.ot, P.stem)
    return c


@glyph("nine", 0x39)
def g_nine(P):
    from .geometry import rotate180_all
    return rotate180_all(g_six(P), 300, P.cap / 2)


# =========================================================================
# Punctuation & symbols
# =========================================================================

@glyph("space", 0x20)
def g_space(P):
    return []


@glyph("exclam", 0x21)
def g_exclam(P):
    c = vstem(P, 300, 220, P.cap, P.stem + 6)
    c += dot(300, 66, P.dotr + 8)
    return c


@glyph("quotedbl", 0x22)
def g_quotedbl(P):
    w = P.thin
    return (rect(218 - w / 2, 520, 218 + w / 2, P.cap + 20)
            + rect(382 - w / 2, 520, 382 + w / 2, P.cap + 20))


@glyph("quotesingle", 0x27)
def g_quotesingle(P):
    w = P.thin
    return rect(300 - w / 2, 520, 300 + w / 2, P.cap + 20)


@glyph("grave", 0x60)
def g_grave(P):
    # heavy and clearly slanted: must never be mistaken for '
    return stroke((225, P.cap + 20), (375, 520), P.thin + 14)


@glyph("numbersign", 0x23)
def g_numbersign(P):
    c = vstem(P, 222, 70, 650, P.thin + 6) + vstem(P, 378, 70, 650, P.thin + 6)
    c += hbar(P, 462, 78, 522) + hbar(P, 248, 78, 522)
    return c


@glyph("dollar", 0x24)
def g_dollar(P):
    c = _s_shape(P, P.cap)
    c += vstem(P, 300, -70, P.cap + 70, P.thin - 6)
    return c


@glyph("percent", 0x25)
def g_percent(P):
    # Bold clogging fix: open the two ring counters (slightly larger rings,
    # tighter stroke cap) and lighten the slash so it doesn't dominate at 12pt.
    rw = min(P.thin, 110 * 0.55)
    c = ring(158, 560, 110, 114, rw)
    c += ring(442, 160, 110, 114, rw)
    c += stroke((470, 700), (130, 20), min(P.thin, 84))
    return c


@glyph("ampersand", 0x26)
def g_ampersand(P):
    # Bold clogging fix: open the small upper eye and lighten the two tails so
    # the loops survive at 12pt instead of merging into a blob.
    # Larger upper eye overlapping the bowl: keeps the counter open even with a
    # connecting wall, so the two loops don't merge into a blob (Bold) nor
    # detach into a floating ring (thin wall).
    c = ring(235, 528, 135, 165, capw(P.stem - 4, 135))
    c += ring(235, 192, 182, 205, capw(P.stem - 8, 182))
    c += stroke((310, 70), (556, 344), P.ds)
    c += stroke((448, 214), (556, 0), P.ds - 12)
    return c


@glyph("parenleft", 0x28)
def g_parenleft(P):
    return arc_band(560, 290, 330, 560, P.stem, 128, 232)


@glyph("parenright", 0x29)
def g_parenright(P):
    return arc_band(40, 290, 330, 560, P.stem, 52, -52)


@glyph("asterisk", 0x2A)
def g_asterisk(P):
    # Bold clogging fix: thinner, longer spokes so the six arms stay distinct
    # at 12pt instead of fusing into a single dot (and not read as a period).
    import math
    c = []
    cx, cy, r = 300, 500, 172
    aw = min(P.thin - 8, 70)
    for ang in (90, 150, 210, 270, 330, 30):
        a = math.radians(ang)
        c += stroke((cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a)), aw)
    return c


@glyph("plus", 0x2B)
def g_plus(P):
    return (hbar(P, 330, 105, 495, P.thin + 6)
            + vstem(P, 300, 135, 525, P.thin + 6))


@glyph("comma", 0x2C)
def g_comma(P):
    c = dot(300, 70, P.dotr + 8)
    c += poly((332, 96), (358, 50), (252, -118), (222, -84))
    return c


@glyph("hyphen", 0x2D)
def g_hyphen(P):
    return hbar(P, 330, 140, 460, P.thin + 12)


@glyph("period", 0x2E)
def g_period(P):
    return dot(300, 66, P.dotr + 8)


@glyph("slash", 0x2F)
def g_slash(P):
    return stroke((462, P.cap + 50), (138, -110), P.stem - 8)


@glyph("colon", 0x3A)
def g_colon(P):
    return dot(300, 66, P.dotr + 8) + dot(300, 440, P.dotr + 8)


@glyph("semicolon", 0x3B)
def g_semicolon(P):
    return g_comma(P) + dot(300, 440, P.dotr + 8)


@glyph("less", 0x3C)
def g_less(P):
    return (stroke((455, 596), (135, 330), P.ds)
            + stroke((135, 330), (455, 64), P.ds))


@glyph("equal", 0x3D)
def g_equal(P):
    return (hbar(P, 240, 105, 495, P.thin + 6)
            + hbar(P, 420, 105, 495, P.thin + 6))


@glyph("greater", 0x3E)
def g_greater(P):
    return (stroke((145, 596), (465, 330), P.ds)
            + stroke((465, 330), (145, 64), P.ds))


@glyph("question", 0x3F)
def g_question(P):
    c = arc_band(300, 545, 158, 162, P.stem, 172, -76)
    c += vstem(P, 322, 230, 392, P.stem)
    c += dot(300, 66, P.dotr + 8)
    return c


@glyph("at", 0x40)
def g_at(P):
    w = capw(P.thin + 2, 118)
    c = arc_band(300, 320, 245, 380, capw(P.thin + 8, 245), -38, 262)
    c += ring(308, 330, 118, 128, w)
    c += vstem(P, 425, 205, 450, w)
    c += arc_band(330, 240, 110, 38, w, 180, 320)
    return c


@glyph("bracketleft", 0x5B)
def g_bracketleft(P):
    # exaggerated: tall with long flanges
    c = vstem(P, 240, -150, 770)
    c += hbar(P, 770 - P.thin / 2, 240, 455)
    c += hbar(P, -150 + P.thin / 2, 240, 455)
    return c


@glyph("bracketright", 0x5D)
def g_bracketright(P):
    c = vstem(P, 360, -150, 770)
    c += hbar(P, 770 - P.thin / 2, 145, 360)
    c += hbar(P, -150 + P.thin / 2, 145, 360)
    return c


@glyph("backslash", 0x5C)
def g_backslash(P):
    return stroke((138, P.cap + 50), (462, -110), P.stem - 8)


@glyph("asciicircum", 0x5E)
def g_asciicircum(P):
    return (stroke((300, P.cap + 10), (140, 452), P.ds)
            + stroke((300, P.cap + 10), (460, 452), P.ds))


@glyph("underscore", 0x5F)
def g_underscore(P):
    return rect(45, -160, 555, -160 + P.thin + 4)


@glyph("braceleft", 0x7B)
def g_braceleft(P):
    w = P.stem - 4
    c = arc_band(442, 648, 142, 122, w, 90, 180)
    c += vstem(P, 300, 460, 650, w)
    c += arc_band(168, 460, 132, 152, w, 0, -88)
    c += arc_band(168, 158, 132, 152, w, 88, 0)
    c += vstem(P, 300, -32, 158, w)
    c += arc_band(442, -28, 142, 122, w, 180, 270)
    return c


@glyph("braceright", 0x7D)
def g_braceright(P):
    w = P.stem - 4
    c = arc_band(158, 648, 142, 122, w, 90, 0)
    c += vstem(P, 300, 460, 650, w)
    c += arc_band(432, 460, 132, 152, w, 180, 268)
    c += arc_band(432, 158, 132, 152, w, 92, 180)
    c += vstem(P, 300, -32, 158, w)
    c += arc_band(158, -28, 142, 122, w, 0, -90)
    return c


@glyph("bar", 0x7C)
def g_bar(P):
    return vstem(P, 300, -150, 770, P.stem - 6)


@glyph("asciitilde", 0x7E)
def g_asciitilde(P):
    w = capw(P.thin + 4, 95)
    c = arc_band(200, 318, 100, 62, w, 155, 25)
    c += arc_band(400, 342, 100, 62, w, 205, 335)
    return c


# --- .notdef --------------------------------------------------------------

def g_notdef(P):
    c = rect(80, 0, 520, P.cap)
    inner = rect(80 + P.thin, P.thin, 520 - P.thin, P.cap - P.thin)
    c += [inner[0].oriented(clockwise=False)]
    return c


BUILDERS[".notdef"] = (None, g_notdef)
