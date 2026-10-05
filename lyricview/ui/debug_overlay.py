"""Simple debug overlay UI to display engine state for development."""

from __future__ import annotations

from typing import Any


class DebugOverlay:
    def __init__(self, root, x: int = 12, y: int = 12) -> None:
        tk = __import__("tkinter")
        self.frame = tk.Frame(root, bg="#000000", padx=8, pady=6)
        self.frame.place(x=x, y=y)
        self.labels = {}
        for key in ("time", "active_line", "playback_rate", "lines_count"):
            lbl = tk.Label(self.frame, text=f"{key}: -", fg="#ffffff", bg="#000000", anchor="w")
            lbl.pack(fill="x")
            self.labels[key] = lbl

    def update(self, time_state: Any, visual: dict[str, Any]) -> None:
        self.labels["time"].configure(text=f"time: {time_state.current_time:.2f}")
        self.labels["active_line"].configure(text=f"active_line: {visual.get('active_line_index')}")
        self.labels["playback_rate"].configure(text=f"playback_rate: {time_state.playback_rate}")
        self.labels["lines_count"].configure(text=f"lines: {visual.get('lines_count')}")
