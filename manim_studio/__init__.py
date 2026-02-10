"""manim-studio: Thin integration layer for ManimCE educational video production."""

from manim_studio.base import NarratedScene, NarratedMovingCameraScene
from manim_studio.helpers import (
    make_title,
    equation_stack,
    make_legend,
    data_scaler,
    labeled_arrow,
)
from manim_studio.themes import apply_theme, timing_preset, THEMES

__all__ = [
    "NarratedScene",
    "NarratedMovingCameraScene",
    "make_title",
    "equation_stack",
    "make_legend",
    "data_scaler",
    "labeled_arrow",
    "apply_theme",
    "timing_preset",
    "THEMES",
]
