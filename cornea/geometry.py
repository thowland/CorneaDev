"""Vector geometry primitives for parametric glyph construction.

Coordinates are font units, y-up. Shapes are built as filled cubic-Bezier
contours; overlapping positive contours merge under nonzero winding, so
glyphs can be composed from simple primitives without boolean unions.
Convention (TrueType): positive/filled contours wind clockwise (in y-up),
counters wind counterclockwise.
"""

import math

KAPPA = 0.5522847498307936


class Path:
    """One closed contour: [('move',p),('line',p),('curve',c1,c2,p),...,('close',)]"""

    def __init__(self):
        self.segments = []

    def move_to(self, p):
        self.segments.append(("move", tuple(p)))
        return self

    def line_to(self, p):
        self.segments.append(("line", tuple(p)))
        return self

    def curve_to(self, c1, c2, p):
        self.segments.append(("curve", tuple(c1), tuple(c2), tuple(p)))
        return self

    def close(self):
        self.segments.append(("close",))
        return self

    # --- analysis -------------------------------------------------------

    def sample_points(self, n=6):
        """Approximate the contour as a polygon for area/orientation checks."""
        pts = []
        cur = None
        for seg in self.segments:
            if seg[0] == "move":
                cur = seg[1]
                pts.append(cur)
            elif seg[0] == "line":
                cur = seg[1]
                pts.append(cur)
            elif seg[0] == "curve":
                c1, c2, p = seg[1], seg[2], seg[3]
                for i in range(1, n + 1):
                    t = i / n
                    mt = 1 - t
                    x = (mt**3 * cur[0] + 3 * mt**2 * t * c1[0]
                         + 3 * mt * t**2 * c2[0] + t**3 * p[0])
                    y = (mt**3 * cur[1] + 3 * mt**2 * t * c1[1]
                         + 3 * mt * t**2 * c2[1] + t**3 * p[1])
                    pts.append((x, y))
                cur = p
        return pts

    def signed_area(self):
        pts = self.sample_points()
        a = 0.0
        for i in range(len(pts)):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % len(pts)]
            a += x0 * y1 - x1 * y0
        return a / 2.0  # positive = counterclockwise (y-up)

    def reversed_(self):
        """Return this contour traversed in the opposite direction."""
        on_points = []
        segs = []
        for seg in self.segments:
            if seg[0] in ("move", "line"):
                on_points.append(seg[1])
                segs.append(seg)
            elif seg[0] == "curve":
                on_points.append(seg[3])
                segs.append(seg)
        out = Path()
        out.move_to(on_points[-1])
        for i in range(len(segs) - 1, 0, -1):
            seg = segs[i]
            prev_pt = on_points[i - 1]
            if seg[0] == "line":
                out.line_to(prev_pt)
            else:
                out.curve_to(seg[2], seg[1], prev_pt)
        out.close()
        return out

    def oriented(self, clockwise=True):
        ccw = self.signed_area() > 0
        if ccw == clockwise:
            return self.reversed_()
        return self

    def translated(self, dx, dy):
        out = Path()
        for seg in self.segments:
            if seg[0] == "close":
                out.segments.append(seg)
            else:
                out.segments.append(
                    (seg[0],) + tuple((p[0] + dx, p[1] + dy) for p in seg[1:]))
        return out

    def rotated180(self, cx, cy):
        out = Path()
        for seg in self.segments:
            if seg[0] == "close":
                out.segments.append(seg)
            else:
                out.segments.append(
                    (seg[0],) + tuple((2 * cx - p[0], 2 * cy - p[1])
                                      for p in seg[1:]))
        return out

    def draw(self, pen):
        for seg in self.segments:
            if seg[0] == "move":
                pen.moveTo(seg[1])
            elif seg[0] == "line":
                pen.lineTo(seg[1])
            elif seg[0] == "curve":
                pen.curveTo(seg[1], seg[2], seg[3])
            else:
                pen.closePath()


# --- primitives (each returns a list of Path contours) -------------------

def poly(*pts):
    p = Path()
    p.move_to(pts[0])
    for pt in pts[1:]:
        p.line_to(pt)
    p.close()
    return [p.oriented(clockwise=True)]


def rect(x0, y0, x1, y1):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    return poly((x0, y0), (x0, y1), (x1, y1), (x1, y0))


def stroke(p0, p1, w):
    """A straight stroke of width w from p0 to p1 (flat caps)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    if ln == 0:
        return []
    nx, ny = -dy / ln * w / 2, dx / ln * w / 2
    return poly((p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny),
                (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny))


def _arc_segments(cx, cy, rx, ry, a0, a1):
    """Cubic segments along an ellipse from angle a0 to a1 (degrees).
    Direction follows the sign of (a1 - a0). Returns (start_pt, segs) where
    segs are ('curve', c1, c2, p) tuples."""
    a0r, a1r = math.radians(a0), math.radians(a1)
    total = a1r - a0r
    n = max(1, int(math.ceil(abs(total) / (math.pi / 2 - 1e-9))))
    step = total / n
    k = 4.0 / 3.0 * math.tan(step / 4.0)

    def pt(a):
        return (cx + rx * math.cos(a), cy + ry * math.sin(a))

    def tan_dir(a):
        return (-rx * math.sin(a), ry * math.cos(a))

    segs = []
    a = a0r
    start = pt(a)
    for _ in range(n):
        b = a + step
        p0, p1 = pt(a), pt(b)
        d0, d1 = tan_dir(a), tan_dir(b)
        c1 = (p0[0] + k * d0[0], p0[1] + k * d0[1])
        c2 = (p1[0] - k * d1[0], p1[1] - k * d1[1])
        segs.append(("curve", c1, c2, p1))
        a = b
    return start, segs


def ellipse(cx, cy, rx, ry, clockwise=True):
    start, segs = _arc_segments(cx, cy, rx, ry, 0, 360)
    p = Path()
    p.move_to(start)
    p.segments.extend(segs)
    p.close()
    return [p.oriented(clockwise=clockwise)]


def dot(cx, cy, r):
    return ellipse(cx, cy, r, r)


def ring(cx, cy, rx, ry, w):
    """Elliptical ring; rx/ry are OUTER radii, stroke thickness w."""
    outer = ellipse(cx, cy, rx, ry, clockwise=True)
    inner = ellipse(cx, cy, rx - w, ry - w, clockwise=False)
    return outer + inner


def arc_band(cx, cy, rx, ry, w, a0, a1):
    """Annular arc (a curved stroke) with flat ends. rx/ry are CENTERLINE
    radii; w is stroke thickness. Angles in degrees; direction = sign of
    (a1 - a0)."""
    ro_x, ro_y = rx + w / 2.0, ry + w / 2.0
    ri_x, ri_y = rx - w / 2.0, ry - w / 2.0
    start_o, segs_o = _arc_segments(cx, cy, ro_x, ro_y, a0, a1)
    start_i, segs_i = _arc_segments(cx, cy, ri_x, ri_y, a1, a0)
    p = Path()
    p.move_to(start_o)
    p.segments.extend(segs_o)
    p.line_to(start_i)
    p.segments.extend(segs_i)
    p.close()
    return [p.oriented(clockwise=True)]


def translate_all(contours, dx, dy):
    return [c.translated(dx, dy) for c in contours]


def rotate180_all(contours, cx, cy):
    return [c.rotated180(cx, cy) for c in contours]
