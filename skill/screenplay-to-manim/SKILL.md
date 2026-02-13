---
name: screenplay-to-manim
description: Use when converting a .screenplay file to ManimCE Python code, generating scene files from screenplays, or when user says generate, render, or build a scene from a screenplay
---

# Generating ManimCE Code from Screenplays

Read a `.screenplay` file and generate a complete, frame-safe ManimCE scene `.py` file. This skill encodes hard-won layout constraints learned from iterative testing — vague advice does not produce good Manim output, only explicit invariants do.

## Process

1. **Read project context** — Check `CLAUDE.md` for project conventions (base classes, style imports, boilerplate, available mobjects, data sources).
2. **Read the screenplay** — Parse header, data block, and all beats.
3. **Read existing scene files** — Find 1-2 examples in the project to match the code style.
4. **Generate the scene file** — Follow the layout invariants below.
5. **Run the Layout Verifier** — Mental self-check before saving (see below).
6. **Save** to the project's scene directory.

## Scene File Structure

### Single-voice scene (no `VOICES:` block)

```python
"""[Scene description from screenplay header]"""

from __future__ import annotations

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Project-specific imports (style, mobjects, data — check CLAUDE.md)


class SceneName(VoiceoverScene, MovingCameraScene):
    """Docstring from screenplay SCENE header."""

    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = BG_COLOR

        # ── Data setup ────────────────────────────────────
        # [from DATA: block]

        # ── Beat 1: [description] ─────────────────────────
        with self.voiceover(text="...") as tracker:
            # [visual directives]

        # ── Cleanup ───────────────────────────────────────
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=...)
```

### Multi-voice scene (with `VOICES:` block)

```python
"""[Scene description from screenplay header]"""

from __future__ import annotations

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
import numpy as np
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Project-specific imports


class SceneName(VoiceoverScene, MovingCameraScene):
    """Docstring from screenplay SCENE header."""

    def construct(self):
        # ── Voice setup ───────────────────────────────────
        # One AzureService per voice, using default style from VOICES: block
        narrator = AzureService(voice="en-US-JennyNeural", style="chat")
        skeptic = AzureService(voice="en-US-TonyNeural", style="friendly")
        self.set_speech_service(narrator)
        self.camera.background_color = BG_COLOR

        # ── Data setup ────────────────────────────────────
        # [from DATA: block]

        # ── Beat 1: [description] ─────────────────────────
        self.set_speech_service(narrator)
        with self.voiceover(text="Narrator speaks...") as tracker:
            # [visual directives]

        self.set_speech_service(skeptic)
        with self.voiceover(text="Skeptic responds.") as tracker:
            self.wait(PAUSE_SHORT)

        # ── Cleanup ───────────────────────────────────────
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=...)
```

## DSL-to-Code Mapping

### Visual and timing directives

| Screenplay | Python |
|------------|--------|
| `TITLE: "X" (top)` | `Text("X", ..., font_size=TITLE_SIZE).to_edge(UP, buff=0.3)` |
| `TEXT: "X" (bottom)` | `Text("X", ...).to_edge(DOWN, buff=0.5)` |
| `TEXT: "X" (position, $COLOR)` | `Text("X", color=COLOR, ...).to_edge(...)` |
| `SHOW: axes(...)` | `Axes(x_range=..., y_range=..., x_length=N, y_length=N)` |
| `SHOW: path as dashed line` | `DashedVMobject(path, num_dashes=N)` |
| `ANIMATE: ...` | Appropriate `self.play(...)` calls |
| `PAUSE: short` | `self.wait(PAUSE_SHORT)` or `self.wait(0.5)` |
| `PAUSE: medium` | `self.wait(PAUSE_MEDIUM)` or `self.wait(1.0)` |
| `PAUSE: long` | `self.wait(PAUSE_LONG)` or `self.wait(2.0)` |
| `NOTE: "text"` | Project-specific citation mobject (check CLAUDE.md) |
| `FADEOUT: all` | `self.play(*[FadeOut(mob) for mob in self.mobjects])` |
| `$COLOR_NAME` | Direct constant reference from project style |

### Voiceover and voice directives

| Screenplay | Python |
|------------|--------|
| `> text` (no VOICES block) | `with self.voiceover(text="...") as tracker:` |
| `> [NAME] text` | `self.set_speech_service(name); with self.voiceover(text="...") as tracker:` |
| `> [NAME, style=X] text` | Create new `AzureService(voice=..., style="X")`, set it, then voiceover |
| `> [NAME, rate=+15%] text` | `with self.voiceover(text="...", prosody={"rate": "+15%"}) as tracker:` |
| `> [NAME, pitch=-5Hz] text` | `with self.voiceover(text="...", prosody={"pitch": "-5Hz"}) as tracker:` |
| `> [NAME, volume=+20%] text` | `with self.voiceover(text="...", prosody={"volume": "+20%"}) as tracker:` |
| `> [NAME, style=X, rate=Y]` | New AzureService + prosody combined |

