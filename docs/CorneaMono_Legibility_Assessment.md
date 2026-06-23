# CorneaMono

**Legibility Assessment & Design Rationale**

*A research-grounded evaluation of design decisions for a monospace typeface intended to support software developers experiencing presbyopia.*

*Status: Working assessment · For design review and onboarding · Companion to the plain-language guide*

## 1. Purpose and scope

This document records the design intent behind CorneaMono and the published evidence that supports it. It has two jobs: to guide future design and engineering work against a shared rationale, and to answer questions about why specific letterforms look the way they do. It is deliberately candid about where the evidence is strong, where it rests on professional consensus, and where reasonable designers could still disagree.

The scope is the typeface's legibility-relevant decisions — letterform shape, character disambiguation, weight, spacing, and style structure. It does not cover hinting, OpenType engineering, or licensing, which are tracked separately.

## 2. Framing the target condition

Presbyopia is not low vision, and the distinction matters for which research applies. Presbyopia is the age-related loss of the eye's ability to focus at near distance: the lens stiffens, accommodation declines, and close work becomes blurry at a normal reading distance. It typically begins around age 40 and progresses into the mid-60s. It does not remove parts of the visual field the way macular degeneration or glaucoma do.

The practical consequence is that a presbyopic developer's retinal image of the screen is degraded by blur, not cropped or obscured. The correct evidence base, therefore, is the research on legibility under degraded imaging — blur, crowding, and distance reading — rather than the disease-specific low-vision literature. These bodies of work overlap heavily, because they are all asking the same underlying question: which letter shapes survive a poor-quality image? Where this assessment cites low-vision studies, it does so because their mechanism (a degraded image) transfers to presbyopia, not because presbyopia is a form of low vision.

> **Working principle** Design for a slightly out-of-focus image. Every decision below is justified by how well a letterform holds its identity when blur and crowding erode its finer detail — which is exactly the condition CorneaMono's readers face when working at small sizes without optimal correction.

## 3. Assessment summary

The table below maps each major design decision to its primary evidence basis and a confidence rating. Confidence reflects the strength and directness of the supporting evidence, not the strength of the designers' conviction. Detailed rationale follows in Section 4.

| **Design decision** | **Primary evidence basis** | **Confidence** |
|---|---|---|
| **Monospace foundation** | Coding-domain requirement (alignment, disambiguation); partial-sight guidance favouring wide, regular spacing. | **Moderate** |
| **Disambiguation of confusable characters (0/O, 1/l/I, rn/m, 5/S, 8/B)** | Established coding-font convention; Atkinson Hyperlegible per-glyph differentiation; slashed-zero literature. | **Strong** |
| **Open apertures on a, c, e, r, s** | Beier & Oderkerk (2022); Tinker (1963); blur-feature studies. Per-letter caveat for c. | **Strong** |
| **Selective serifs inside a sans-serif design** | Serif × stroke-contrast low-vision study (2022); Beier & Dyson distance reading; Atkinson precedent. | **Moderate** |
| **Mid-range stroke weight (avoiding very light or very heavy)** | Luciole design criteria; stroke-width reading studies (Bernard et al.; Sheedy et al.). | **Moderate** |
| **Large x-height and generous spacing** | Distance-reading reviews (Beier); crowding literature. | **Strong** |
| **Italic treated as the weakest legibility channel** | Inclusive-design guidance (Vision Australia); broad low-vision consensus. | **Moderate** |

**Confidence key.**  **Strong** = supported by controlled experiments directly on the relevant feature.  **Moderate** = supported by targeted studies plus strong professional consensus, with some transfer assumptions.  **Emerging / Contested** = mixed or indirect evidence; decision rests partly on judgement.

## 4. Design decisions and supporting evidence

### 4.1  Monospace foundation

A monospace grid is a baseline requirement for a coding typeface: fixed advance widths keep code aligned and make indentation, columns, and diffs legible. Beyond that functional need, the even, generous spacing of a monospace font is mildly beneficial for degraded reading. Arditi's guidance for readers with partial sight recommends wide spacing where possible and notes that monospaced fonts can be more legible than proportional ones for this audience. CorneaMono therefore inherits an accessibility advantage from a constraint it already had to satisfy.

### 4.2  Disambiguation of confusable characters

