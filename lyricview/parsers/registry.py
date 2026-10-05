"""Parser registry for different lyric sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from ..model.lyrics import Song, Section, Line, Word


class ParserRegistry:
    def __init__(self) -> None:
        self._parsers: dict[str, Callable[[Any], Song]] = {}

    def register(self, name: str, parser: Callable[[Any], Song]) -> None:
        self._parsers[name.lower()] = parser

    def get(self, name: str) -> Callable[[Any], Song]:
        key = name.lower()
        if key not in self._parsers:
            raise KeyError(f"Parser '{name}' is not registered")
        return self._parsers[key]

    def parse(self, source: Any, parser_name: str | None = None) -> Song:
        if parser_name:
            return self.get(parser_name)(source)
        for candidate in ("lrc", "json", "plain"):
            if candidate in self._parsers:
                return self._parsers[candidate](source)
        raise ValueError("No parser registered to parse the source")


def parse_plain_text(source: str | Path) -> Song:
    if isinstance(source, Path):
        text = source.read_text(encoding="utf-8")
    else:
        text = str(source)

    lines = [Line(text=line.strip()) for line in text.splitlines() if line.strip()]
    return Song(title="Plain text lyrics", sections=[Section(lines=lines)])


def _parse_lrc_line(raw: str) -> tuple[float, float, str]:
    if "[" not in raw or "]" not in raw:
        raise ValueError(f"Malformed LRC entry: {raw!r}")
    tag, text = raw.split("]", 1)
    value = tag[1:]
    minute, second = value.split(":", 1)
    start = int(minute) * 60 + float(second)
    return start, start + 1.0, text.strip()


def parse_lrc(source: str | Path) -> Song:
    if isinstance(source, Path):
        text = source.read_text(encoding="utf-8")
    else:
        text = str(source)

    lines: list[Line] = []
    for entry in text.splitlines():
        cleaned = entry.strip()
        if not cleaned or not cleaned.startswith("["):
            continue
        try:
            start, end, lyric_text = _parse_lrc_line(cleaned)
            lines.append(Line(text=lyric_text, start=start, end=end))
        except ValueError:
            # treat malformed entries as plain text fallback line
            if cleaned:
                lines.append(Line(text=cleaned))

    if not lines:
        return parse_plain_text(text)
    return Song(title="LRC lyrics", sections=[Section(lines=lines)])


def parse_json(source: str | dict | Path) -> Song:
    if isinstance(source, Path):
        payload = json.loads(source.read_text(encoding="utf-8"))
    elif isinstance(source, str):
        payload = json.loads(source)
    else:
        payload = source

    lines = []
    for item in payload.get("lines", []):
        words = []
        for word_item in item.get("words", []):
            words.append(
                Word(
                    text=str(word_item.get("text", "")),
                    start=word_item.get("start"),
                    end=word_item.get("end"),
                )
            )
        lines.append(
            Line(
                text=item.get("text", ""),
                start=item.get("start"),
                end=item.get("end"),
                words=words,
            )
        )

    return Song(title=payload.get("title"), sections=[Section(lines=lines)])


def register_default_parsers(registry: ParserRegistry) -> ParserRegistry:
    registry.register("plain", parse_plain_text)
    registry.register("lrc", parse_lrc)
    registry.register("json", parse_json)
    return registry