### Voice tag rules

1. **Each `[TAG]` switch = new voiceover block.** Consecutive lines with the same tag are concatenated into one block.
2. **Style overrides create new AzureService instances.** Cache them to avoid recreating:

```python
# At top of construct():
narrator = AzureService(voice="en-US-JennyNeural", style="chat")
narrator_whisper = AzureService(voice="en-US-JennyNeural", style="whispering")
skeptic = AzureService(voice="en-US-TonyNeural", style="friendly")
skeptic_excited = AzureService(voice="en-US-TonyNeural", style="excited")
```

3. **Prosody is per-voiceover, not per-service.** Pass it to `self.voiceover()`:

```python
self.set_speech_service(narrator)
with self.voiceover(
    text="This part is spoken slowly...",
    prosody={"rate": "-15%", "pitch": "-3Hz"},
) as tracker:
    self.wait(PAUSE_MEDIUM)
```

4. **Distribute animations across voice blocks.** When a beat has multiple voice tags, the first voice block gets the main animations. Subsequent interjections typically just `self.wait()`:

```python
# Beat with narrator + skeptic exchange
self.set_speech_service(narrator)
with self.voiceover(text="Here's what happens...") as tracker:
    self.play(FadeIn(diagram), run_time=NORMAL_ANIM)

self.set_speech_service(skeptic)
with self.voiceover(text="That seems too simple.") as tracker:
    self.wait(PAUSE_SHORT)  # visuals hold during skeptic's line

self.set_speech_service(narrator)
with self.voiceover(text="It is. That's the beauty of it.") as tracker:
    self.wait(PAUSE_MEDIUM)
```

---

## NON-NEGOTIABLE LAYOUT INVARIANTS

These are not suggestions. They are invariants that the generated code must satisfy. Violating any of these produces broken, ugly, or unwatchable output. These rules were refined through 23 iterations of testing — every one exists because softer guidance failed.

### 1. Safe Frame

The ManimCE camera is 16:9. The safe visible region:
- **Horizontal:** x in `[-6, 6]` with at least 0.2 padding → usable: `[-5.8, 5.8]`
- **Vertical:** y in `[-3.4, 3.4]` with at least 0.2 padding → usable: `[-3.2, 3.2]`

Every visible mobject must stay inside this region. No exceptions.

### 2. No Overlapping Text — ABSOLUTE RULE

Never show more than one paragraph-level text block on screen at once. If two short labels must coexist, they MUST be explicitly arranged:

```python
# CORRECT: explicit arrangement
labels = VGroup(label_a, label_b).arrange(DOWN, buff=0.3)

# WRONG: manual placement that might overlap
label_a.move_to(UP * 0.5)
label_b.move_to(UP * 0.3)  # overlaps!
```

### 3. Short Text Only

- Summarize into **4-6 word phrases**
- **Maximum ~3 lines** per Text block
- **Maximum ~35-40 characters** per line — if longer, split into two stacked Text objects
- Never copy long sentences from the screenplay voiceover into on-screen text
- On-screen text is a title card. The voiceover carries the explanation.

### 4. Vertical Bands

Organize the frame into non-overlapping horizontal bands:

| Band | Y range | Contents |
|------|---------|----------|
| **Title** | y > 2.4 | Scene title, `.to_edge(UP, buff=0.3)` |
| **Subtitle** | y ~ 2.0 | Optional subtitle, `.next_to(title, DOWN, buff=0.2)` |
| **Diagram** | y ~ -1.5 to 2.0 | Main visual content |
| **Lower text** | y ~ -2.0 to -1.5 | Explanatory text, labels |
| **Note/citation** | y < -2.5 | Citations, footnotes |

Bands must not share vertical space. If content from two bands overlaps, something is wrong.

### 5. Relative Positioning Only

**Never use raw coordinates for text placement.** Always use:
- `.to_edge(UP/DOWN/LEFT/RIGHT, buff=N)`
- `.next_to(other_mobject, direction, buff=N)`
- `VGroup(...).arrange(direction, buff=N)`
- `.move_to(ORIGIN)` only for centering groups

```python
# CORRECT
title.to_edge(UP, buff=0.3)
explanation.next_to(diagram, DOWN, buff=0.5)

# WRONG — fragile, may overlap
title.move_to([0, 3.2, 0])
explanation.move_to([0, -1.5, 0])
```

### 6. Minimum Spacing

When stacking text or visual elements vertically:
- **buff >= 0.35** between any two text-like elements
- **buff >= 0.5** between a diagram and text below it
- **buff >= 0.3** between title and subtitle

