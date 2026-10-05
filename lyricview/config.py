"""Read configuration from a local .env file."""

from __future__ import annotations

from pathlib import Path


def load_env(path: str = ".env") -> dict[str, str]:
    env_path = Path(path)
    values: dict[str, str] = {}

    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        if not key:
            continue
        if value and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values


def get_runtime_config(env_path: str = ".env") -> dict[str, str]:
    env_values = load_env(env_path)
    return {
        "theme": env_values.get("LYRICVIEW_THEME", "minimal"),
        "file": env_values.get("LYRICVIEW_FILE", "lyric-test.txt"),
        "window_title": env_values.get("LYRICVIEW_WINDOW_TITLE", "LyricView"),
        "show_title": env_values.get("LYRICVIEW_SHOW_TITLE", "true").lower() == "true",
        "font_size": env_values.get("LYRICVIEW_FONT_SIZE", "30"),
    }
