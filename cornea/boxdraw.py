"""Box Drawing (U+2500-257F) and Block Elements (U+2580-259F).

Glyphs fill the full line box (x 0..600, y -250..950, matching hhea/win
metrics) so lines and blocks connect seamlessly across cells and rows.
Single/heavy chars are generated from an arm table; double-line chars are
hand-specified for correct junctions.
"""

from .geometry import rect, stroke, arc_band
from .glyphs import BUILDERS

X0, X1 = 0, 600
Y0, Y1 = -250, 950
CX, CY = 300, 350
ARC_R = 160


def _register(cp, fn):
    BUILDERS[f"uni{cp:04X}"] = (cp, fn)


def _H(y, x0, x1, w):
    return rect(x0, y - w / 2, x1, y + w / 2)


def _V(x, y0, y1, w):
    return rect(x - w / 2, y0, x + w / 2, y1)


def _ld(P):                      # light line width
    return P.thin - 4


def _hd(P):                      # heavy line width
    return (P.thin - 4) * 1.9


def _width(P, style):
    return 0 if style == 0 else (_ld(P) if style == 1 else _hd(P))


# --- single/heavy arms (2500-254B, 2574-257F) -----------------------------

def _arms(u, d, l, r):
    def fn(P, u=u, d=d, l=l, r=r):
        c = []
        wv = max(_width(P, u), _width(P, d))   # for horizontal extension
        wh = max(_width(P, l), _width(P, r))   # for vertical extension
        if u:
            w = _width(P, u)
            ext = wh / 2 if wh else w / 2
            c += _V(CX, CY - ext, Y1, w)
        if d:
            w = _width(P, d)
            ext = wh / 2 if wh else w / 2
            c += _V(CX, Y0, CY + ext, w)
        if l:
            w = _width(P, l)
            ext = wv / 2 if wv else w / 2
            c += _H(CY, X0, CX + ext, w)
        if r:
            w = _width(P, r)
            ext = wv / 2 if wv else w / 2
            c += _H(CY, CX - ext, X1, w)
        return c
    return fn


_ARM_TABLE = {
    0x2500: (0, 0, 1, 1), 0x2501: (0, 0, 2, 2),
    0x2502: (1, 1, 0, 0), 0x2503: (2, 2, 0, 0),
    0x250C: (0, 1, 0, 1), 0x250D: (0, 1, 0, 2),
    0x250E: (0, 2, 0, 1), 0x250F: (0, 2, 0, 2),
    0x2510: (0, 1, 1, 0), 0x2511: (0, 1, 2, 0),
    0x2512: (0, 2, 1, 0), 0x2513: (0, 2, 2, 0),
    0x2514: (1, 0, 0, 1), 0x2515: (1, 0, 0, 2),
    0x2516: (2, 0, 0, 1), 0x2517: (2, 0, 0, 2),
    0x2518: (1, 0, 1, 0), 0x2519: (1, 0, 2, 0),
    0x251A: (2, 0, 1, 0), 0x251B: (2, 0, 2, 0),
    0x251C: (1, 1, 0, 1), 0x251D: (1, 1, 0, 2),
    0x251E: (2, 1, 0, 1), 0x251F: (1, 2, 0, 1),
    0x2520: (2, 2, 0, 1), 0x2521: (2, 1, 0, 2),
    0x2522: (1, 2, 0, 2), 0x2523: (2, 2, 0, 2),
    0x2524: (1, 1, 1, 0), 0x2525: (1, 1, 2, 0),
    0x2526: (2, 1, 1, 0), 0x2527: (1, 2, 1, 0),
    0x2528: (2, 2, 1, 0), 0x2529: (2, 1, 2, 0),
    0x252A: (1, 2, 2, 0), 0x252B: (2, 2, 2, 0),
    0x252C: (0, 1, 1, 1), 0x252D: (0, 1, 2, 1),
    0x252E: (0, 1, 1, 2), 0x252F: (0, 1, 2, 2),
    0x2530: (0, 2, 1, 1), 0x2531: (0, 2, 2, 1),
    0x2532: (0, 2, 1, 2), 0x2533: (0, 2, 2, 2),
    0x2534: (1, 0, 1, 1), 0x2535: (1, 0, 2, 1),
    0x2536: (1, 0, 1, 2), 0x2537: (1, 0, 2, 2),
    0x2538: (2, 0, 1, 1), 0x2539: (2, 0, 2, 1),
    0x253A: (2, 0, 1, 2), 0x253B: (2, 0, 2, 2),
    0x253C: (1, 1, 1, 1), 0x253D: (1, 1, 2, 1),
    0x253E: (1, 1, 1, 2), 0x253F: (1, 1, 2, 2),
    0x2540: (2, 1, 1, 1), 0x2541: (1, 2, 1, 1),
    0x2542: (2, 2, 1, 1), 0x2543: (2, 1, 2, 1),
    0x2544: (2, 1, 1, 2), 0x2545: (1, 2, 2, 1),
    0x2546: (1, 2, 1, 2), 0x2547: (2, 1, 2, 2),
    0x2548: (1, 2, 2, 2), 0x2549: (2, 2, 2, 1),
    0x254A: (2, 2, 1, 2), 0x254B: (2, 2, 2, 2),
    0x2574: (0, 0, 1, 0), 0x2575: (1, 0, 0, 0),
    0x2576: (0, 0, 0, 1), 0x2577: (0, 1, 0, 0),
    0x2578: (0, 0, 2, 0), 0x2579: (2, 0, 0, 0),
    0x257A: (0, 0, 0, 2), 0x257B: (0, 2, 0, 0),
    0x257C: (0, 0, 1, 2), 0x257D: (1, 2, 0, 0),
    0x257E: (0, 0, 2, 1), 0x257F: (2, 1, 0, 0),
}
for cp, arms in _ARM_TABLE.items():
    _register(cp, _arms(*arms))


