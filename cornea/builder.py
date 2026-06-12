"""Assemble TTF files from the parametric glyph definitions."""

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib.tables.O_S_2f_2 import Panose

from . import params
from .glyphs import BUILDERS
from .ligatures import LIGATURES, feature_text


def _compile_glyph(contours):
    pen = TTGlyphPen(None)
    quad = Cu2QuPen(pen, max_err=1.0)
    for c in contours:
        c.draw(quad)
    return pen.glyph()


def build_weight(P, family, version, enable_ligatures=True):
    glyph_order = [".notdef", "space"]
    cmap = {}
    glyphs = {}
    advances = {}

    for name, (cp, fn) in BUILDERS.items():
        if name not in glyph_order:
            glyph_order.append(name)
        if cp is not None:
            cmap[cp] = name
        glyphs[name] = _compile_glyph(fn(P))
        advances[name] = P.adv

    if enable_ligatures:
        for name, (cells, fn, _comps) in LIGATURES.items():
            glyph_order.append(name)
            glyphs[name] = _compile_glyph(fn(P))
            advances[name] = P.adv * cells

    fb = FontBuilder(params.UPM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)

    glyf = fb.font["glyf"]
    metrics = {}
    for name in glyph_order:
        g = glyf[name]
        g.recalcBounds(glyf)
        lsb = g.xMin if g.numberOfContours else 0
        metrics[name] = (advances[name], lsb)
    fb.setupHorizontalMetrics(metrics)

    fb.setupHorizontalHeader(ascent=params.HHEA_ASC, descent=params.HHEA_DESC,
                             lineGap=0)

    style = P.subfamily
    ps_family = family.replace(" ", "")
    fb.setupNameTable({
        "familyName": family,
        "styleName": style,
        "uniqueFontIdentifier": f"{version};{ps_family}-{style}",
        "fullName": f"{family} {style}",
        "psName": f"{ps_family}-{style}",
        "version": f"Version {version}",
    })

    panose = Panose()
    panose.bFamilyType = 2          # Latin text
    panose.bSerifStyle = 11         # normal sans
    panose.bWeight = 8 if P.bold_bit else 5
    panose.bProportion = 9          # monospaced -- required for detection
    panose.bContrast = 2
    panose.bStrokeVariation = 2
    panose.bArmStyle = 3
    panose.bLetterForm = 2
    panose.bMidline = 2
    panose.bXHeight = 4

    fs_selection = 0x20 if P.bold_bit else 0x40   # BOLD / REGULAR
    fb.setupOS2(
        sTypoAscender=params.TYPO_ASC, sTypoDescender=params.TYPO_DESC,
        sTypoLineGap=params.TYPO_GAP,
        usWinAscent=params.HHEA_ASC, usWinDescent=-params.HHEA_DESC,
        sxHeight=params.XH, sCapHeight=params.CAP,
        usWeightClass=P.weight_class, usWidthClass=5,
        xAvgCharWidth=P.adv, fsSelection=fs_selection,
        panose=panose, achVendID="WDOG",
        ulCodePageRange1=0x00000001,   # Latin 1
    )
    fb.setupPost(isFixedPitch=1, underlinePosition=-120,
                 underlineThickness=70)

    fb.font["head"].macStyle = 0x01 if P.bold_bit else 0x00

    if enable_ligatures:
        fb.addOpenTypeFeatures(feature_text())

    return fb.font


def build(family, weights, version, enable_ligatures, out_dir):
    import os
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for wname in weights:
        P = params.weight(wname)
        font = build_weight(P, family, version, enable_ligatures)
        fname = f"{family.replace(' ', '')}-{P.subfamily}.ttf"
        path = os.path.join(out_dir, fname)
        font.save(path)
        paths.append(path)
    return paths
