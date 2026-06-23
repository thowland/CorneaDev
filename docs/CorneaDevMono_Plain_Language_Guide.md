# Why CorneaDev Mono

**looks the way it does**

*A plain-language guide to a coding font built for eyes over 40.*

CorneaDev Mono is a monospace typeface — the kind you write code in — designed with one particular reader in mind: someone whose near vision has started doing the thing that near vision does after about age 40. A few of its letters look a little unusual at first glance. All of that is on purpose. This guide explains the why, in plain terms, no type-design vocabulary required.

**First, the one fact that explains almost everything**

Around 40, the lens inside the eye gets less flexible and stops focusing up close as easily. The name for this is presbyopia, and it happens to nearly everyone eventually. It is not a disease and it is not going blind — it just means small things held close, like code on a screen, get a bit blurry.

So the whole design problem is this: **make letters that still tell themselves apart when the picture is slightly out of focus.** Once you know that's the goal, every odd-looking choice below stops being odd.

**Why does the lowercase “a” (and “e”) look a bit funny?**

Look at the little gap that lets you see into the inside of an “a,” “e,” or “c.” In CorneaDev Mono we keep that gap wide open instead of curling it almost shut. That openness is what reads as slightly unusual.

Here's the reason. When letters blur, the first thing that happens is that their openings fill in and the letters start to smear into their neighbours. A wide-open “e” stays an “e” when it's fuzzy; a nearly-closed one turns into a gray blob that could be an “s” or a “o.” Researchers have actually tested this — letters with open gaps are recognised more reliably than the same letters drawn closed, especially when they're crowded together like they are in a line of code. The funny-looking “e” is the whole point of the font working.

**It's a sans-serif font… except sometimes it isn't?**

Correct, and that's deliberate too. “Serifs” are the little feet on the ends of letter strokes. CorneaDev Mono is mostly a clean, footless (sans-serif) design — but we added tiny serifs to a handful of specific letters, like the capital “I” and the bottom of the lowercase “l.”

Why the inconsistency? Because those particular letters are troublemakers: a plain capital I, a lowercase l, and the number 1 can all look like the same vertical stick. A small serif gives each one a distinct silhouette so you don't have to guess. We didn't put serifs everywhere — just on the letters that earn them. (The makers of Atkinson Hyperlegible, a well-known accessibility font, do exactly the same thing.)

**What's with the slash through the zero?**

Blur turns a capital “O” and a zero into the same circle. In code, mixing those up breaks things. The slash makes the zero unmistakably a *zero*, every time, even when you can barely focus. It's a small mark that prevents a genuinely annoying class of mistake.

**Why monospace? Doesn't that waste space?**

Two reasons. The practical one: code relies on things lining up — indentation, columns, the way a diff shows what changed. Monospace (every character the same width) makes that alignment automatic. The bonus reason: the even, roomy spacing that comes with monospace also happens to be easier on tired or unfocused eyes, because letters aren't jammed together. We'd have used monospace anyway; it just turns out to help.

**Is any of this actually proven, or did we just decide it looked good?**

Honest answer: it's a mix, and we'd rather say so.

- **Solidly tested:** the open letter shapes and the disambiguated characters (the zero, the I/l/1 family) rest on real experiments.
- **Expert consensus:** the selective serifs, the stroke weight, and the spacing follow well-established professional guidance plus some good supporting studies.
- **Genuinely individual:** eyes differ a lot, and how much any one person likes a font is personal. No typeface is perfect for everybody.

So we lean on the evidence where it's strong, follow informed judgement where it isn't, and we test rather than assume. If a choice ever turns out not to help, it's allowed to change.

**And the italics?**

Italics are the soft spot. Slanted text is the hardest style for exactly the eyes this font is meant to help. We can't drop it — code editors use italics for comments and the like — so instead we keep the slant gentle and lean on bolder weight and colour to do the heavy lifting. If you're setting up a theme, don't make italics carry an important distinction all on their own.

**Who is this actually for?**

Mainly developers around 40 and up, and anyone who reads code at small sizes or in less-than-ideal light. But good legibility design is meant to be invisible: if you don't have any trouble reading, CorneaDev Mono should simply feel like a clean, comfortable coding font and never announce that it's an “accessibility” typeface. That's the goal — helpful to the people who need it, unremarkable to everyone else.

> **The short version** Presbyopia makes close-up text blurry. CorneaDev Mono draws every letter so it survives that blur — open shapes that don't smear, a few well-placed serifs to keep look-alike characters apart, a slashed zero, and roomy spacing. The unusual-looking letters are the ones doing the work.

*Want the evidence and the references? See the companion document, “CorneaDev Mono — Legibility Assessment & Design Rationale.”*