# --- dashed (2504-250B triple/quadruple, 254C-254F double) -----------------

def _dashed(n, vertical, heavy):
    def fn(P, n=n, vertical=vertical, heavy=heavy):
        w = _hd(P) if heavy else _ld(P)
        c = []
        if vertical:
            seg = (Y1 - Y0) / n
            for i in range(n):
                c += _V(CX, Y0 + i * seg + seg * 0.15,
                        Y0 + i * seg + seg * 0.85, w)
        else:
            seg = (X1 - X0) / n
            for i in range(n):
                c += _H(CY, i * seg + seg * 0.15, i * seg + seg * 0.85, w)
        return c
    return fn


for cp, (n, vert, heavy) in {
        0x2504: (3, False, False), 0x2505: (3, False, True),
        0x2506: (3, True, False), 0x2507: (3, True, True),
        0x2508: (4, False, False), 0x2509: (4, False, True),
        0x250A: (4, True, False), 0x250B: (4, True, True),
        0x254C: (2, False, False), 0x254D: (2, False, True),
        0x254E: (2, True, False), 0x254F: (2, True, True)}.items():
    _register(cp, _dashed(n, vert, heavy))


# --- double lines (2550-256C) ----------------------------------------------

def _o(P):
    return _ld(P) * 1.25


def _corner(P, h, v):
    """Double corner: horizontal arm toward h (+1 right), vertical toward
    v (+1 up). Outer and inner rails pair up for clean nested corners."""
    d, o = _ld(P), _o(P)
    c = []
    # outer: vertical rail on the far side of the horizontal direction
    xo, xi = CX - h * o, CX + h * o
    yo, yi = CY - v * o, CY + v * o
    v_edge = Y1 if v > 0 else Y0
    h_edge = X1 if h > 0 else X0
    c += _V(xo, *sorted((v_edge, yo - v * d / 2)), d)
    c += _H(yo, *sorted((h_edge, xo - h * d / 2)), d)
    c += _V(xi, *sorted((v_edge, yi - v * d / 2)), d)
    c += _H(yi, *sorted((h_edge, xi - h * d / 2)), d)
    return c


def _dbl(spec):
    def fn(P, spec=spec):
        d, o = _ld(P), _o(P)
        c = []
        for item in spec(P, d, o):
            c += item
        return c
    return fn


