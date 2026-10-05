"""Motion primitives and easing functions for LyricView.

Provides interpolation helpers used by animation definitions.
"""

from __future__ import annotations

from typing import Callable
import math


def clamp(v: float, a: float = 0.0, b: float = 1.0) -> float:
    return max(a, min(b, v))


def linear(t: float) -> float:
    return clamp(t)


def ease_in_out_cubic(t: float) -> float:
    t = clamp(t)
    if t < 0.5:
        return 4 * t * t * t
    f = (2 * t) - 2
    return 0.5 * f * f * f + 1


def spring(t: float, mass: float = 1.0, stiffness: float = 100.0, damping: float = 10.0) -> float:
    # Very small, cheap spring-like easing approximation
    t = clamp(t)
    return 1 - math.exp(-damping * t) * math.cos(math.sqrt(max(0.0, stiffness / mass)) * t)


def interpolate(a: float, b: float, t: float, easing: Callable[[float], float] | None = None) -> float:
    if easing is None:
        easing = linear
    return a + (b - a) * easing(clamp(t))
