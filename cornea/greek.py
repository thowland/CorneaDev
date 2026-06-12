"""Greek (U+0391-03C9), common math operators, and general punctuation.

Greek capitals that are visually identical to Latin (Alpha=A etc.) are
cmap aliases; the rest are drawn here with the same metrics and stroke
parameters as the Latin set.
"""

from .geometry import (stroke, dot, ring, arc_band, translate_all,
                       rotate180_all)
from .glyphs import (BUILDERS, glyph, vstem, hbar, capw,
                     g_O, g_n, g_comma, g_equal, g_asciitilde)

# Identical shapes: alias codepoints to existing glyphs.
EXTRA_CMAP = {
    0x0391: "A", 0x0392: "B", 0x0395: "E", 0x0396: "Z", 0x0397: "H",
    0x0399: "I", 0x039A: "K", 0x039C: "M", 0x039D: "N", 0x039F: "O",
    0x03A1: "P", 0x03A4: "T", 0x03A5: "Y", 0x03A7: "X",
    0x03BF: "o", 0x03BC: "uni00B5",
}


# --- Greek capitals --------------------------------------------------------

@glyph("uni0393", 0x393)        # Gamma
def g_Gamma(P):
    return vstem(P, 105, 0, P.cap) + hbar(P, P.cap - P.thin / 2, 105, 515)


@glyph("uni0394", 0x394)        # Delta
def g_Delta(P):
    return (stroke((300, P.cap + 6), (78, 0), P.ds)
            + stroke((300, P.cap + 6), (522, 0), P.ds)
            + hbar(P, P.thin / 2, 78, 522))


@glyph("uni0398", 0x398)        # Theta
def g_Theta(P):
    return g_O(P) + hbar(P, P.cap / 2, 195, 405)


@glyph("uni039B", 0x39B)        # Lambda
def g_Lambda(P):
    return (stroke((78, 0), (300, P.cap + 6), P.ds)
            + stroke((522, 0), (300, P.cap + 6), P.ds))


@glyph("uni039E", 0x39E)        # Xi
def g_Xi(P):
    return (hbar(P, P.cap - P.thin / 2, 80, 520)
            + hbar(P, 360, 150, 450) + hbar(P, P.thin / 2, 80, 520))


@glyph("uni03A0", 0x3A0)        # Pi
def g_PiCap(P):
    return (vstem(P, 105, 0, P.cap) + vstem(P, 495, 0, P.cap)
            + hbar(P, P.cap - P.thin / 2, 70, 530))


@glyph("uni03A3", 0x3A3)        # Sigma
def g_Sigma(P):
    c = hbar(P, P.cap - P.thin / 2, 100, 500)
    c += hbar(P, P.thin / 2, 100, 500)
    c += stroke((112, P.cap - 30), (330, 372), P.ds)
    c += stroke((330, 348), (112, 30), P.ds)
    return c


@glyph("uni03A6", 0x3A6)        # Phi
def g_PhiCap(P):
    return (vstem(P, 300, 0, P.cap)
            + ring(300, P.cap / 2, 200, 178, P.stem))


@glyph("uni03A8", 0x3A8)        # Psi
def g_PsiCap(P):
    c = vstem(P, 300, 0, P.cap)
    c += vstem(P, 120, 460, P.cap) + vstem(P, 480, 460, P.cap)
    c += arc_band(300, 460, 180, 150, P.stem * 0.9, 180, 360)
    return c


@glyph("uni03A9", 0x3A9)        # Omega
def g_Omega(P):
    c = arc_band(300, 420, 195, 290, P.stem, -60, 240)
    c += vstem(P, 195, 30, 190, P.stem * 0.9)
    c += vstem(P, 405, 30, 190, P.stem * 0.9)
    c += hbar(P, P.thin / 2, 85, 250) + hbar(P, P.thin / 2, 350, 515)
    return c


# --- Greek lowercase -------------------------------------------------------

@glyph("uni03B1", 0x3B1)        # alpha
def g_alpha(P):
    c = ring(280, 270, 185, 282, P.stem)
    c += vstem(P, 448, 160, P.xh)
    c += arc_band(503, 160, 55, 90, P.stem * 0.85, 180, 300)
    return c


@glyph("uni03B2", 0x3B2)        # beta
def g_beta(P):
    w = P.stem - 6
    c = vstem(P, 120, P.desc, 620)
    c += arc_band(295, 620, 168, 105, w, 180, 0)
    c += arc_band(385, 432, 100, 90, w, 90, -90)
    c += arc_band(355, 190, 145, 150, w, 80, -140)
    return c


@glyph("uni03B3", 0x3B3)        # gamma
def g_gamma(P):
    return (stroke((90, P.xh), (290, 40), P.ds)
            + stroke((510, P.xh), (290, 40), P.ds)
            + vstem(P, 290, P.desc, 90, P.ds))