If elements feel close, increase buff. Crowded is always worse than spread out.

### 7. Group and Scale Multi-Part Layouts

When a scene has multiple diagram parts (left/right comparison, grid of charts):

```python
# ALWAYS group, arrange, and scale-to-fit
full = VGroup(part1, part2, part3)
full.arrange(RIGHT, buff=0.6)
full.scale_to_fit_width(12)  # never exceed 12 units
full.move_to(ORIGIN)
```

Never rely on manual coordinates for multi-part layouts. Always VGroup + arrange + scale.

### 8. Text Boundary Safety

After placing ANY text label, verify it stays in-frame:

```python
# Mental check (or actual code for complex scenes):
# If text exceeds x = ±5, move it
if abs(label.get_x()) > 5:
    # Fallback: place below the reference object instead of beside it
    label.next_to(reference, DOWN, buff=0.4)
```

**Prefer BELOW or ABOVE** over RIGHT for labels near diagram edges. RIGHT placement is the #1 cause of text overflowing the frame.

### 9. Bottom-Edge Constraint

No content below y = -3.2. If a citation note or summary text would go below this:
- Shrink font_size by 2-6 points
- Increase upward buff
- Shift the entire diagram group upward

### 10. Title Z-Index

Titles should stay visible above other content:

```python
title.set_z_index(10)
```

---

## VOICEOVER INTEGRATION

Every beat's animations go INSIDE the voiceover context manager. This synchronizes speech with visuals.

### Single-voice

```python
# CORRECT — animations inside voiceover
with self.voiceover(text="Here's what happens...") as tracker:
    self.play(FadeIn(diagram), run_time=NORMAL_ANIM)
    self.wait(PAUSE_SHORT)
    self.play(Create(path), run_time=SLOW_ANIM)

# WRONG — animations outside voiceover (no sync)
self.play(FadeIn(diagram))
with self.voiceover(text="Here's what happens...") as tracker:
    pass
```

### Multi-voice

Each `[TAG]` switch creates a separate `set_speech_service()` + `voiceover()` block. Consecutive lines with the same tag merge into one block.

```python
# Screenplay:
#   > [NARRATOR] The ellipse grows during prediction.
#   > [SKEPTIC] Why does it grow?
#   > [NARRATOR] Because the model isn't perfect.

# Generated code:
self.set_speech_service(narrator)
with self.voiceover(text="The ellipse grows during prediction.") as tracker:
    self.play(ellipse.animate.scale(1.3), run_time=NORMAL_ANIM)

self.set_speech_service(skeptic)
with self.voiceover(text="Why does it grow?") as tracker:
    self.wait(PAUSE_SHORT)

self.set_speech_service(narrator)
with self.voiceover(text="Because the model isn't perfect.") as tracker:
    self.wait(PAUSE_MEDIUM)
```

### Style overrides mid-scene

```python
# Screenplay:
#   > [NARRATOR, style=whispering] And it's only four equations.

# Generated code — pre-create the style variant at top of construct():
narrator_whisper = AzureService(voice="en-US-JennyNeural", style="whispering")

# Then at the point of use:
self.set_speech_service(narrator_whisper)
with self.voiceover(text="And it's only four equations.") as tracker:
    self.wait(PAUSE_MEDIUM)
```

### Prosody overrides

```python
# Screenplay:
#   > [SKEPTIC, rate=+15%] That seems obvious.

# Generated code — same service, prosody passed per-call:
self.set_speech_service(skeptic)
with self.voiceover(
    text="That seems obvious.",
    prosody={"rate": "+15%"},
) as tracker:
    self.wait(PAUSE_SHORT)
```

### Combined style + prosody

```python
# Screenplay:
#   > [NARRATOR, style=excited, rate=-10%, pitch=+5Hz] This changes everything.

# Generated code:
narrator_excited = AzureService(voice="en-US-JennyNeural", style="excited")
self.set_speech_service(narrator_excited)
with self.voiceover(
    text="This changes everything.",
    prosody={"rate": "-10%", "pitch": "+5Hz"},
) as tracker:
    self.play(Flash(result, color=COLOR_HIGHLIGHT), run_time=0.5)
```

**Voiceover text rules:**
- Concatenate consecutive `>` lines with the **same tag** into one string
- Strip the `>` prefix and `[TAG]` prefix
- Join with spaces (not newlines)
- A tag change = new voiceover block
- No special characters that would break JSON serialization

---

## ANIMATION TIMING

