# Scene Generation Guide

How to use AI assistants (Claude, GPT, etc.) to generate ManimCE scenes efficiently with `manim-studio`.

## Quick Start

Give the AI this context:

1. **The base class API** (copy from below)
2. **Your theme** (e.g., "dark_swiss")
3. **One example scene** from your project
4. **The scene specification** (title, concept, narration, visuals)

## Base Class API

```python
from manim import *
from manim_studio import (
    NarratedScene,              # base class (auto setup/teardown)
    NarratedMovingCameraScene,  # same + camera controls
    make_title,                 # positioned title + optional subtitle
    equation_stack,             # vertical MathTex arrangement
    make_legend,                # color-coded legend
    data_scaler,                # auto-scale 2D data to scene coords
    labeled_arrow,              # arrow with text label
    apply_theme,                # load color theme
    timing_preset,              # load timing constants
)
```

### NarratedScene

```python
class MyScene(NarratedScene):
    background_color = "#1a1a2e"  # override per-scene if needed
    speech_service = "gtts"       # "gtts", "elevenlabs", "azure", "recorder"
    auto_fade_out = True          # auto-cleanup at end

    def construct(self):
        with self.voiceover(text="Narration here.") as tracker:
            self.play(Create(Circle()))
```

### Helpers

```python
# Title at top of screen
title = make_title("Main Title", subtitle="Optional subtitle")

# Stack equations vertically on right side
eqs = equation_stack(eq1, eq2, eq3, position=RIGHT, buff=0.2)

# Color legend in upper-left
legend = make_legend([("#e63946", "Prediction"), ("#457b9d", "Measurement")])

# Auto-scale trajectory data to fit scene
to_scene = data_scaler(positions, measurements, target_scale=4.0)
scene_point = to_scene(np.array([x, y]))  # returns [sx, sy, 0]

# Arrow with label
arrow = labeled_arrow(start_3d, end_3d, "Force", color=RED)
```

### Themes

```python
theme = apply_theme("dark_swiss")  # or "3b1b_classic", "light", "nord"
# theme["bg"], theme["primary"], theme["secondary"], theme["accent"],
# theme["highlight"], theme["text"], theme["muted"], theme["success"], theme["error"]

timing = timing_preset("normal")   # or "relaxed", "fast"
# timing["fast"], timing["normal"], timing["slow"],
# timing["pause_short"], timing["pause_medium"], timing["pause_long"]
```

## Prompt Template

```
Create a ManimCE scene using manim-studio.

Theme: dark_swiss
Base class: NarratedScene

Scene: [Title]
Concept: [What this scene teaches]
Duration: ~[X] seconds
Narration: [Script or key points]

Visual elements:
- [Element 1]
- [Element 2]
- [Animations/transitions]

Use make_title for the title, equation_stack for any equations,
and wrap animation groups in voiceover blocks.
```

## Tips for Token Efficiency

1. **Don't repeat the API** — provide it once in the system prompt or first message
2. **Provide 1 example scene** — the AI will match its style
3. **Be specific about narration** — the script is the most creative part; equations and animations are mechanical
4. **Request structured output** — single Python file, no explanations needed
5. **Iterate on narration separately** — write the script first, then generate the scene code

## Rendering

```bash
# Development preview (fast, low quality)
PYTHONPATH=. manim -pql scene.py SceneName --disable_caching

# Final render (1080p60)
PYTHONPATH=. manim -qh scene.py SceneName --disable_caching

# PNG only (fastest, for checking layout)
PYTHONPATH=. manim -ql --format png scene.py SceneName --disable_caching
```
