"""Tests for manim_studio helpers and themes (no rendering required)."""

from __future__ import annotations

import numpy as np
import pytest
from manim import VGroup, MathTex, Text

from manim_studio.helpers import (
    make_title,
    equation_stack,
    make_legend,
    data_scaler,
    labeled_arrow,
)
from manim_studio.themes import apply_theme, timing_preset, THEMES, TIMING_PRESETS


# ── make_title ─────────────────────────────────────────────────────────────

class TestMakeTitle:
    def test_returns_vgroup(self):
        result = make_title("Hello")
        assert isinstance(result, VGroup)

    def test_title_only_has_one_child(self):
        result = make_title("Hello")
        assert len(result) == 1

    def test_with_subtitle_has_two_children(self):
        result = make_title("Hello", subtitle="World")
        assert len(result) == 2

    def test_custom_font_size(self):
        result = make_title("Big", font_size=72)
        assert abs(result[0].font_size - 72) < 0.01


# ── equation_stack ─────────────────────────────────────────────────────────

class TestEquationStack:
    def test_returns_vgroup(self):
        # Use Text instead of MathTex to avoid LaTeX dependency in tests
        eq1 = Text("x = 1", font_size=24)
        eq2 = Text("y = 2", font_size=24)
        result = equation_stack(eq1, eq2)
        assert isinstance(result, VGroup)
        assert len(result) == 2

    def test_vertical_ordering(self):
        eq1 = Text("x = 1", font_size=24)
        eq2 = Text("y = 2", font_size=24)
        stack = equation_stack(eq1, eq2, buff=0.5)
        # First equation should be above the second
        assert stack[0].get_center()[1] > stack[1].get_center()[1]


# ── make_legend ────────────────────────────────────────────────────────────

class TestMakeLegend:
    def test_returns_vgroup(self):
        result = make_legend([("#ff0000", "Red"), ("#0000ff", "Blue")])
        assert isinstance(result, VGroup)

    def test_correct_number_of_rows(self):
        result = make_legend([
            ("#ff0000", "Red"),
            ("#0000ff", "Blue"),
            ("#00ff00", "Green"),
        ])
        assert len(result) == 3


# ── data_scaler ────────────────────────────────────────────────────────────

class TestDataScaler:
    def test_returns_callable(self):
        data = np.array([[0, 0], [1, 1]])
        scaler = data_scaler(data)
        assert callable(scaler)

    def test_output_is_3d(self):
        data = np.array([[0, 0], [10, 10]])
        scaler = data_scaler(data)
        result = scaler(np.array([5, 5]))
        assert result.shape == (3,)
        assert result[2] == 0.0

    def test_center_maps_near_origin(self):
        data = np.array([[0, 0], [10, 10]])
        scaler = data_scaler(data, target_scale=4.0)
        center = scaler(np.array([5.0, 5.0]))
        assert abs(center[0]) < 1e-10
        assert abs(center[1]) < 1e-10

    def test_scale_respects_target(self):
        data = np.array([[0, 0], [10, 0]])
        scaler = data_scaler(data, target_scale=5.0)
        edge = scaler(np.array([10.0, 0.0]))
        # Point at max x should map to +target_scale/2 from center
        # (center is at 5.0, span is 10, scale = 5/10 = 0.5, so (10-5)*0.5 = 2.5)
        assert abs(edge[0] - 2.5) < 1e-10

    def test_multiple_arrays(self):
        a = np.array([[0, 0], [5, 5]])
        b = np.array([[10, 10], [15, 15]])
        scaler = data_scaler(a, b, target_scale=4.0)
        # Center should be mean of combined data
        center = scaler(np.array([7.5, 7.5]))
        assert abs(center[0]) < 1e-10
        assert abs(center[1]) < 1e-10


# ── labeled_arrow ──────────────────────────────────────────────────────────

class TestLabeledArrow:
    def test_returns_vgroup_with_two_elements(self):
        result = labeled_arrow(
            np.array([0, 0, 0]),
            np.array([1, 0, 0]),
            "Force",
        )
        assert isinstance(result, VGroup)
        assert len(result) == 2


# ── themes ─────────────────────────────────────────────────────────────────

class TestThemes:
    def test_all_themes_have_required_keys(self):
        required = {"bg", "primary", "secondary", "accent", "highlight",
                     "text", "muted", "success", "error"}
        for name, theme in THEMES.items():
            missing = required - set(theme.keys())
            assert not missing, f"Theme {name!r} missing keys: {missing}"

    def test_apply_theme_returns_dict(self):
        theme = apply_theme("dark_swiss")
        assert isinstance(theme, dict)
        assert theme["bg"] == "#1a1a2e"

    def test_apply_theme_returns_copy(self):
        t1 = apply_theme("dark_swiss")
        t2 = apply_theme("dark_swiss")
        t1["bg"] = "modified"
        assert t2["bg"] == "#1a1a2e"

    def test_unknown_theme_raises(self):
        with pytest.raises(ValueError, match="Unknown theme"):
            apply_theme("nonexistent")


class TestTimingPresets:
    def test_all_presets_have_required_keys(self):
        required = {"fast", "normal", "slow", "pause_short",
                     "pause_medium", "pause_long"}
        for name, preset in TIMING_PRESETS.items():
            missing = required - set(preset.keys())
            assert not missing, f"Preset {name!r} missing keys: {missing}"

    def test_timing_preset_returns_dict(self):
        t = timing_preset("normal")
        assert isinstance(t, dict)
        assert t["fast"] < t["normal"] < t["slow"]

    def test_relaxed_is_slower_than_fast(self):
        relaxed = timing_preset("relaxed")
        fast = timing_preset("fast")
        assert relaxed["normal"] > fast["normal"]

    def test_unknown_preset_raises(self):
        with pytest.raises(ValueError, match="Unknown timing"):
            timing_preset("ludicrous")
