"""Native GUI viewer for LyricView."""

from __future__ import annotations

from pathlib import Path
from typing import List

from .renderers.tk_renderer import TkinterRenderer
from .model.lyrics import Song, Section, Line


def load_lyrics(file_path: str) -> List[Line]:
    path = Path(file_path)
    if not path.exists():
        return [
            Line(text="No lyrics file was found."),
            Line(text="Use --file path/to/your-lyrics.txt"),
            Line(text="or launch the built-in test mode."),
        ]

    raw_lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    filtered = [Line(text=line) for line in raw_lines if line]
    return filtered or [Line(text="The lyric file is empty.")]


class LyricViewerApp:
    def __init__(self, file_path: str, theme: dict, title: str = "LyricView", test_mode: bool = False):
        try:
            import tkinter as tk
        except ImportError as exc:  # pragma: no cover - depends on platform runtime
            raise RuntimeError(
                "Tkinter is required to open the native LyricView window. Install the system package for Tk (for example: python3-tk or tk)."
            ) from exc

        self.tk = tk
        self.root = tk.Tk()
        self.theme = theme
        self.file_path = file_path
        self.test_mode = test_mode
        self.lines = load_lyrics(file_path)
        self.index = 0
        self.scroll_speed = int(theme.get("scroll_speed_ms", 2200))
        self.song = Song(sections=[Section(lines=self.lines)])

        self.root.title(title)
        self.root.configure(bg="#0a0f1d")
        self.root.geometry("980x600")
        self.root.minsize(720, 420)
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        if test_mode:
            self.root.wm_attributes("-topmost", 1)

        self._build_ui()
        self.engine = None
        try:
            from .core.engine import LyricEngine

            self.engine = LyricEngine(song=self.song)
        except Exception:
            self.engine = None

        self.renderer = TkinterRenderer(self.root, theme)
        self.renderer.mount()
        self._debug_overlay = None
        # create debug overlay when in test_mode
        if test_mode:
            try:
                from .ui.debug_overlay import DebugOverlay

                self._debug_overlay = DebugOverlay(self.root)
            except Exception:
                self._debug_overlay = None

        # start legacy animation loop while engine not in use
        self.animate()

    def _build_ui(self) -> None:
        root = self.root
        theme = self.theme
        tk = self.tk

        outer = tk.Frame(root, bg="#0a0f1d", padx=18, pady=18)
        outer.pack(fill="both", expand=True)

        title_bar = tk.Label(
            outer,
            text="LyricView preview",
            fg="#dfe7f5",
            bg="#111827",
            font=(theme.get("font_family", "Segoe UI"), 11, "bold"),
            pady=8,
            padx=14,
            anchor="w",
        )
        title_bar.pack(fill="x", pady=(0, 12))

        display_frame = tk.Frame(outer, bg="#111827", padx=30, pady=24)
        display_frame.pack(fill="both", expand=True)

        # renderer will create widgets
        pass

    def animate(self) -> None:
        if not self.lines:
            return

        # If an engine exists, prefer engine-driven rendering
        if self.engine is not None:
            self.engine.time.play()
            state = self.engine.tick()
            visual = state.get("visual", {})
            # provide lines for renderer convenience
            visual["_lines"] = self.lines
            self.renderer.render(visual)
            # update debug overlay if present
            if self._debug_overlay is not None:
                self._debug_overlay.update(state["time"], visual)
            self.root.after(40, self.animate)
            return

        # Legacy fallback loop (text-only cycling)
        current_index = self.index % len(self.lines)
        previous_index = (current_index - 1) % len(self.lines)
        next_index = (current_index + 1) % len(self.lines)

        current_line = self.lines[current_index].text
        previous_line = self.lines[previous_index].text
        next_line = self.lines[next_index].text

        # update renderer directly
        self.renderer._widgets["previous"].configure(text=previous_line)
        self.renderer._widgets["glow"].configure(text=current_line)
        self.renderer._widgets["primary"].configure(text=current_line)
        self.renderer._widgets["next"].configure(text=next_line)

        self.index += 1
        self.root.after(self.scroll_speed, self.animate)


def launch_app(file_path: str, theme: dict, test_mode: bool = False, title: str = "LyricView") -> None:
    app = LyricViewerApp(file_path=file_path, theme=theme, title=title, test_mode=test_mode)
    app.root.mainloop()
