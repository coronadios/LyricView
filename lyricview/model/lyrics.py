"""Lyric data models: Song, Section, Line, Word, Syllable.

Lightweight, immutable-ish dataclasses that represent hierarchical lyric timing.
The model supports partial timing information: lines may have timestamps, or
words may have timestamps; the consumer must handle fallbacks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Syllable:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None


@dataclass
class Word:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    syllables: List[Syllable] = field(default_factory=list)


@dataclass
class Line:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    words: List[Word] = field(default_factory=list)

    def word_progress(self, word_index: int, current_time: float) -> float:
        if not self.words:
            return 0.0
        if word_index < 0 or word_index >= len(self.words):
            return 0.0
        w = self.words[word_index]
        if w.start is None or w.end is None:
            return 0.0
        span = max(1e-6, w.end - w.start)
        return max(0.0, min(1.0, (current_time - w.start) / span))


@dataclass
class Section:
    title: Optional[str] = None
    lines: List[Line] = field(default_factory=list)


@dataclass
class Song:
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[float] = None
    sections: List[Section] = field(default_factory=list)

    @property
    def lines(self) -> List[Line]:
        out: List[Line] = []
        for s in self.sections:
            out.extend(s.lines)
        return out
