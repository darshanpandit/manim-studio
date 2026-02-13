---
name: screenplay-writer
description: Use when creating, brainstorming, or writing a new ManimCE video scene, planning narration and visual beats, or when user says write a script or screenplay for an educational math animation
---

# Writing Screenplays for ManimCE

Brainstorm and write `.screenplay` files — a Fountain-inspired DSL that specifies narrative, visuals, and data for ManimCE scenes. The screenplay is a complete scene spec in readable format, not code.

## Process

1. **Check project context** — Read `CLAUDE.md` and any project style guide for available mobjects, colors, data sources, and conventions.
2. **Teaching goal** — What should the viewer understand after this scene?
3. **Data choice** — What data drives the visuals? Precomputed, generated, or none?
4. **Narrative arc** — Choose a pedagogical pattern (see below).
5. **Write beats** — Each beat = voiceover + visuals. 3-8 beats per scene.
6. **Save** to `screenplays/` directory (project determines subfolder structure).

## Pedagogical Patterns

Pick one arc per scene:

| Pattern | Structure | When to use |
|---------|-----------|-------------|
| **Hook** | Mystery/question, reveal, tease solution | Opening scenes |
| **Concept** | Intuition first, then formalize, then "why it works" | Teaching new math |
| **Demo** | Setup, run algorithm, interpret results | Showing a method in action |
| **Comparison** | Side-by-side, metrics, decision guide | Comparing approaches |
| **Capstone** | Recap, taxonomy, open questions | Closing scenes |

### Storytelling Principles

These are lessons from educational math animation (3Blue1Brown style):

- **Show before tell.** Visual intuition first, equations later (or never).
- **One idea per beat.** If a beat explains two things, split it.
- **Conversational narration.** "Look at how..." not "We observe that..." or "It can be shown that..."
- **Emotional arc.** Start with wonder or curiosity, build tension, resolve with insight.
- **Concrete before abstract.** Show a specific example, then generalize.
- **Visual metaphors over formulas.** An ellipse shrinking IS the uncertainty reducing — say that. A dot cloud converging IS the algorithm working — show it.
- **Honest about limitations.** Acknowledge when theory meets practice. Cite papers.
- **Silence is powerful.** A `PAUSE:` after a key visual lets the viewer absorb it.

## DSL Syntax

### File Structure

```
PART N: Part Title
SCENE NN: Scene Title — "Subtitle"

REFERENCES:
  - Author (Year) — description

DATA:
  source: description of data source
  parameters: as needed by the project

= BEAT 1: Description =

[directives and voiceover]

= BEAT 2: Description =

[directives and voiceover]

FADEOUT: all
```

### Header Block

```
PART N: Part Title
SCENE NN: Scene Title — "Subtitle"
```

Required. Identifies which video and scene.

### References Block (optional)

```
REFERENCES:
  - Author (Year) — description
```

Papers or sources to cite. Generates citation annotations in the scene.

### Data Block (optional)

```
DATA:
  source: description or path
  key: value
```

Freeform key-value block describing what data the scene needs. Project-specific — the code generator interprets this based on project conventions (check `CLAUDE.md`).

### Beat Block

```
= BEAT N: Short Description =
```

A narrative segment. Each beat pairs voiceover with visuals. 3-8 beats per scene.

### Voiceover

```
> Narrator text goes in blockquotes.
> Can span multiple lines.
> This becomes the text-to-speech voiceover.
```

Every beat must have at least one voiceover block. Write conversationally — this is spoken aloud.

### Visual Directives

**TITLE** — prominent heading text:
```
TITLE: "Text" (position)
```
Position: `top`, `center`. Typically one per scene.

**TEXT** — on-screen text (not narration):
```
TEXT: "Short phrase" (position)
TEXT: "Emphasized text" (position, color_name)
```
Position: `top`, `bottom`, `center`, or relative like `below title`.

Keep text SHORT: max 6 words, max 2 lines. This is a title card, not a paragraph. The voiceover carries the explanation.

**SHOW** — create and display a visual element:
```
SHOW: description of what to display
SHOW: MobjectName(parameters) at position
SHOW: axes with range [0,10] x [0,5], size 7x4
SHOW: data points appearing in batches of 8
SHOW: path as dashed line
```

Descriptive — the code generator interprets these into specific Manim code. Reference project mobjects by name when available.

**ANIMATE** — dynamic behavior over time:
```
ANIMATE: description of motion or transformation
ANIMATE: dots morphing from blue to gold
ANIMATE: step through values at indices [10, 25, 45]
```

**PAUSE** — timing break:
```
PAUSE: short
PAUSE: medium
PAUSE: long
```

Maps to project-defined timing constants.

**NOTE** — citation/reference annotation:
```
NOTE: "Author (Year): Key finding.\nSecond line if needed."
```

Typically placed near scene end.

**FADEOUT** — scene cleanup:
```
FADEOUT: all
FADEOUT: title, subtitle
```

`FADEOUT: all` is required as the last directive.

### Style References

Use `$NAME` to reference project-defined style constants:
```
SHOW: path colored $COLOR_PRIMARY
TEXT: "Key insight" (bottom, $COLOR_HIGHLIGHT)
```

Available constants depend on the project — check `CLAUDE.md` or project style guide.

## Complete Example

```
PART 1: Introduction
SCENE 01: Hook — "Where is it?"

REFERENCES:
  - Smith et al. (2009) — Dataset source

DATA:
  source: real_dataset/trajectory #42
  noise_std: 0.6
  max_steps: 60
  algorithm: BasicFilter(params)

= BEAT 1: The mystery =

TITLE: "Where is it?" (top)
SHOW: noisy measurement dots appearing in batches of 8

> Where is it? These are real measurements from a sensor.
> Each reading gives a position estimate, but look at how
> noisy they are. Can we do better?

PAUSE: medium

= BEAT 2: The truth revealed =

TEXT: "What's really happening?" (below title)
SHOW: true path as dashed line

> Here's what's actually happening — a smooth, continuous
> path. But all we get from the sensor are those scattered,
> noisy observations.

= BEAT 3: The solution =

TEXT: "Can we recover the truth?" (bottom, $COLOR_HIGHLIGHT)
SHOW: filtered estimate path ($COLOR_RESULT)
TEXT: "Yes." (replace previous, $COLOR_RESULT)

> Can we recover the true path from noisy measurements?
> Yes. By intelligently combining predictions with
> observations, we get remarkably close to the truth.

PAUSE: long

> Over the next few videos, I'll show you exactly how.

FADEOUT: all
```

## Validation Before Saving

- [ ] Every beat has voiceover (`>` lines)
- [ ] Every beat has at least one visual (`SHOW`, `ANIMATE`, `TITLE`, or `TEXT`)
- [ ] DATA block is complete if scene uses data
- [ ] 3-8 beats total
- [ ] Voiceover is conversational, not academic
- [ ] On-screen text is SHORT (max 6 words per line, max 2 lines)
- [ ] Last directive is `FADEOUT: all`
- [ ] Total voiceover reads aloud in ~2-4 minutes
- [ ] One teaching goal per scene, not three
- [ ] Checked project CLAUDE.md for available assets

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Cramming 3 ideas into one scene | Split into multiple scenes |
| Academic prose in voiceover | "Look at this" not "One can observe" |
| Too much on-screen text | Text = title card. Narration carries the story. |
| No visual for a beat | If you can't show it, it's not a beat |
| Forgetting data spec | Scene without data = nothing to animate |
| 10+ beats | Split the scene if > 8 |
| Using project-specific terms without checking | Read CLAUDE.md first |