_DOUBLES = {
    0x2550: lambda P, d, o: [_H(CY - o, X0, X1, d), _H(CY + o, X0, X1, d)],
    0x2551: lambda P, d, o: [_V(CX - o, Y0, Y1, d), _V(CX + o, Y0, Y1, d)],
    0x2552: lambda P, d, o: [_V(CX, Y0, CY + o + d / 2, d),
                             _H(CY + o, CX - d / 2, X1, d),
                             _H(CY - o, CX - d / 2, X1, d)],
    0x2553: lambda P, d, o: [_V(CX - o, Y0, CY + d / 2, d),
                             _V(CX + o, Y0, CY + d / 2, d),
                             _H(CY, CX - o - d / 2, X1, d)],
    0x2554: lambda P, d, o: [_corner(P, +1, -1)],
    0x2555: lambda P, d, o: [_V(CX, Y0, CY + o + d / 2, d),
                             _H(CY + o, X0, CX + d / 2, d),
                             _H(CY - o, X0, CX + d / 2, d)],
    0x2556: lambda P, d, o: [_V(CX - o, Y0, CY + d / 2, d),
                             _V(CX + o, Y0, CY + d / 2, d),
                             _H(CY, X0, CX + o + d / 2, d)],
    0x2557: lambda P, d, o: [_corner(P, -1, -1)],
    0x2558: lambda P, d, o: [_V(CX, CY - o - d / 2, Y1, d),
                             _H(CY + o, CX - d / 2, X1, d),
                             _H(CY - o, CX - d / 2, X1, d)],
    0x2559: lambda P, d, o: [_V(CX - o, CY - d / 2, Y1, d),
                             _V(CX + o, CY - d / 2, Y1, d),
                             _H(CY, CX - o - d / 2, X1, d)],
    0x255A: lambda P, d, o: [_corner(P, +1, +1)],
    0x255B: lambda P, d, o: [_V(CX, CY - o - d / 2, Y1, d),
                             _H(CY + o, X0, CX + d / 2, d),
                             _H(CY - o, X0, CX + d / 2, d)],
    0x255C: lambda P, d, o: [_V(CX - o, CY - d / 2, Y1, d),
                             _V(CX + o, CY - d / 2, Y1, d),
                             _H(CY, X0, CX + o + d / 2, d)],
    0x255D: lambda P, d, o: [_corner(P, -1, +1)],
    0x255E: lambda P, d, o: [_V(CX, Y0, Y1, d),
                             _H(CY + o, CX - d / 2, X1, d),
                             _H(CY - o, CX - d / 2, X1, d)],
    0x255F: lambda P, d, o: [_V(CX - o, Y0, Y1, d), _V(CX + o, Y0, Y1, d),
                             _H(CY, CX + o - d / 2, X1, d)],
    0x2560: lambda P, d, o: [_V(CX - o, Y0, Y1, d),
                             _V(CX + o, Y0, CY - o + d / 2, d),
                             _V(CX + o, CY + o - d / 2, Y1, d),
                             _H(CY + o, CX + o - d / 2, X1, d),
                             _H(CY - o, CX + o - d / 2, X1, d)],
    0x2561: lambda P, d, o: [_V(CX, Y0, Y1, d),
                             _H(CY + o, X0, CX + d / 2, d),
                             _H(CY - o, X0, CX + d / 2, d)],
    0x2562: lambda P, d, o: [_V(CX - o, Y0, Y1, d), _V(CX + o, Y0, Y1, d),
                             _H(CY, X0, CX - o + d / 2, d)],
    0x2563: lambda P, d, o: [_V(CX + o, Y0, Y1, d),
                             _V(CX - o, Y0, CY - o + d / 2, d),
                             _V(CX - o, CY + o - d / 2, Y1, d),
                             _H(CY + o, X0, CX - o + d / 2, d),
                             _H(CY - o, X0, CX - o + d / 2, d)],
    0x2564: lambda P, d, o: [_H(CY + o, X0, X1, d), _H(CY - o, X0, X1, d),
                             _V(CX, Y0, CY - o + d / 2, d)],
    0x2565: lambda P, d, o: [_H(CY, X0, X1, d),
                             _V(CX - o, Y0, CY + d / 2, d),
                             _V(CX + o, Y0, CY + d / 2, d)],
    0x2566: lambda P, d, o: [_H(CY + o, X0, X1, d),
                             _H(CY - o, X0, CX - o + d / 2, d),
                             _H(CY - o, CX + o - d / 2, X1, d),
                             _V(CX - o, Y0, CY - o + d / 2, d),
                             _V(CX + o, Y0, CY - o + d / 2, d)],
    0x2567: lambda P, d, o: [_H(CY + o, X0, X1, d), _H(CY - o, X0, X1, d),
                             _V(CX, CY + o - d / 2, Y1, d)],
    0x2568: lambda P, d, o: [_H(CY, X0, X1, d),
                             _V(CX - o, CY - d / 2, Y1, d),
                             _V(CX + o, CY - d / 2, Y1, d)],
    0x2569: lambda P, d, o: [_H(CY - o, X0, X1, d),
                             _H(CY + o, X0, CX - o + d / 2, d),
                             _H(CY + o, CX + o - d / 2, X1, d),
                             _V(CX - o, CY + o - d / 2, Y1, d),
                             _V(CX + o, CY + o - d / 2, Y1, d)],
    0x256A: lambda P, d, o: [_V(CX, Y0, Y1, d),
                             _H(CY + o, X0, X1, d), _H(CY - o, X0, X1, d)],
    0x256B: lambda P, d, o: [_V(CX - o, Y0, Y1, d), _V(CX + o, Y0, Y1, d),
                             _H(CY, X0, X1, d)],
    0x256C: lambda P, d, o: [_corner(P, +1, -1), _corner(P, -1, -1),
                             _corner(P, +1, +1), _corner(P, -1, +1)],
}
for cp, spec in _DOUBLES.items():
    _register(cp, _dbl(spec))


