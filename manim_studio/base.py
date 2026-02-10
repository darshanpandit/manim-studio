"""Base scene classes that eliminate per-scene boilerplate.

Usage:
    from manim_studio import NarratedScene

    class MyScene(NarratedScene):
        background_color = "#1a1a2e"  # optional override
        speech_service = "gtts"       # optional override

        def construct(self):
            # Just your unique content — setup and teardown are automatic.
            with self.voiceover(text="Hello world.") as tracker:
                self.play(Create(Circle()))
"""

from __future__ import annotations

from manim import *
from manim_voiceover import VoiceoverScene


def _make_speech_service(name: str):
    """Resolve a speech service name to an instance."""
    name = name.lower()
    if name == "gtts":
        from manim_voiceover.services.gtts import GTTSService
        return GTTSService()
    if name == "elevenlabs":
        from manim_voiceover.services.elevenlabs import ElevenLabsService
        return ElevenLabsService()
    if name == "azure":
        from manim_voiceover.services.azure import AzureSpeechService
        return AzureSpeechService()
    if name == "recorder":
        from manim_voiceover.services.recorder import RecorderService
        return RecorderService()
    raise ValueError(
        f"Unknown speech service {name!r}. "
        f"Supported: gtts, elevenlabs, azure, recorder"
    )


class NarratedScene(VoiceoverScene, Scene):
    """Base scene with automatic TTS setup, background color, and fade-out.

    Class attributes (override in subclass or per-project):
        background_color: Hex color string for camera background.
        speech_service: Name of TTS backend ("gtts", "elevenlabs", "azure", "recorder").
        auto_fade_out: If True, fade out all mobjects after construct() finishes.
    """

    background_color: str = "#1a1a2e"
    speech_service: str = "gtts"
    auto_fade_out: bool = True

    def setup(self):
        super().setup()
        self.set_speech_service(_make_speech_service(self.speech_service))
        self.camera.background_color = self.background_color

    def tear_down(self):
        if self.auto_fade_out and self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        super().tear_down()


class NarratedMovingCameraScene(VoiceoverScene, MovingCameraScene):
    """Same as NarratedScene but with MovingCameraScene for zoom/pan."""

    background_color: str = "#1a1a2e"
    speech_service: str = "gtts"
    auto_fade_out: bool = True

    def setup(self):
        super().setup()
        self.set_speech_service(_make_speech_service(self.speech_service))
        self.camera.background_color = self.background_color

    def tear_down(self):
        if self.auto_fade_out and self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        super().tear_down()
