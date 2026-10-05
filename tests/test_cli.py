from lyricview.cli import build_parser, resolve_theme_name
from lyricview.themes import get_theme


def test_parser_supports_test_file_and_theme():
    parser = build_parser()
    args = parser.parse_args(["-test", "--file", "lyric-test.txt", "--theme:aurora"])

    assert args.test is True
    assert args.file == "lyric-test.txt"
    assert args.theme == "aurora"


def test_default_theme_is_minimal():
    assert resolve_theme_name("minimal") == "minimal"


def test_theme_controls_text_behavior():
    theme = get_theme("aurora")
    assert "current_text_color" in theme
    assert "previous_text_color" in theme
    assert "next_text_color" in theme
    assert "glow_color" in theme
    assert "scroll_speed_ms" in theme
    assert "font_family" in theme