@glyph("uni03B4", 0x3B4)        # delta
def g_delta(P):
    c = ring(300, 200, 190, 212, P.stem)
    c += arc_band(295, 555, 150, 168, P.stem - 6, 215, 25)
    return c


@glyph("uni03B5", 0x3B5)        # epsilon
def g_epsilon(P):
    w = P.stem - 6
    c = arc_band(305, 395, 138, 112, w, 50, 310)
    c += arc_band(305, 158, 148, 112, w, 50, 310)
    return c


@glyph("uni03B6", 0x3B6)        # zeta
def g_zeta(P):
    w = min(P.stem - 8, 100)
    c = hbar(P, 655, 150, 450, P.thin)
    c += stroke((425, 630), (195, 210), P.ds)
    c += arc_band(310, 170, 115, 165, w, 180, 320)
    c += arc_band(420, -55, 75, 80, w * 0.85, 90, -50)
    return c


@glyph("uni03B7", 0x3B7)        # eta
def g_eta(P):
    return g_n(P) + vstem(P, P.lc_stem_r, P.desc, 50)


@glyph("uni03B8", 0x3B8)        # theta
def g_theta(P):
    c = ring(300, 365, 195, 377, P.stem)
    c += hbar(P, 365, 200, 400)
    return c


@glyph("uni03B9", 0x3B9)        # iota
def g_iota(P):
    c = vstem(P, 300, 110, P.xh)
    c += arc_band(385, 112, 85, 90, P.stem, 180, 285)
    return c


@glyph("uni03BA", 0x3BA)        # kappa
def g_kappa(P):
    c = vstem(P, 120, 0, P.xh)
    c += stroke((133, 250), (465, 530), P.ds)
    c += stroke((240, 330), (480, 0), P.ds)
    return c


@glyph("uni03BB", 0x3BB)        # lambda
def g_lambda(P):
    return (stroke((140, P.asc), (470, 0), P.ds)
            + stroke((303, 370), (125, 0), P.ds))


@glyph("uni03BD", 0x3BD)        # nu
def g_nu(P):
    return (stroke((110, P.xh), (300, 0), P.ds)
            + stroke((300, 0), (490, P.xh), P.ds * 0.9))


@glyph("uni03BE", 0x3BE)        # xi
def g_xi(P):
    w = min(P.stem - 8, 100)
    c = arc_band(300, 590, 110, 68, w, 150, -10)
    c += arc_band(280, 390, 110, 95, w, 60, 270)
    c += arc_band(310, 150, 120, 145, w, 180, 320)
    c += arc_band(425, -60, 70, 78, w * 0.85, 90, -50)
    return c


@glyph("uni03C0", 0x3C0)        # pi
def g_pi(P):
    return (hbar(P, P.xh - P.thin / 2, 60, 540, P.thin + 4)
            + vstem(P, 170, 0, P.xh - P.thin)
            + vstem(P, 430, 0, P.xh - P.thin))


@glyph("uni03C1", 0x3C1)        # rho
def g_rho(P):
    c = ring(305, 270, 200, 282, P.stem)
    c += vstem(P, 125, P.desc, 280)
    return c


@glyph("uni03C2", 0x3C2)        # final sigma
def g_finalsigma(P):
    c = arc_band(300, 290, 168, 235, P.stem, 45, 270)
    c += arc_band(295, -55, 115, 115, P.stem * 0.9, 90, -10)
    return c


@glyph("uni03C3", 0x3C3)        # sigma
def g_sigma(P):
    c = ring(280, 255, 190, 267, P.stem)
    c += hbar(P, P.xh - P.thin / 2 - 10, 285, 550, P.thin + 4)
    return c


@glyph("uni03C4", 0x3C4)        # tau
def g_tau(P):
    c = hbar(P, P.xh - P.thin / 2, 110, 490, P.thin + 4)
    c += vstem(P, 300, 90, P.xh)
    c += arc_band(385, 92, 85, 80, P.stem * 0.9, 180, 280)
    return c


@glyph("uni03C5", 0x3C5)        # upsilon
def g_upsilon(P):
    c = arc_band(300, 245, 180, 210, P.stem, 180, 360)
    c += vstem(P, 120, 245, P.xh, P.stem * 0.95)
    c += vstem(P, 480, 245, P.xh, P.stem * 0.95)
    return c


@glyph("uni03C6", 0x3C6)        # phi
def g_phi(P):
    return (ring(300, 270, 195, 280, P.stem)
            + vstem(P, 300, P.desc, 600))


@glyph("uni03C7", 0x3C7)        # chi
def g_chi(P):
    return (stroke((110, P.xh), (490, P.desc), P.ds)
            + stroke((490, P.xh), (110, P.desc), P.ds))


