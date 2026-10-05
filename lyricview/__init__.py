"""LyricView package."""

from .accessibility import AccessibilityProfile, build_accessibility_profile, prefers_reduced_motion
from .cli import main
from .core.engine import LyricEngine
from .model.lyrics import Song, Section, Line, Word, Syllable
from .themes import get_theme, resolve_theme_name

__all__ = [
    "main",
    "get_theme",
    "resolve_theme_name",
    "LyricEngine",
    "Song",
    "Section",
    "Line",
    "Word",
    "Syllable",
    "AccessibilityProfile",
    "build_accessibility_profile",
    "prefers_reduced_motion",
]
__version__ = "0.1.0"
