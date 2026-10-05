"""Tkinter renderer adaptor for LyricEngine visual state.

Provides a renderer that mounts into a Tk root and renders a small
previous/current/next lyric layout. The renderer is intentionally
minimal — it's a reference backend for the engine.
"""

from __future__ import annotations

from typing import Any

from ..accessibility import build_accessibility_profile


class TkinterRenderer:
    def __init__(self, root, theme: dict[str, Any]) -> None:
        self.root = root
        self.theme = theme
        self.accessibility = build_accessibility_profile(theme)
        self._widgets = {}
        self.display_frame = None
        self._last_time: float | None = None
        try:
            from ..motion.scroll_controller import ScrollController

            self._scroll = ScrollController()
        except Exception:
            self._scroll = None

    def mount(self) -> None:
        tk = __import__("tkinter")
        outer = tk.Frame(self.root, bg=self.theme.get("panel", "#0f172a"), padx=18, pady=18)
        outer.pack(fill="both", expand=True)

        title_bar = tk.Label(
            outer,
            text="LyricView preview",
            fg=self.theme.get("current_text_color", "#dfe7f5"),
            bg=self.theme.get("surface", "#111827"),
            font=(self.theme.get("font_family", "Segoe UI"), 11, "bold"),
            pady=8,
            padx=14,
            anchor="w",
        )
        title_bar.pack(fill="x", pady=(0, 12))

        display_frame = tk.Frame(outer, bg=self.theme.get("surface", "#111827"), padx=30, pady=24)
        display_frame.pack(fill="both", expand=True)
        self.display_frame = display_frame

        self._widgets["previous"] = tk.Label(
            display_frame,
            text="",
            fg=self.theme.get("previous_text_color", "#dfe7f5"),
            bg=self.theme.get("surface", "#111827"),
            justify="center",
            wraplength=760,
            font=(self.theme.get("font_family", "Segoe UI"), int(self.theme.get("font_size", 32)) - 4, "bold"),
        )
        self._widgets["previous"].place(relx=0.5, rely=0.2, anchor="center")

        self._widgets["glow"] = tk.Label(
            display_frame,
            text="",
            fg=self.theme.get("glow_color", "#ffffff"),
            bg=self.theme.get("surface", "#111827"),
            justify="center",
            wraplength=760,
            font=(self.theme.get("font_family", "Segoe UI"), int(self.theme.get("font_size", 32)), "bold"),
        )
        self._widgets["glow"].place(relx=0.5, rely=0.5, anchor="center", x=2, y=2)

        self._widgets["primary"] = tk.Label(
            display_frame,
            text="",
            fg=self.theme.get("current_text_color", "#ffffff"),
            bg=self.theme.get("surface", "#111827"),
            justify="center",
            wraplength=760,
            font=(self.theme.get("font_family", "Segoe UI"), int(self.theme.get("font_size", 32)), "bold"),
        )
        self._widgets["primary"].place(relx=0.5, rely=0.5, anchor="center")

        self._widgets["next"] = tk.Label(
            display_frame,
            text="",
            fg=self.theme.get("next_text_color", "#dfe7f5"),
            bg=self.theme.get("surface", "#111827"),
            justify="center",
            wraplength=760,
            font=(self.theme.get("font_family", "Segoe UI"), int(self.theme.get("font_size", 32)) - 4, "bold"),
        )
        self._widgets["next"].place(relx=0.5, rely=0.8, anchor="center")

    def render(self, visual_state: dict) -> None:
        # visual_state expected keys: active_line_index, lines_count, current_time
        active = visual_state.get("active_line_index")
        lines = visual_state.get("_lines", [])
        current_time = visual_state.get("current_time", 0.0)

        # compute delta time for integration
        dt = 0.04
        if self._last_time is not None:
            dt = max(1e-6, current_time - self._last_time)
        self._last_time = current_time

        # optionally apply simple motion primitive to highlight active line
        try:
            from ..motion.primitives import interpolate, ease_in_out_cubic
        except Exception:
            interpolate = None
            ease_in_out_cubic = None

        prev_text = ""
        curr_text = ""
        next_text = ""

        if lines:
            if active is None:
                # No timing info — show first three
                prev_text = lines[0].text if len(lines) > 0 else ""
                curr_text = lines[0].text if len(lines) > 0 else ""
                next_text = lines[1].text if len(lines) > 1 else ""
            else:
                prev_text = lines[active - 1].text if active - 1 >= 0 else ""
                curr_text = lines[active].text if 0 <= active < len(lines) else ""
                next_text = lines[active + 1].text if active + 1 < len(lines) else ""

        self._widgets["previous"].configure(text=prev_text)
        self._widgets["glow"].configure(text=curr_text)
        self._widgets["primary"].configure(text=curr_text)
        self._widgets["next"].configure(text=next_text)

        # set subtle scale/opacity simulation via font size tweak (cheap)
        if not self.accessibility.reduced_motion and interpolate is not None and active is not None:
            # compute a pseudo-progress inside the line duration if available
            active_line = lines[active] if 0 <= active < len(lines) else None
            progress = 0.0
            if active_line and getattr(active_line, "start", None) is not None and getattr(active_line, "end", None) is not None:
                span = max(1e-6, active_line.end - active_line.start)
                progress = max(0.0, min(1.0, (current_time - active_line.start) / span))

            scale = interpolate(0.96, 1.0, progress, ease_in_out_cubic)
            base_size = int(self.theme.get("font_size", 32))
            size = max(10, int(base_size * scale))
            self._widgets["primary"].configure(font=(self.theme.get("font_family", "Segoe UI"), size, "bold"))

        # Smooth auto-scroll: use ScrollController to chase index positions
        if self._scroll is not None and not self.accessibility.reduced_motion:
            try:
                target = float(active) if active is not None else 0.0
            except Exception:
                target = 0.0

            pos = self._scroll.step(target, dt)

            # compute pixel positions relative to display_frame center
            frame = self.display_frame
            fw = frame.winfo_width() or 800
            fh = frame.winfo_height() or 400
            center_x = int(fw / 2)
            center_y = int(fh / 2)
            v_offset = int(self.theme.get("vertical_offset", 34))

            # indices for widgets
            indices = {
                "previous": (active - 1) if active is not None else 0,
                "primary": active if active is not None else 0,
                "next": (active + 1) if active is not None else 1,
            }

            for key, idx in indices.items():
                try:
                    idxf = float(idx)
                except Exception:
                    idxf = 0.0
                y = center_y + int((idxf - pos) * v_offset)
                w = self._widgets.get(key)
                if w:
                    # place using absolute coords to avoid jumping with relx
                    w.place_configure(x=center_x, y=y)
