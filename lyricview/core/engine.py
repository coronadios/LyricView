"""Core LyricEngine orchestration.

The engine is responsible for loading a `Song` model, driving the `TimeEngine`,
computing which line/word is active for a given time, and emitting events. The
engine is intentionally renderer-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Callable

from ..model.lyrics import Song
from ..parsers.registry import ParserRegistry, register_default_parsers
from ..plugins import PluginManager
from .time import TimeEngine
from .events import EventEmitter


@dataclass(frozen=True)
class ProgressPayload:
    current_time: float
    active_line_index: int | None
    active_word_index: int | None
    playback_rate: float
    playing: bool


class LyricEngine:
    def __init__(self, song: Song | None = None, now_fn: Callable[[], float] | None = None) -> None:
        self.song = song
        self.time = TimeEngine(now_fn=now_fn)
        self.events = EventEmitter()
        self.plugin_manager = PluginManager()
        self.parser_registry = register_default_parsers(ParserRegistry())
        self._last_active_line_index: int | None = None
        self._last_active_word_index: int | None = None

    def on(self, event: str, callback):
        self.events.on(event, callback)

    def off(self, event: str, callback):
        self.events.off(event, callback)

    def register_parser(self, name: str, parser) -> None:
        self.parser_registry.register(name, parser)

    def parse(self, source, parser_name: str | None = None) -> Song:
        song = self.parser_registry.parse(source, parser_name=parser_name)
        self.load_song(song)
        return song

    def use(self, plugin, *args, **kwargs):
        return self.plugin_manager.use(plugin, *args, **kwargs)

    def load_song(self, song: Song) -> None:
        self.song = song
        if song.duration is not None:
            self.time.state.duration = song.duration
        self.events.emit("ready", song)

    def play(self) -> None:
        self.time.play()
        self.events.emit("play")

    def pause(self) -> None:
        self.time.pause()
        self.events.emit("pause")

    def seek(self, t: float) -> None:
        self.time.seek(t)
        self.events.emit("seek", t)

    def tick(self) -> dict:
        state = self.time.tick()
        current_time = state.current_time
        visual = self._compute_visual_state(current_time)
        payload = ProgressPayload(
            current_time=current_time,
            active_line_index=visual.get("active_line_index"),
            active_word_index=visual.get("active_word_index"),
            playback_rate=state.playback_rate,
            playing=state.playing,
        )
        self.events.emit("tick", state, visual)
        self.events.emit("progress", payload.__dict__)
        return {"time": state, "visual": visual, "progress": payload.__dict__}

    def _compute_visual_state(self, current_time: float) -> dict:
        # Basic implementation: find active line by line.start <= time < line.end
        active_index = None
        lines = self.song.lines if self.song else []
        for idx, line in enumerate(lines):
            if line.start is not None and line.end is not None:
                if line.start <= current_time < line.end:
                    active_index = idx
                    break
        # Fallback: nearest line whose start <= current_time
        if active_index is None:
            last = None
            for idx, line in enumerate(lines):
                if line.start is not None and line.start <= current_time:
                    last = idx
            active_index = last

        active_word_index = None
        if active_index is not None and active_index < len(lines):
            line = lines[active_index]
            words = line.words
            for idx, word in enumerate(words):
                if word.start is not None and word.end is not None:
                    if word.start <= current_time < word.end:
                        active_word_index = idx
                        break
            if active_word_index is None and words:
                last_word = None
                for idx, word in enumerate(words):
                    if word.start is not None and word.start <= current_time:
                        last_word = idx
                active_word_index = last_word

        if active_index != self._last_active_line_index:
            self.events.emit("linechange", active_index)
            self._last_active_line_index = active_index

        if active_word_index != self._last_active_word_index:
            self.events.emit("wordchange", active_word_index)
            self._last_active_word_index = active_word_index

        return {
            "active_line_index": active_index,
            "active_word_index": active_word_index,
            "lines_count": len(lines),
            "current_time": current_time,
        }