The specimen's test string — O 0 o, 1 l I and the pipe, i ! j, 5 S $, 8 B &, 2 Z ? 7, the rn/m collision, g 9 q — is the canonical inventory of characters that cause real bugs when confused. This is the most settled area of coding-font design. The reference implementation is Atkinson Hyperlegible, which differentiates commonly misread pairs (capital I from lowercase l from the digit 1; B from 8) through deliberate per-glyph shaping rather than uniform letterforms.

The zero deserves a specific, recorded decision. Under blur, an undifferentiated 0 and O become identical, and context does not always rescue the reader (passwords, hashes, identifiers). The literature supports a slash, an interior dot, or a distinctly different shape. A known trade-off: a dotted zero can be mistaken for an 8 on a low-resolution display — and blur effectively turns any display into a low-resolution one. CorneaMono should favour a slashed zero as the default, optionally exposing a dotted variant through the standard OpenType 'zero' feature so users in scripts where the slash collides with Ø can opt out.

### 4.3  Open apertures (the “funky” a and e)

The lowercase a and e read as unusual because their apertures — the openings into the letters' interior counters — are held open rather than curled closed. This is the single best-supported decision in the typeface, and it should be protected from well-meaning attempts to make the letters look more conventional.

Beier and Oderkerk (2022) tested a, c, e, r, s, t, and f at three aperture sizes and found that closed apertures measurably impaired letter recognition relative to open ones — an effect that was strongest when letters were flanked by neighbours, i.e. under crowding. Dense lines of code are a crowded environment, and blur amplifies crowding, so the condition CorneaMono targets is precisely where the open-aperture advantage is largest. The proposed mechanism is that larger apertures enlarge the interior counter, sharpen individual-letter recognition, and reduce “feature migration” between adjacent letters. The principle is old — Tinker observed in 1963 that more enclosed white space tends to raise legibility — and blur-specific work reinforces it: when letters are blurred, readers identify them more accurately when the stroke endings that define an open aperture remain visible.

> **Honest caveat to carry into review** The aperture benefit is not uniform across every letter. Subsequent analysis confirmed the advantage for the lowercase e, but did not confirm it for the larger opening of the lowercase c. Treat the open e as settled and the open c as a defensible judgement call rather than a mandate — someone will ask, and this is the accurate answer.

### 4.4  Selective serifs within a sans-serif design

CorneaMono is mostly sans-serif with serifs added only to specific glyphs. This is a more defensible position than a blanket “serif” or “sans” choice, because the blunt question of serif-versus-sans has no reliable answer in the legibility literature — reviews repeatedly find no dependable difference on screen or paper. The selective approach sidesteps that stalemate and targets the cases where serifs demonstrably help.

Two findings support the decision. First, a 2022 study of low-acuity readers isolated stroke contrast and serifs and found that when stroke width is uniform — as it is in a monospace coding font — adding serifs produced significantly better word identification than omitting them. CorneaMono's low stroke contrast places it in exactly the cell where serifs helped. Second, Beier and Dyson's distance-reading work found that serifs at the vertical extremes of letters improve legibility under degraded viewing. Together these justify placing serifs precisely where confusion or instability arises — the capital I, the foot of the lowercase l, terminals that need anchoring — and nowhere else. Atkinson Hyperlegible follows the same logic explicitly, adding selective serifs to a sans-serif design (a serifed capital I, a spur on the lowercase i, a curved terminal on the lowercase l).

### 4.5  Stroke weight and contrast

CorneaMono uses a mid-range weight. The evidence cautions against both extremes: stroke thickness beyond a moderate value does not improve reading, and excessively bold strokes slow it down by closing counters and intensifying crowding — the opposite of the aperture strategy in 4.3. The design-review question is therefore not whether the Regular weight is correct (it appears well-judged) but whether the Bold remains a legibility tool or tips into a weight heavy enough to undermine the open-counter benefit.

### 4.6  x-height and spacing

Large x-height combined with open counters and generous inter-letter spacing is the consistent prescription from distance- and blur-reading research. In a coding context the user controls the nominal point size in their editor, so the lever that actually buys blur tolerance is the x-height — the proportion of the em that the lowercase letters occupy — rather than the point size itself. CorneaMono's large x-height is doing more accessibility work than the size control most users will reach for first.

### 4.7  The italic style

