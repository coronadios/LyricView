from lyricview.parsers.registry import parse_lrc, parse_plain_text


def test_parse_plain_text_falls_back_to_lines():
    song = parse_plain_text("hello\nworld\n")
    assert len(song.lines) == 2
    assert song.lines[0].text == "hello"


def test_parse_lrc_reads_minimal_timestamps():
    song = parse_lrc("[00:01.00]Hello\n[00:02.00]World")
    assert len(song.lines) == 2
    assert song.lines[0].start == 1.0
    assert song.lines[0].text == "Hello"
