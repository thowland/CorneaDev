"""Core programming ligatures.

Each ligature is a single unencoded glyph whose advance is an exact multiple
of the 600-unit cell, substituted via GSUB (liga + calt), so column alignment
in editors is preserved. LIGATURES maps glyph name -> (n_cells, builder,
component glyph names for the FEA rule)."""

from .geometry import stroke, dot
from .glyphs import hbar, vstem

LIGATURES = {}


def liga(name, cells, components):
    def deco(fn):
        LIGATURES[name] = (cells, fn, components)
        return fn
    return deco


def _chevron_right(P, tip_x, mid_y, size):
    return (stroke((tip_x - size, mid_y + size), (tip_x, mid_y), P.ds)
            + stroke((tip_x, mid_y), (tip_x - size, mid_y - size), P.ds))


def _chevron_left(P, tip_x, mid_y, size):
    return (stroke((tip_x + size, mid_y + size), (tip_x, mid_y), P.ds)
            + stroke((tip_x, mid_y), (tip_x + size, mid_y - size), P.ds))


@liga("arrowright.liga", 2, ["hyphen", "greater"])
def lig_arrow_r(P):
    c = hbar(P, 330, 110, 1010, P.thin + 8)
    c += _chevron_right(P, 1085, 330, 250)
    return c


@liga("arrowleft.liga", 2, ["less", "hyphen"])
def lig_arrow_l(P):
    c = hbar(P, 330, 190, 1090, P.thin + 8)
    c += _chevron_left(P, 115, 330, 250)
    return c


@liga("darrowright.liga", 2, ["equal", "greater"])
def lig_darrow_r(P):
    c = hbar(P, 240, 100, 940, P.thin + 6)
    c += hbar(P, 420, 100, 940, P.thin + 6)
    c += _chevron_right(P, 1090, 330, 265)
    return c


@liga("eqeq.liga", 2, ["equal", "equal"])
def lig_eqeq(P):
    return (hbar(P, 240, 130, 1070, P.thin + 6)
            + hbar(P, 420, 130, 1070, P.thin + 6))


@liga("eqeqeq.liga", 3, ["equal", "equal", "equal"])
def lig_eqeqeq(P):
    return (hbar(P, 180, 200, 1600, P.thin + 6)
            + hbar(P, 330, 200, 1600, P.thin + 6)
            + hbar(P, 480, 200, 1600, P.thin + 6))


@liga("noteq.liga", 2, ["exclam", "equal"])
def lig_noteq(P):
    c = lig_eqeq(P)
    c += stroke((470, 60), (730, 600), P.ds)
    return c


@liga("noteqeq.liga", 3, ["exclam", "equal", "equal"])
def lig_noteqeq(P):
    c = lig_eqeqeq(P)
    c += stroke((770, 40), (1030, 620), P.ds)
    return c


@liga("lesseq.liga", 2, ["less", "equal"])
def lig_lesseq(P):
    c = _chevron_left(P, 330, 400, 290)
    c += hbar(P, 95, 340, 870, P.thin + 6)
    return c


@liga("greatereq.liga", 2, ["greater", "equal"])
def lig_greatereq(P):
    c = _chevron_right(P, 870, 400, 290)
    c += hbar(P, 95, 330, 860, P.thin + 6)
    return c


@liga("andand.liga", 2, ["ampersand", "ampersand"])
def lig_andand(P):
    from .glyphs import g_ampersand
    from .geometry import translate_all
    a = g_ampersand(P)
    return translate_all(a, 40, 0) + translate_all(a, 560, 0)


@liga("barbar.liga", 2, ["bar", "bar"])
def lig_barbar(P):
    return (vstem(P, 480, -150, 770, P.stem - 6)
            + vstem(P, 720, -150, 770, P.stem - 6))


@liga("coloncolon.liga", 2, ["colon", "colon"])
def lig_coloncolon(P):
    r = P.dotr + 8
    return (dot(480, 66, r) + dot(480, 440, r)
            + dot(720, 66, r) + dot(720, 440, r))


@liga("ellipsis.liga", 3, ["period", "period", "period"])
def lig_ellipsis(P):
    r = P.dotr + 8
    return dot(450, 66, r) + dot(900, 66, r) + dot(1350, 66, r)


def feature_text():
    """Generate the FEA source for liga/calt. Longest sequences first."""
    rules = sorted(LIGATURES.items(), key=lambda kv: -kv[1][0])
    subs = "\n".join(
        f"    sub {' '.join(comps)} by {name};"
        for name, (_cells, _fn, comps) in rules)
    return (
        "lookup progligs {\n" + subs + "\n} progligs;\n\n"
        "feature liga {\n    lookup progligs;\n} liga;\n\n"
        "feature calt {\n    lookup progligs;\n} calt;\n"
    )