The italic is the weakest channel for this audience and should be treated as such. Inclusive-design guidance is consistent that slanted text degrades legibility under exactly the conditions CorneaMono targets, and recommends weight rather than slant for emphasis. A coding font cannot abandon its italic — editor themes use it for comments, keywords, and types — but the project can limit how much semantic load the slant carries: keep the italic angle modest, reserve true cursive forms for letters where they aid recognition rather than merely leaning the upright, and encourage themes to pair italic with colour and weight so meaning never rests on slant alone.

## 5. Strength of evidence and limitations

This assessment is only as honest as its caveats, which reviewers and onboarding readers should understand:

- **Preference is not performance.** Much low-vision evidence measures subjective preference, which does not always track measured reading speed or accuracy. The Luciole validation is candid about this: roughly half of low-vision participants preferred the font, while its objective advantages over comparison fonts were slight.
- **Individual variation is large.** Presbyopia varies in degree and correction status, and reading performance is highly individual. No single set of letterforms is optimal for everyone; the field's own conclusion is that personalised recommendation matters.
- **Transfer assumptions are real.** Several cited studies concern low-vision or distance reading, applied here through the shared mechanism of a degraded image. The logic is sound but it is an inference, not a presbyopia-specific result.
- **The serif/sans question is genuinely unsettled.** Our selective-serif rationale is defensible precisely because it does not depend on the broad claim that serifs beat sans (they do not, reliably) — only on the narrower, better-supported claims in 4.4.

## 6. Recommendations for upcoming work

- **Run a blur-simulation legibility pass.** Render the full confusable set and representative code, apply a Gaussian blur calibrated to a few diopters of uncorrected near add (the method Nini uses to model the aging eye), and record which glyph pairs collapse first. This converts review from taste into evidence and is roughly an afternoon of work.
- **Settle the zero deliberately.** Adopt the slashed zero as default for blur robustness; expose a dotted variant via the OpenType 'zero' feature for users who need it.
- **Hold the open apertures.** Treat the open e as final; document the open c as an intentional judgement call so it is not “corrected” in a later round.
- **Constrain the italic.** Decide explicitly how much work the slant does, and pair it with weight and colour rather than relying on angle alone.
- **Pressure-test the Bold.** Confirm the Bold weight still preserves open counters and does not work against the aperture strategy.
- **Consider a small targeted user test.** A short preference-and-error study with developers aged roughly 40+ would generate the one kind of evidence this project does not yet have — from its actual audience. Preference data is meaningful precisely because this group is the intended user.

## 7. Selected references

Sources are listed in rough priority for a review packet. Citations omit volume or page detail where it could not be confirmed.

Beier, S., & Oderkerk, C. A. T. (2022). *Closed letter counters impair recognition.* Applied Ergonomics, 101, 103709. — Controlled basis for the open-aperture decision (4.3).

The effect of serifs and stroke contrast on low vision reading (2022). *Applied Ergonomics.* — Study of low-acuity (ADOA) readers supporting selective serifs with uniform stroke width (4.4).

Galiano, A. R., et al. (2023). *Luciole, a new font for people with low vision.* Acta Psychologica. — Validation methodology and the candid preference-versus-performance result (Section 5).

Nini, P. J. *Typography and the Aging Eye: Typeface Legibility for Older Viewers with Vision Problems.* — Source of the blur-simulation review protocol (Recommendation 1).

Beier, S., & Dyson, M. C. (2014). Work on distance legibility and the role of serifs at the vertical extremes — basis for serif placement (4.4, 4.6).

Beier, S. (2012). *Reading Letters: Designing for Legibility.* BIS Publishers. — General reference for aperture, x-height, and spacing principles.

Tinker, M. A. (1963). *Legibility of Print.* Iowa State University Press. — Early statement of the enclosed-white-space principle.

Atkinson Hyperlegible (2019). Braille Institute & Applied Design Works. — Reference implementation of per-glyph disambiguation and selective serifs (4.2, 4.4).

Arditi, A. *Making Text Legible: Designing for People with Partial Sight.* Lighthouse International. — Spacing and monospace guidance (4.1).

Vision Australia. *Typography in Inclusive Design.* — Guidance on italics and emphasis (4.7).

*Prepared as a synthesis of published legibility research. It is a working document and should be revised as the design evolves and as project-specific testing produces new evidence.*