@glyph("uni03C8", 0x3C8)        # psi
def g_psi(P):
    c = vstem(P, 300, P.desc, 600)
    c += arc_band(300, 250, 178, 235, P.stem * 0.9, 180, 360)
    c += vstem(P, 122, 250, P.xh, P.stem * 0.9)
    c += vstem(P, 478, 250, P.xh, P.stem * 0.9)
    return c


@glyph("uni03C9", 0x3C9)        # omega
def g_omega(P):
    s = P.stem * 0.88
    c = arc_band(190, 230, 93, 195, s, 180, 360)
    c += arc_band(410, 230, 93, 195, s, 180, 360)
    c += vstem(P, 97, 230, 525, s * 0.9)
    c += vstem(P, 503, 230, 525, s * 0.9)
    c += vstem(P, 300, 230, 425, s * 0.9)
    return c


# --- math operators --------------------------------------------------------

@glyph("uni2212", 0x2212)       # minus sign
def g_minus(P):
    return hbar(P, 330, 90, 510, P.thin + 8)


@glyph("uni2248", 0x2248)       # almost equal
def g_approxequal(P):
    t = g_asciitilde(P)
    return (translate_all(t, 0, 85) + translate_all(t, 0, -85))


@glyph("uni2260", 0x2260)       # not equal
def g_notequal(P):
    return g_equal(P) + stroke((225, 120), (375, 540), P.ds - 6)


@glyph("uni2264", 0x2264)       # less or equal
def g_lessequal(P):
    return (stroke((450, 620), (150, 390), P.ds)
            + stroke((150, 390), (450, 160), P.ds)
            + hbar(P, 55, 160, 450, P.thin + 4))


@glyph("uni2265", 0x2265)       # greater or equal
def g_greaterequal(P):
    return (stroke((150, 620), (450, 390), P.ds)
            + stroke((450, 390), (150, 160), P.ds)
            + hbar(P, 55, 150, 440, P.thin + 4))


@glyph("uni221E", 0x221E)       # infinity
def g_infinity(P):
    w = capw(P.stem - 6, 100)
    return ring(195, 330, 102, 102, w) + ring(405, 330, 102, 102, w)


@glyph("uni221A", 0x221A)       # square root
def g_radical(P):
    return (stroke((100, 320), (178, 70), P.thin)
            + stroke((178, 70), (288, 660), P.ds)
            + hbar(P, 645, 280, 545, P.thin))


# --- general punctuation ---------------------------------------------------

@glyph("uni2013", 0x2013)       # en dash
def g_endash(P):
    return hbar(P, 330, 80, 520, P.thin + 6)


@glyph("uni2014", 0x2014)       # em dash
def g_emdash(P):
    return hbar(P, 330, 0, 600, P.thin + 6)


@glyph("uni2019", 0x2019)       # right single quote
def g_quoteright(P):
    return translate_all(g_comma(P), 0, 580)


@glyph("uni2018", 0x2018)       # left single quote
def g_quoteleft(P):
    return rotate180_all(g_quoteright(P), 300, 640)


@glyph("uni201D", 0x201D)       # right double quote
def g_quotedblright(P):
    q = g_quoteright(P)
    return translate_all(q, -85, 0) + translate_all(q, 85, 0)


@glyph("uni201C", 0x201C)       # left double quote
def g_quotedblleft(P):
    return rotate180_all(g_quotedblright(P), 300, 640)


@glyph("uni2026", 0x2026)       # horizontal ellipsis
def g_ellipsis_char(P):
    r = P.dotr
    return dot(115, 66, r) + dot(300, 66, r) + dot(485, 66, r)


@glyph("uni2022", 0x2022)       # bullet
def g_bullet(P):
    return dot(300, 330, 115)


# --- arrows ----------------------------------------------------------------

@glyph("uni2192", 0x2192)       # right arrow
def g_arrowright(P):
    w = P.ds - 6
    return (hbar(P, 330, 75, 460, P.thin + 6)
            + stroke((520, 330), (360, 455), w)
            + stroke((520, 330), (360, 205), w))


@glyph("uni2190", 0x2190)       # left arrow
def g_arrowleft(P):
    return [c.scaled(-1, 1, 300, 0) for c in g_arrowright(P)]


@glyph("uni2191", 0x2191)       # up arrow
def g_arrowup(P):
    w = P.ds - 6
    return (vstem(P, 300, 90, 560, P.thin + 6)
            + stroke((300, 600), (180, 450), w)
            + stroke((300, 600), (420, 450), w))


@glyph("uni2193", 0x2193)       # down arrow
def g_arrowdown(P):
    return rotate180_all(g_arrowup(P), 300, 345)
