"""Time engine for LyricView.

Provides a deterministic update loop which can be driven by a real clock or a
mocked clock for tests. It exposes a `tick()` method that computes a corrected
currentTime taking playback rate and drift into account.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class TimeState:
    current_time: float = 0.0
    duration: float | None = None
    playback_rate: float = 1.0
    playing: bool = False


class TimeEngine:
    def __init__(self, now_fn: Callable[[], float] | None = None) -> None:
        self.now = now_fn or time.monotonic
        self._last_wall: float | None = None
        self.state = TimeState()

    def play(self) -> None:
        if not self.state.playing:
            self.state.playing = True
            self._last_wall = self.now()

    def pause(self) -> None:
        if self.state.playing:
            self._sync()
            self.state.playing = False
            self._last_wall = None

    def seek(self, t: float) -> None:
        self.state.current_time = float(max(0.0, t))
        self._last_wall = self.now() if self.state.playing else None

    def set_playback_rate(self, rate: float) -> None:
        self._sync()
        self.state.playback_rate = float(rate)

    def _sync(self) -> None:
        if self.state.playing and self._last_wall is not None:
            wall = self.now()
            elapsed = wall - self._last_wall
            self.state.current_time += elapsed * self.state.playback_rate
            self._last_wall = wall

    def tick(self) -> TimeState:
        self._sync()
        return self.state