# --- arcs (256D-2570) and diagonals (2571-2573) ----------------------------

def _arc_corner(h, v):
    """Rounded corner: vertical arm toward v, horizontal arm toward h."""
    def fn(P, h=h, v=v):
        d, r = _ld(P), ARC_R
        c = _V(CX, *sorted((Y0 if v < 0 else Y1, CY + v * r)), d)
        c += _H(CY, *sorted((X0 if h < 0 else X1, CX + h * r)), d)
        # arc center sits diagonally inward at (CX+h*r, CY+v*r); the quarter
        # arc runs from the vertical arm's endpoint to the horizontal arm's
        a0 = 180 if h > 0 else 0
        a1 = 90 if v < 0 else (270 if h > 0 else -90)
        c += arc_band(CX + h * r, CY + v * r, r, r, d, a0, a1)
        return c
    return fn


_register(0x256D, _arc_corner(+1, -1))   # arc down and right
_register(0x256E, _arc_corner(-1, -1))   # arc down and left
_register(0x256F, _arc_corner(-1, +1))   # arc up and left
_register(0x2570, _arc_corner(+1, +1))   # arc up and right


def _diag_up(P):
    return stroke((X0, Y0), (X1, Y1), _ld(P))


def _diag_down(P):
    return stroke((X0, Y1), (X1, Y0), _ld(P))


_register(0x2571, _diag_up)
_register(0x2572, _diag_down)
_register(0x2573, lambda P: _diag_up(P) + _diag_down(P))


# --- block elements (2580-259F) --------------------------------------------

_EIGHTH = (Y1 - Y0) / 8     # 150
_COL = (X1 - X0) / 8        # 75

_register(0x2580, lambda P: rect(X0, CY, X1, Y1))
for k in range(1, 9):
    _register(0x2580 + k,
              lambda P, k=k: rect(X0, Y0, X1, Y0 + k * _EIGHTH))
for i, k in enumerate(range(7, 0, -1)):
    _register(0x2589 + i, lambda P, k=k: rect(X0, Y0, X0 + k * _COL, Y1))
_register(0x2590, lambda P: rect(CX, Y0, X1, Y1))
_register(0x2594, lambda P: rect(X0, Y1 - _EIGHTH, X1, Y1))
_register(0x2595, lambda P: rect(X1 - _COL, Y0, X1, Y1))


def _shade_light(P):
    c = []
    for r in range(12):
        for col in range(6):
            x = col * 100 + (15 if r % 2 else 60)
            y = Y0 + r * 100 + 25
            c += rect(x, y, x + 50, y + 50)
    return c


def _shade_medium(P):
    c = []
    for r in range(12):
        for col in range(6):
            if (r + col) % 2 == 0:
                x, y = col * 100, Y0 + r * 100
                c += rect(x, y, x + 100, y + 100)
    return c


def _shade_dark(P):
    c = rect(X0, Y0, X1, Y1)
    for r in range(12):
        for col in range(6):
            x = col * 100 + (15 if r % 2 else 60)
            y = Y0 + r * 100 + 25
            hole = rect(x, y, x + 50, y + 50)[0]
            c += [hole.oriented(clockwise=False)]
    return c


_register(0x2591, _shade_light)
_register(0x2592, _shade_medium)
_register(0x2593, _shade_dark)

_QUAD = {"ul": (X0, CY, CX, Y1), "ur": (CX, CY, X1, Y1),
         "ll": (X0, Y0, CX, CY), "lr": (CX, Y0, X1, CY)}


def _quads(*names):
    def fn(P, names=names):
        c = []
        for n in names:
            c += rect(*_QUAD[n])
        return c
    return fn


for cp, quads in {
        0x2596: ("ll",), 0x2597: ("lr",), 0x2598: ("ul",),
        0x2599: ("ul", "ll", "lr"), 0x259A: ("ul", "lr"),
        0x259B: ("ul", "ur", "ll"), 0x259C: ("ul", "ur", "lr"),
        0x259D: ("ur",), 0x259E: ("ur", "ll"),
        0x259F: ("ur", "ll", "lr")}.items():
    _register(cp, _quads(*quads))
