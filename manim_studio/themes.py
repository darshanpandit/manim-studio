"""Color and timing presets for consistent visual style.

Usage:
    from manim_studio import apply_theme, timing_preset

    theme = apply_theme("dark_swiss")
    # theme["bg"], theme["primary"], theme["text"], etc.

    timing = timing_preset("relaxed")
    # timing["fast"], timing["normal"], timing["slow"], timing["pause_short"], etc.
"""

from __future__ import annotations


THEMES: dict[str, dict[str, str]] = {
    "dark_swiss": {
        "bg": "#1a1a2e",
        "primary": "#e63946",       # Swiss red
        "secondary": "#457b9d",     # Royal blue
        "accent": "#f4a261",        # Gold
        "highlight": "#f4a261",     # Same as accent
        "text": "#edf2f4",          # Off-white
        "muted": "#8d99ae",         # Slate
        "success": "#2a9d8f",       # Teal
        "error": "#e63946",         # Red
    },
    "3b1b_classic": {
        "bg": "#1c1c1c",
        "primary": "#58C4DD",       # Blue
        "secondary": "#83C167",     # Green
        "accent": "#FFFF00",        # Yellow
        "highlight": "#FF8C00",     # Orange
        "text": "#FFFFFF",
        "muted": "#888888",
        "success": "#83C167",
        "error": "#FC6255",         # Red
    },
    "light": {
        "bg": "#fafafa",
        "primary": "#2d3436",       # Dark grey
        "secondary": "#0984e3",     # Blue
        "accent": "#fdcb6e",        # Yellow
        "highlight": "#e17055",     # Orange-red
        "text": "#2d3436",
        "muted": "#b2bec3",
        "success": "#00b894",       # Green
        "error": "#d63031",         # Red
    },
    "nord": {
        "bg": "#2e3440",
        "primary": "#88c0d0",       # Frost blue
        "secondary": "#81a1c1",     # Lighter blue
        "accent": "#ebcb8b",        # Yellow
        "highlight": "#d08770",     # Orange
        "text": "#eceff4",          # Snow white
        "muted": "#4c566a",         # Polar night
        "success": "#a3be8c",       # Green
        "error": "#bf616a",         # Red
    },
}

TIMING_PRESETS: dict[str, dict[str, float]] = {
    "relaxed": {
        "fast": 0.6,
        "normal": 1.2,
        "slow": 2.5,
        "pause_short": 0.8,
        "pause_medium": 1.5,
        "pause_long": 3.0,
    },
    "normal": {
        "fast": 0.4,
        "normal": 0.8,
        "slow": 1.8,
        "pause_short": 0.5,
        "pause_medium": 1.0,
        "pause_long": 2.0,
    },
    "fast": {
        "fast": 0.25,
        "normal": 0.5,
        "slow": 1.0,
        "pause_short": 0.3,
        "pause_medium": 0.6,
        "pause_long": 1.0,
    },
}


def apply_theme(name: str) -> dict[str, str]:
    """Load a named color theme.

    Args:
        name: One of "dark_swiss", "3b1b_classic", "light", "nord".

    Returns:
        Dictionary with keys: bg, primary, secondary, accent, highlight,
        text, muted, success, error.
    """
    if name not in THEMES:
        available = ", ".join(sorted(THEMES))
        raise ValueError(f"Unknown theme {name!r}. Available: {available}")
    return dict(THEMES[name])


def timing_preset(pace: str = "normal") -> dict[str, float]:
    """Load a timing preset.

    Args:
        pace: One of "relaxed", "normal", "fast".

    Returns:
        Dictionary with keys: fast, normal, slow, pause_short,
        pause_medium, pause_long.
    """
    if pace not in TIMING_PRESETS:
        available = ", ".join(sorted(TIMING_PRESETS))
        raise ValueError(f"Unknown timing preset {pace!r}. Available: {available}")
    return dict(TIMING_PRESETS[pace])
