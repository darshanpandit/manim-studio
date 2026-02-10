"""Generic, topic-agnostic scene helpers.

These reduce boilerplate for common visual patterns found in educational videos:
titles, equation stacks, legends, data scaling, labeled arrows.
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np
from manim import (
    VGroup, Text, MathTex, Arrow, Dot, Line,
    UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR,
    WHITE, ORIGIN,
)


def make_title(
    text: str,
    subtitle: str | None = None,
    color=WHITE,
    font_size: float = 48,
    subtitle_font_size: float = 28,
    buff: float = 0.3,
) -> VGroup:
    """Create a title (+ optional subtitle) positioned at the top of the screen.

    Returns a VGroup so it can be animated as a single unit.
    """
    title = Text(text, color=color, font_size=font_size)
    title.to_edge(UP, buff=buff)

    if subtitle is None:
        return VGroup(title)

    sub = Text(subtitle, color=color, font_size=subtitle_font_size)
    sub.next_to(title, DOWN, buff=0.15)
    return VGroup(title, sub)


def equation_stack(
    *equations: MathTex,
    position=RIGHT,
    buff: float = 0.2,
    shift: np.ndarray = ORIGIN,
    aligned_edge=LEFT,
    outer_buff: float = 0.3,
) -> VGroup:
    """Arrange MathTex equations vertically with consistent spacing.

    Args:
        *equations: MathTex objects to stack.
        position: Edge to place the stack (RIGHT, LEFT, DOWN, etc.).
        buff: Vertical spacing between equations.
        shift: Additional offset after positioning.
        aligned_edge: Alignment within the stack (LEFT, RIGHT, ORIGIN).
        outer_buff: Distance from the screen edge.
    """
    stack = VGroup(*equations).arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
    stack.to_edge(position, buff=outer_buff)
    if not np.array_equal(shift, ORIGIN):
        stack.shift(shift)
    return stack


def make_legend(
    items: Sequence[tuple],
    position=UL,
    font_size: float = 16,
    buff: float = 0.3,
    line_width: float = 2.5,
) -> VGroup:
    """Create a color-coded legend.

    Args:
        items: List of (color, label_text) tuples.
        position: Corner to place the legend (UL, UR, DL, DR).
        font_size: Text size for labels.
        buff: Distance from screen edge.
        line_width: Stroke width for color swatches.
    """
    rows = VGroup()
    for color, label_text in items:
        swatch = Line(LEFT * 0.3, RIGHT * 0.3, color=color, stroke_width=line_width)
        label = Text(label_text, color=color, font_size=font_size)
        row = VGroup(swatch, label).arrange(RIGHT, buff=0.1)
        rows.add(row)

    rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    rows.to_corner(position, buff=buff)
    return rows


def data_scaler(
    *arrays: np.ndarray,
    target_scale: float = 4.0,
) -> Callable[[np.ndarray], np.ndarray]:
    """Auto-scale 2D data arrays to fit scene coordinates.

    Computes a center and scale factor from the combined data,
    then returns a function that maps (x, y) -> (scene_x, scene_y, 0).

    Args:
        *arrays: 2D numpy arrays of shape (N, 2).
        target_scale: Target half-width of the data in scene units.

    Returns:
        Callable that maps a 2D point to a 3D scene coordinate.
    """
    combined = np.vstack(arrays)
    center = combined.mean(axis=0)
    span = max(np.ptp(combined[:, 0]), np.ptp(combined[:, 1]), 1e-8)
    scale = target_scale / span

    def to_scene(xy: np.ndarray) -> np.ndarray:
        s = (xy - center) * scale
        return np.array([s[0], s[1], 0.0])

    return to_scene


def labeled_arrow(
    start: np.ndarray,
    end: np.ndarray,
    label_text: str,
    color=WHITE,
    font_size: float = 24,
    label_buff: float = 0.1,
) -> VGroup:
    """Arrow with a text label positioned above it.

    Args:
        start: 3D start point.
        end: 3D end point.
        label_text: Text or LaTeX to display.
        color: Arrow and label color.
        font_size: Label text size.
        label_buff: Distance from arrow to label.
    """
    arrow = Arrow(start, end, color=color, stroke_width=2, buff=0.1)
    label = Text(label_text, color=color, font_size=font_size)
    label.next_to(arrow, UP, buff=label_buff)
    return VGroup(arrow, label)
