"""Powerline glyphs (PUA: U+E0A0-E0A2, U+E0B0-E0B3).

Separators fill the full line box flush to the cell edges so prompt
segments butt together seamlessly.
"""

from .geometry import poly, stroke, ring, translate_all, scale_all
from .glyphs import BUILDERS

X0, X1 = 0, 600
Y0, Y1 = -250, 950
CY = 350


def _register(cp, fn):
    BUILDERS[f"uni{cp:04X}"] = (cp, fn)


def _branch(P):
    d = P.thin - 4
    c = ring(190, 700, 85, 85, d)
    c += ring(190, -90, 85, 85, d)
    c += ring(445, 555, 85, 85, d)
    c += stroke((190, -10), (190, 620), d)
    c += stroke((190, 230), (400, 480), d)
    return c


def _line_number(P):
    from .glyphs import g_L, g_N
    c = translate_all(scale_all(g_L(P), 0.52, 0.52, 300, 0), -140, 330)
    c += translate_all(scale_all(g_N(P), 0.52, 0.52, 300, 0), 140, -130)
    return c


def _padlock(P):
    from .geometry import arc_band
    d = P.thin - 4
    body = poly((140, -170), (140, 270), (460, 270), (460, -170))
    hole = poly((270, -60), (270, 110), (330, 110), (330, -60))[0]
    c = body + [hole.oriented(clockwise=False)]
    c += arc_band(300, 300, 105, 170, d + 10, 0, 180)
    return c


_register(0xE0A0, _branch)
_register(0xE0A1, _line_number)
_register(0xE0A2, _padlock)

_register(0xE0B0, lambda P: poly((X0, Y0), (X1, CY), (X0, Y1)))
_register(0xE0B2, lambda P: poly((X1, Y0), (X0, CY), (X1, Y1)))


def _chev_r(P):
    w = P.thin + 4
    return (stroke((90, Y1 - 40), (560, CY), w)
            + stroke((560, CY), (90, Y0 + 40), w))


def _chev_l(P):
    w = P.thin + 4
    return (stroke((510, Y1 - 40), (40, CY), w)
            + stroke((40, CY), (510, Y0 + 40), w))


_register(0xE0B1, _chev_r)
_register(0xE0B3, _chev_l)
