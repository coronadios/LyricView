"""Accessibility helpers for LyricView."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AccessibilityProfile:
    reduced_motion: bool = False
    high_contrast: bool = False
    keyboard_navigation: bool = True


def prefers_reduced_motion(env: dict[str, str] | None = None) -> bool:
    """Return True when reduced motion should be respected.

    Honors the `LYRICVIEW_REDUCED_MOTION` environment variable and an explicit
    `prefers-reduced-motion` media query-style value when passed in a mapping.
    """
    values = os.environ if env is None else env
    if "LYRICVIEW_REDUCED_MOTION" in values:
        return str(values["LYRICVIEW_REDUCED_MOTION"]).strip().lower() in {"1", "true", "yes", "on"}
    if "prefers-reduced-motion" in values:
        return str(values["prefers-reduced-motion"]).strip().lower() in {"1", "true", "yes", "on"}
    return False


def build_accessibility_profile(preferences: dict[str, object] | None = None) -> AccessibilityProfile:
    settings = preferences or {}
    reduced_motion = bool(settings.get("reduced_motion", prefers_reduced_motion()))
    high_contrast = bool(settings.get("high_contrast", False))
    keyboard_navigation = bool(settings.get("keyboard_navigation", True))
    return AccessibilityProfile(
        reduced_motion=reduced_motion,
        high_contrast=high_contrast,
        keyboard_navigation=keyboard_navigation,
    )
