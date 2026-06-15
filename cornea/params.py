"""Per-weight design parameters. All glyph builders read from these, so a
new weight is just a new parameter set."""

from types import SimpleNamespace

# Shared vertical scheme (font units, UPM = 1000)
UPM = 1000
ADV = 600          # fixed advance for every encoded glyph
CAP = 720          # cap height (digits share this)
XH = 540           # x-height -- deliberately tall for small-size legibility
ASC = 740          # b/d/h/k/l ascender top
DESC = -240        # p/q/g/y descender bottom
OT = 12            # overshoot for round shapes

# Vertical metrics for the font tables (1.2em default line)
TYPO_ASC = 760
TYPO_DESC = -240
TYPO_GAP = 200
HHEA_ASC = 950
HHEA_DESC = -250


def weight(name):
    common = dict(
        upm=UPM, adv=ADV, cap=CAP, xh=XH, asc=ASC, desc=DESC, ot=OT,
        mid=ADV // 2,
        left=70, right=530,      # default flat-sided glyph extents
        # shared lowercase metrics: every lowercase letter aligns to these
        lc_stem_l=120,           # left stem center (b h k n p r ...)
        lc_stem_r=480,           # right stem center (d q u a g ...)
        lc_rx=220,               # OUTER x-radius of round bowls (o b d e ...)
        # italic defaults (upright weights leave these untouched)
        slant=0,                 # degrees; >0 leans the tops right
        slant_pivot=340,         # shear pivot y (centres the slanted ink in the
                                 # cell so caps don't lean past the right wall)
        italic_bit=False,
    )
    if name == "regular":
        w = dict(stem=84, thin=68, ds=80, dotr=58,
                 weight_class=400, subfamily="Regular", bold_bit=False)
    elif name == "bold":
        w = dict(stem=130, thin=102, ds=122, dotr=72,
                 weight_class=700, subfamily="Bold", bold_bit=True)
    elif name == "italic":
        # true italic: regular stroke widths + a slope, with single-story a
        # and a cursive f supplied as glyph overrides (see ITALIC_BUILDERS).
        w = dict(stem=84, thin=68, ds=80, dotr=58,
                 weight_class=400, subfamily="Italic", bold_bit=False,
                 slant=10, italic_bit=True)
    else:
        raise ValueError(f"unknown weight: {name}")
    return SimpleNamespace(**{**common, **w})


WEIGHTS = ["regular", "bold", "italic"]
