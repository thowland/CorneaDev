"""Assemble TTF files from the parametric glyph definitions."""

import math

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib.tables.O_S_2f_2 import Panose

from . import params
from .geometry import shear_all
from .glyphs import BUILDERS, ITALIC_BUILDERS
from .ligatures import LIGATURES, feature_text

# Full-cell glyphs (box-drawing/blocks, Powerline) must stay axis-aligned so
# adjacent cells connect -- they are never slanted, even in the italic.
_NO_SLANT_RANGES = [(0x2500, 0x259F), (0xE0A0, 0xE0B3)]

# Licensing, embedded in every build's name table (see setupNameTable below).
# The Reserved Font Name clause documents the original "Cornea Mono"; a fork
# rebuilt under --family must rename and update this line.
COPYRIGHT = ('Copyright 2026 Tim Howland (th@wdogsystems.com), '
             'with Reserved Font Name "Cornea Mono".')
DESIGNER = "Tim Howland"
LICENSE_DESC = ("This Font Software is licensed under the SIL Open Font "
                "License, Version 1.1. This license is available with a FAQ "
                "at https://openfontlicense.org")
LICENSE_URL = "https://openfontlicense.org"


def _no_slant(cp):
    return cp is not None and any(a <= cp <= b for a, b in _NO_SLANT_RANGES)

# Extension ranges register themselves into BUILDERS on import.
from . import latin1, boxdraw, powerline, greek  # noqa: F401

EXTRA_CMAP = {}
EXTRA_CMAP.update(latin1.EXTRA_CMAP)
EXTRA_CMAP.update(greek.EXTRA_CMAP)


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

    slant = getattr(P, "slant", 0)
    k = math.tan(math.radians(slant)) if slant else 0

    def shaped(name, cp, fn):
        builder = ITALIC_BUILDERS.get(name, fn) if P.italic_bit else fn
        contours = builder(P)
        if k and not _no_slant(cp):
            contours = shear_all(contours, k, P.slant_pivot)
        return _compile_glyph(contours)

    for name, (cp, fn) in BUILDERS.items():
        if name not in glyph_order:
            glyph_order.append(name)
        if cp is not None:
            cmap[cp] = name
        glyphs[name] = shaped(name, cp, fn)
        advances[name] = P.adv

    for cp, target in EXTRA_CMAP.items():
        cmap[cp] = target

    if enable_ligatures:
        for name, (cells, fn, _comps) in LIGATURES.items():
            glyph_order.append(name)
            glyphs[name] = shaped(name, None, fn)
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
        "copyright": COPYRIGHT,
        "familyName": family,
        "styleName": style,
        "uniqueFontIdentifier": f"{version};{ps_family}-{style}",
        "fullName": f"{family} {style}",
        "psName": f"{ps_family}-{style}",
        "version": f"Version {version}",
        "manufacturer": DESIGNER,
        "designer": DESIGNER,
        "licenseDescription": LICENSE_DESC,
        "licenseInfoURL": LICENSE_URL,
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

    fs_selection = 0
    if P.bold_bit:
        fs_selection |= 0x20          # BOLD
    if P.italic_bit:
        fs_selection |= 0x01          # ITALIC
    if not fs_selection:
        fs_selection = 0x40           # REGULAR
    fb.setupOS2(
        sTypoAscender=params.TYPO_ASC, sTypoDescender=params.TYPO_DESC,
        sTypoLineGap=params.TYPO_GAP,
        usWinAscent=params.HHEA_ASC, usWinDescent=-params.HHEA_DESC,
        sxHeight=params.XH, sCapHeight=params.CAP,
        usWeightClass=P.weight_class, usWidthClass=5,
        xAvgCharWidth=P.adv, fsSelection=fs_selection,
        fsType=0,                      # installable embedding (OFL-friendly)
        panose=panose, achVendID="WDOG",
        ulCodePageRange1=0x00000001,   # Latin 1
        # Basic Latin, Latin-1, Greek, General Punctuation
        ulUnicodeRange1=0x80000083,
        # Arrows, Math Operators, Box Drawing, Block Elements, PUA
        ulUnicodeRange2=0x10001860,
    )
    fb.setupPost(isFixedPitch=1, underlinePosition=-120,
                 underlineThickness=70)
    # italicAngle is negative for a right-leaning slope; ttfautohint and
    # layout engines read it to position underline/strikeout and cursors.
    fb.font["post"].italicAngle = -float(P.slant)

    mac_style = 0
    if P.bold_bit:
        mac_style |= 0x01
    if P.italic_bit:
        mac_style |= 0x02
    fb.font["head"].macStyle = mac_style

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