| Type | Speed | Use |
|------|-------|-----|
| Title appearance | `Write()` or `FadeIn(shift=DOWN*0.3)` | Scene opening |
| Content appear | `FadeIn()`, `run_time=FAST_ANIM` | Adding elements |
| Path drawing | `Create()`, `run_time=SLOW_ANIM` | Revealing trajectories |
| Batch appearance | `LaggedStart(*anims, lag_ratio=0.15)` | Multiple dots/items |
| Transitions | `FadeOut()` then `FadeIn()` | Replacing content |
| Exit | `FadeOut()`, `run_time=NORMAL_ANIM` | Clearing screen |

Map `PAUSE:` durations to project constants or sensible defaults (short=0.5s, medium=1.0s, long=2.0s).

---

## LAYOUT VERIFIER PROTOCOL

Before saving generated code, run this mental self-check. This catches the bugs that cause ugly output.

### Step 1: Tag every text element

List every `Text()` in the scene. For each, note:
- **ROLE:** title, subtitle, explanation, label, note, result
- **ANCHOR:** what it's positioned relative to

### Step 2: Bucket into vertical bands

Map each element to a band (title / subtitle / diagram / lower text / note). If two elements share a band and aren't in a VGroup, they will overlap.

### Step 3: Detect suspicious patterns

These are bugs. If you see any, fix before saving:

| Suspicious Pattern | Fix |
|-------------------|-----|
| Multiple Text with `.move_to([x, y, 0])` at similar y | Use VGroup.arrange(DOWN) |
| Magic numbers: `buff=0.12`, `.shift(UP * 0.07)` | Use standard buffs (0.3, 0.5) |
| `next_to(..., DOWN, buff < 0.3)` for stacked text | Increase buff to >= 0.35 |
| Label placed RIGHT of rightmost diagram element | Place BELOW instead |
| Manual coordinates for anything except ORIGIN centering | Use relative positioning |
| Text > 40 characters on one line | Split or shorten |
| VGroup with 3+ items but no `.arrange()` | Add arrangement |
| Animations outside `with self.voiceover(...)` block | Move inside |

### Step 4: Verify frame bounds

- Title: y > 2.4 ✓
- Bottom-most element: y > -3.2 ✓
- Widest element: |x| < 5.8 ✓
- Multi-part groups have `scale_to_fit_width` ✓

### Step 5: Check project conventions

- Correct base classes per CLAUDE.md ✓
- Correct imports and boilerplate ✓
- Style constants from project, not hardcoded colors ✓
- No `MathTex()` if project says `Text()` only ✓
- No `Rectangle(corner_radius=...)` — use `RoundedRectangle` ✓

---

## WHEN MODIFYING EXISTING SCENES

If the screenplay changes an existing scene (not a new one):

1. **Layout correctness overrides code preservation.** If existing code has layout bugs, fix them even if the screenplay didn't mention it.
2. **Treat existing code as a draft.** Preserve the mathematical idea, not every line. You may reorganize, simplify, or rewrite to achieve clean layout.
3. **Be bold in refactoring.** You are explicitly allowed to:
   - Change positions, font sizes, buffs, alignment
   - Split or merge text blocks
   - Regroup mobjects into new VGroups
   - Remove redundant animations
   - Rewrite `construct()` entirely if needed
4. **Keep the class name** unless the user explicitly changes it.

---

## COMMON MISTAKES

These are the specific failure modes learned from testing. Every one of these has caused broken output.

| Mistake | Why it fails | Fix |
|---------|-------------|-----|
| `MathTex()` in a project without LaTeX | Render crashes with `FileNotFoundError: latex` | Use `Text()` — check CLAUDE.md |
| `Rectangle(corner_radius=0.1)` | ManimCE doesn't support this parameter | `RoundedRectangle(corner_radius=0.1)` |
| Text label to RIGHT of diagram | Overflows safe frame on right side | Place BELOW with `buff=0.4` |
| Manual `.move_to([x, y, 0])` for text | Overlaps other text at similar y | Use `next_to()` or `VGroup.arrange()` |
| Animations outside voiceover block | Audio and visuals desync | Move all `self.play()` inside `with self.voiceover()` |
| Forgetting `set_z_index(10)` on title | Later mobjects cover the title | Add `.set_z_index(10)` |
| Parallel Manim renders | GTTS voiceover JSON cache corruption | Render one scene at a time, or accept occasional re-renders |
| `buff=0.1` between stacked text | Elements visually overlap | Use `buff >= 0.35` |
| 50+ character Text on one line | Runs off screen edges | Split at ~35 chars or shorten |
| VGroup with no arrangement | Items pile on top of each other | Always `.arrange(direction, buff=N)` |
| Hardcoded color hex values | Doesn't match project theme | Use `$COLOR_NAME` constants from project style |
| Missing `self.wait()` after key visual | Viewer can't absorb the insight | Add `PAUSE: medium` → `self.wait(1.0)` |
