"""Render the specimen sheet shipped in the README.

This is two things at once: a presentable poster (header, character set,
disambiguation + ligature showcase, a syntax-highlighted code sample, a weight
comparison) and the dev-judging tool the build relies on (the 10-16pt size
waterfall at the bottom is rendered natively, so legibility is still judged at
the real target sizes — see CLAUDE.md).

The whole sheet renders at native resolution (no supersampling) so the
waterfall stays a faithful preview of small-size rasterization.

Run standalone to re-render the poster from the built TTFs without rebuilding
the fonts:

    .venv/bin/python -m cornea.specimen          # -> dist/specimen.png
"""

import os
import re

from PIL import Image, ImageDraw, ImageFont, features

# -- palette --------------------------------------------------------------
BG = (255, 255, 255)
INK = (38, 40, 46)
SUBINK = (92, 96, 104)
MUTE = (150, 154, 162)
RULE = (228, 230, 235)
PANEL_BG = (248, 249, 251)
PANEL_BORDER = (227, 229, 234)
GUTTER = (180, 184, 192)

# light editor theme for the code sample
SYNTAX = {
    "comment": (150, 154, 162),
    "keyword": (167, 41, 109),
    "type": (150, 100, 28),
    "call": (45, 110, 196),
    "string": (60, 140, 72),
    "number": (196, 104, 36),
    "op": (108, 114, 128),
    "ident": INK,
}

# -- specimen content -----------------------------------------------------
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
DIGSYM = "0123456789  ! @ # $ % ^ & * ( ) - = + [ ] { } ; : ' \" , . < > / ? \\ | ` ~"
DISAMBIG = "O0o   Il1|   rn/m   8B   5S$   2Z?   g9q   ;: .,   ''\"\"``"
LIGATURES = "->  <-  =>  ==  ===  !=  !==  >=  <=  &&  ||  ::  ..."
WEIGHT_LINE = "The quick brown fox jumps over 0 lazy Il1| dogs."

CODE = [
    "// CorneaDev Mono — built for long sessions at small sizes.",
    'import { readFile } from "node:fs/promises";',
    "",
    "interface Config {",
    "  retries: number;",
    "  timeout: number;",
    "  tags: string[];",
    "}",
    "",
    "async function loadConfig(path: string): Promise<Config> {",
    '  const raw = await readFile(path, "utf8");',
    "  const cfg = JSON.parse(raw) ?? {};",
    "  return {",
    "    retries: cfg.retries >= 0 ? cfg.retries : 3,",
    "    timeout: cfg.timeout || 5_000,",
    '    tags: [...cfg.tags, "default"],',
    "  };",
    "}",
    "",
    "const double = (xs: number[]) => xs.filter(x => x != null).map(x => x * 2);",
    "const ready = a === b && c !== d || count <= 0x1F;",
]

# pt -> px at 96 dpi (the real IDE target band; rendered natively below)
SIZES = [(10, 13), (11, 15), (12, 16), (13, 17), (14, 19), (16, 21)]
WCODE = "if (x != y && a >= b) { return list[i] -> 0x1F; }"
WALPHA = "ABCDEFG abcdefg 0123456789 — the quick brown fox"
WDIS = "O0o Il1| rn/m 8B 5S$ 2Z g9q ;: .,"

# -- code lexer (light syntax colouring for the sample) -------------------
KEYWORDS = {
    "import", "from", "export", "default", "interface", "type", "enum",
    "class", "extends", "implements", "async", "function", "const", "let",
    "var", "return", "await", "yield", "if", "else", "for", "while", "do",
    "switch", "case", "break", "continue", "new", "delete", "typeof",
    "instanceof", "in", "of", "this", "void", "null", "undefined", "true",
    "false", "number", "string", "boolean", "any", "unknown", "never",
}

_TOKEN_RE = re.compile(
    r"(?P<comment>//[^\n]*)"
    r"|(?P<string>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)"
    r"|(?P<number>0[xX][0-9a-fA-F]+|\d[\d_]*\.?\d*)"
    r"|(?P<ident>[A-Za-z_$][\w$]*)"
    r"|(?P<ws>\s+)"
    r"|(?P<op>[^\sA-Za-z0-9_$]+)"
)


def _lex(line):
    """Tokenize one line into (text, kind) pairs. Idents are refined into
    keyword/type/call so the sample reads like a real editor."""
    toks = [[m.group(), m.lastgroup] for m in _TOKEN_RE.finditer(line)]
    for i, (text, kind) in enumerate(toks):
        if kind != "ident":
            continue
        if text in KEYWORDS:
            toks[i][1] = "keyword"
        elif text[0].isupper():
            toks[i][1] = "type"
        else:
            j = i + 1
            while j < len(toks) and toks[j][1] == "ws":
                j += 1
            if j < len(toks) and toks[j][1] == "op" and toks[j][0].startswith("("):
                toks[i][1] = "call"
    return toks


def _style(kind):
    """(colour, weight-role) for a token kind. Comments lean on the italic and
    keywords on the bold, so the sample exercises all three faces inline."""
    if kind == "comment":
        return SYNTAX["comment"], "italic"
    if kind == "keyword":
        return SYNTAX["keyword"], "bold"
    if kind == "ws":
        return None, "regular"
    return SYNTAX.get(kind, INK), "regular"


