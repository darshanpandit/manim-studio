---
name: manim-studio
description: |
  Trigger when: (1) User wants to create a narrated ManimCE scene, (2) Code contains `from manim_studio import`, (3) User mentions "manim-studio" or "NarratedScene", (4) User wants to generate an educational video scene with voiceover.

  Integration layer for ManimCE video production. Provides base scene classes with automatic TTS setup and teardown, helper functions for titles/equations/legends/data-scaling, color themes, and timing presets. Eliminates ~60% of per-scene boilerplate.

  Requires: `pip install -e path/to/manim-studio` (or `pip install manim-studio` when published).
  Dependencies: manim >= 0.18, manim-voiceover[gtts].
---

## Quick Reference

```python
from manim import *
from manim_studio import (
    NarratedScene,              # base class (auto TTS setup, bg color, fade-out)
    NarratedMovingCameraScene,  # same + camera zoom/pan
    make_title,                 # positioned title + optional subtitle
    equation_stack,             # vertical MathTex arrangement
    make_legend,                # color-coded legend
    data_scaler,                # auto-scale 2D data to scene coords
    labeled_arrow,              # arrow with text label
    apply_theme,                # load color theme dict
    timing_preset,              # load timing constants dict
)
```

## Base Scene Classes

### NarratedScene

Inherits from `VoiceoverScene` + `Scene`. Automatically:
- Calls `set_speech_service()` in `setup()` (before `construct()`)
- Sets `camera.background_color`
- Fades out all mobjects in `tear_down()` (after `construct()`)

```python
class MyScene(NarratedScene):
    background_color = "#1a1a2e"  # override per-scene (default: "#1a1a2e")
    speech_service = "gtts"       # "gtts", "elevenlabs", "azure", "recorder"
    auto_fade_out = True          # set False to skip auto-cleanup

    def construct(self):
        # No setup needed — just write your content
        with self.voiceover(text="Narration here.") as tracker:
            self.play(Create(Circle()))
        # No fade-out needed — automatic
```

### NarratedMovingCameraScene

Same as `NarratedScene` but inherits `MovingCameraScene` for camera controls:

```python
class TrajectoryScene(NarratedMovingCameraScene):
    def construct(self):
        # self.camera.frame available for zoom/pan
        self.play(self.camera.frame.animate.set_width(8))
```

## Helper Functions

### make_title(text, subtitle=None, color=WHITE, font_size=48) -> VGroup

```python
title = make_title("Kalman Filter")              # title only
title = make_title("Part 1", subtitle="Basics")  # title + subtitle
self.play(Write(title[0]))                        # animate the title Text
```

### equation_stack(*equations, position=RIGHT, buff=0.2) -> VGroup

```python
eq1 = MathTex(r"x_{k+1} = F x_k + w_k")
eq2 = MathTex(r"z_k = H x_k + v_k")
eqs = equation_stack(eq1, eq2, position=RIGHT, buff=0.2)
# Stacked vertically, aligned left, positioned at right edge
```

Parameters: `position` (edge), `buff` (vertical spacing), `shift` (offset), `aligned_edge` (LEFT default), `outer_buff` (edge distance).

### make_legend(items, position=UL) -> VGroup

```python
legend = make_legend([
    ("#e63946", "Prediction"),
    ("#457b9d", "Measurement"),
    ("#f4a261", "Posterior"),
], position=UL)
```

### data_scaler(*arrays, target_scale=4.0) -> Callable

```python
to_scene = data_scaler(true_positions, measurements, target_scale=4.0)
scene_point = to_scene(np.array([x, y]))  # returns [sx, sy, 0]
```

Auto-centers and scales 2D data to fit within `target_scale` scene units.

### labeled_arrow(start, end, label_text, color=WHITE) -> VGroup

```python
arrow = labeled_arrow(np.array([0,0,0]), np.array([2,1,0]), "Force", color=RED)
```

## Themes

