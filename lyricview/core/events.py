"""Simple event emitter for LyricView core."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable, Any


class EventEmitter:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def on(self, event: str, fn: Callable[..., Any]) -> None:
        self._handlers[event].append(fn)

    def off(self, event: str, fn: Callable[..., Any]) -> None:
        if event in self._handlers and fn in self._handlers[event]:
            self._handlers[event].remove(fn)

    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        for fn in list(self._handlers.get(event, [])):
            try:
                fn(*args, **kwargs)
            except Exception:
                # Don't allow handler errors to bubble — consumers should handle their own errors
                pass