def render(ttf_paths, out_path, width=1360):
    has_raqm = features.check("raqm")
    layout = ImageFont.Layout.RAQM if has_raqm else ImageFont.Layout.BASIC

    roles = {}
    for p in ttf_paths:
        b = os.path.basename(p).lower()
        role = "bold" if "bold" in b else "italic" if "italic" in b else "regular"
        roles[role] = p
    reg = roles.get("regular") or next(iter(roles.values()))
    faces = {"regular": reg, "bold": roles.get("bold", reg),
             "italic": roles.get("italic", reg)}

    cache = {}

    def F(role, px):
        key = (role, px)
        if key not in cache:
            cache[key] = ImageFont.truetype(faces[role], px, layout_engine=layout)
        return cache[key]

    M = 56
    img = Image.new("RGB", (width, 4600), BG)
    d = ImageDraw.Draw(img)
    y = M

    def spaced(x, yy, text, font, fill, extra=2):
        for ch in text:
            d.text((x, yy), ch, font=font, fill=fill)
            x += font.getlength(ch) + extra
        return x

    def section(title):
        nonlocal y
        y += 22
        f = F("bold", 14)
        end = spaced(M, y, title.upper(), f, MUTE, extra=2)
        d.line((end + 16, y + 8, width - M, y + 8), fill=RULE, width=1)
        y += 30

    def row(text, px, role="regular", fill=INK, lead=1.35):
        nonlocal y
        d.text((M, y), text, font=F(role, px), fill=fill)
        y += int(px * lead)

    # -- header -----------------------------------------------------------
    d.text((M, y), "CorneaDev Mono", font=F("bold", 60), fill=INK)
    y += 76
    d.text((M, y),
           "A monospace typeface engineered for legibility at small sizes.",
           font=F("regular", 22), fill=SUBINK)
    y += 36
    meta = ("Regular · Bold · Italic     ASCII · Latin-1 · Greek · "
            "Box-drawing · Powerline     600/1000 advance, strictly monospaced")
    d.text((M, y), meta, font=F("regular", 14), fill=MUTE)
    y += 28
    d.line((M, y, width - M, y), fill=RULE, width=1)
    y += 4

    # -- character set ----------------------------------------------------
    section("Character set")
    row(UPPER, 30, lead=1.4)
    row(LOWER, 30, lead=1.4)
    row(DIGSYM, 24, lead=1.55)

    # -- disambiguation ---------------------------------------------------
    section("Disambiguation")
    row(DISAMBIG, 36, lead=1.2)
    d.text((M, y), "look-alikes shaped per-glyph so they never trade places",
           font=F("italic", 14), fill=MUTE)
    y += 24

    # -- ligatures --------------------------------------------------------
    section("Ligatures")
    row(LIGATURES, 34, lead=1.3)

    # -- code sample ------------------------------------------------------
    section("Code")
    cpx = 19
    lh = int(cpx * 1.6)
    pad = 18
    gutter = int(F("regular", cpx).getlength("00")) + 26
    panel_h = len(CODE) * lh + 2 * pad
    d.rounded_rectangle((M, y, width - M, y + panel_h), radius=10,
                        fill=PANEL_BG, outline=PANEL_BORDER, width=1)
    gx = M + pad + gutter
    d.line((gx - 12, y + pad - 2, gx - 12, y + panel_h - pad + 2),
           fill=PANEL_BORDER, width=1)
    cy = y + pad
    nf = F("regular", cpx)
    for i, line in enumerate(CODE):
        num = str(i + 1)
        d.text((gx - 20 - nf.getlength(num), cy), num, font=nf, fill=GUTTER)
        x = gx + 4
        for text, kind in _lex(line):
            color, role = _style(kind)
            f = F(role, cpx)
            if color is not None:
                d.text((x, cy), text, font=f, fill=color)
            x += f.getlength(text)
        cy += lh
    y += panel_h

    # -- weights ----------------------------------------------------------
    section("Weights")
    for role, label in (("regular", "Regular 400"), ("bold", "Bold 700"),
                        ("italic", "Italic")):
        d.text((M, y + 8), label, font=F("regular", 13), fill=MUTE)
        d.text((M + 150, y), WEIGHT_LINE, font=F(role, 26), fill=INK)
        y += 44

    # -- size waterfall (the dev-judging target; rendered natively) -------
    section("Sizes · 10–16 pt waterfall — the actual rendering target")
    for pt, px in SIZES:
        d.text((M, y), f"{pt} pt", font=F("regular", 12), fill=MUTE)
        x = M + 56
        for line in (WCODE, WALPHA, WDIS):
            d.text((x, y), line, font=F("regular", px), fill=INK)
            y += int(px * 1.55)
        y += 10

    # -- footer -----------------------------------------------------------
    y += 6
    d.line((M, y, width - M, y), fill=RULE, width=1)
    y += 14
    d.text((M, y),
           "Generated by build_font.py — judge legibility in the size "
           "waterfall above, at the real target sizes.",
           font=F("italic", 13), fill=MUTE)
    y += 24

    final = img.crop((0, 0, width, y + M))
    final.save(out_path)
    return out_path, has_raqm


if __name__ == "__main__":
    import glob

    order = {"Regular": 0, "Bold": 1, "Italic": 2}
    paths = sorted(
        glob.glob("dist/CorneaDevMono-*.ttf"),
        key=lambda p: order.get(os.path.basename(p).split("-")[-1][:-4], 9),
    )
    if not paths:
        raise SystemExit("no dist/CorneaDevMono-*.ttf found; run build_font.py first")
    out, raqm = render(paths, "dist/specimen.png")
    note = "" if raqm else "  (no raqm: ligatures not shaped)"
    print(f"specimen {out}{note}")