Four built-in color themes. Each returns a dict with keys: `bg`, `primary`, `secondary`, `accent`, `highlight`, `text`, `muted`, `success`, `error`.

```python
theme = apply_theme("dark_swiss")     # Swiss red/blue/gold on dark bg
theme = apply_theme("3b1b_classic")   # 3Blue1Brown blue/green/yellow
theme = apply_theme("light")          # Light background
theme = apply_theme("nord")           # Nord color scheme
```

### Theme Colors

| Theme | bg | primary | secondary | accent |
|-------|-----|---------|-----------|--------|
| dark_swiss | #1a1a2e | #e63946 | #457b9d | #f4a261 |
| 3b1b_classic | #1c1c1c | #58C4DD | #83C167 | #FFFF00 |
| light | #fafafa | #2d3436 | #0984e3 | #fdcb6e |
| nord | #2e3440 | #88c0d0 | #81a1c1 | #ebcb8b |

## Timing Presets

```python
timing = timing_preset("normal")    # default
timing = timing_preset("relaxed")   # slower, more pauses
timing = timing_preset("fast")      # quick pacing

# Keys: fast, normal, slow, pause_short, pause_medium, pause_long
self.play(Write(title), run_time=timing["normal"])
self.wait(timing["pause_short"])
```

## Complete Scene Template

```python
"""Scene: [Title]
[One-line description]
"""
from manim import *
from manim_studio import NarratedScene, make_title, equation_stack, apply_theme, timing_preset

theme = apply_theme("dark_swiss")
t = timing_preset("normal")

class SceneExample(NarratedScene):
    background_color = theme["bg"]

    def construct(self):
        title = make_title("Topic Name", color=theme["text"])

        with self.voiceover(text="Opening narration.") as tracker:
            self.play(Write(title[0]), run_time=t["normal"])

        eq1 = MathTex(r"E = mc^2", color=theme["accent"])
        eq2 = MathTex(r"F = ma", color=theme["primary"])
        eqs = equation_stack(eq1, eq2, position=ORIGIN, outer_buff=1.0)

        with self.voiceover(text="Key equations.") as tracker:
            for eq in eqs:
                self.play(Write(eq), run_time=t["normal"])

        self.wait(t["pause_long"])
        # auto_fade_out handles cleanup
```

## Rendering

```bash
# Development preview
manim -pql scene.py SceneName --disable_caching

# Final HQ render (1080p60)
manim -qh scene.py SceneName --disable_caching

# PNG only (fastest for layout checks)
manim -ql --format png scene.py SceneName --disable_caching
```

## Rules for Scene Generation

1. **Always use NarratedScene or NarratedMovingCameraScene** as the base class — never raw Scene or VoiceoverScene
2. **Always load a theme** at module level with `apply_theme()` and use `theme["..."]` for colors
3. **Always wrap animation groups in `with self.voiceover()` blocks** for narration sync
4. **Use `make_title()` for titles** — don't manually create and position Text
5. **Use `equation_stack()` for math** — don't manually arrange VGroups of MathTex
6. **Use `data_scaler()` for trajectory data** — don't manually compute center/scale
7. **Don't add setup boilerplate** — no `set_speech_service()`, no `camera.background_color`, no final `FadeOut`
8. **Use `--disable_caching` flag** when rendering scenes with voiceover
9. **Data integrity** — Use real data for flagship demos when available. Use curated synthetic only for edge-case/failure-mode illustrations. Always disclose data source in narration.
10. **Theory-observation honesty** — Never silently hide theory-observation mismatches. When visualization doesn't fully support a theoretical claim, add: (a) verbal acknowledgment in voiceover, (b) subtle on-screen annotation via `make_observation_note()`. Present theory correctly, show actual results, explain the gap.
11. **Data provenance** — Document data source in scene docstrings: `Data: real-world (dataset, ID)`, `Data: curated synthetic (target behavior, seed=N)`, or `Data: synthetic (seed=N)`.
