"""Template: [Scene Title]

[One-line description of what this scene teaches]

Usage:
    PYTHONPATH=. manim -pql templates/scene_template.py SceneTemplate --disable_caching
"""

from manim import *
from manim_studio import NarratedScene, make_title, equation_stack, apply_theme

# Load your project's theme
theme = apply_theme("dark_swiss")


class SceneTemplate(NarratedScene):
    background_color = theme["bg"]

    def construct(self):
        # ── Title ──────────────────────────────────────────────────────
        title = make_title("Your Topic Here", color=theme["text"])

        with self.voiceover(text="Opening narration goes here.") as tracker:
            self.play(Write(title[0]), run_time=1.0)

        # ── Main content ──────────────────────────────────────────────
        eq1 = MathTex(r"E = mc^2", color=theme["accent"])
        eq2 = MathTex(r"F = ma", color=theme["primary"])

        eqs = equation_stack(eq1, eq2, position=ORIGIN, outer_buff=1.0)

        with self.voiceover(text="Here are the key equations.") as tracker:
            for eq in eqs:
                self.play(Write(eq), run_time=0.8)

        self.wait(1.0)

        # ── Cleanup is automatic (auto_fade_out = True) ───────────────
