"""Command-line entry point for LyricView."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .app import launch_app
from .config import get_runtime_config
from .themes import get_theme, resolve_theme_name as resolve_theme_name_from_config


def _normalize_theme_flags(argv: list[str]) -> list[str]:
    normalized: list[str] = []
    for argument in argv:
        if argument.startswith("--theme:"):
            normalized.extend(["--theme", argument.split(":", 1)[1]])
        elif argument.startswith("--theme="):
            normalized.extend(["--theme", argument.split("=", 1)[1]])
        else:
            normalized.append(argument)
    return normalized


class LyricViewParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        raw_args = list(sys.argv[1:] if args is None else args)
        normalized = _normalize_theme_flags(raw_args)
        return super().parse_args(normalized, namespace=namespace)


def build_parser() -> argparse.ArgumentParser:
    parser = LyricViewParser(
        prog="lv",
        description="Open-source lyric viewer for music players, web apps, and custom experiences.",
    )
    parser.add_argument(
        "-test",
        "--test",
        action="store_true",
        help="Open the viewer in demo/test mode without hiding the native interface.",
    )
    parser.add_argument(
        "--file",
        default="",
        help="Path to the lyric text file to display. Defaults to a demo lyric file when not provided.",
    )
    parser.add_argument(
        "--theme",
        "--theme:",
        dest="theme",
        default=None,
        help="Select a built-in style like minimal, aurora, sunset, midnight, deep, or glass.",
    )
    return parser


def resolve_theme_name(theme_name: str | None) -> str:
    return resolve_theme_name_from_config(theme_name)


def main(argv: list[str] | None = None) -> int:
    raw_args = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(_normalize_theme_flags(raw_args))

    config = get_runtime_config()
    selected_theme = args.theme or config.get("theme") or "minimal"
    theme_name = resolve_theme_name(selected_theme)
    theme = get_theme(theme_name)

    file_path = args.file or config.get("file") or "lyric-test.txt"
    if not Path(file_path).exists():
        file_path = "lyric-test.txt"

    launch_app(
        file_path=file_path,
        theme=theme,
        test_mode=args.test,
        title=config.get("window_title", "LyricView"),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
