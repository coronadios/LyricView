from lyricview.core.engine import LyricEngine
from lyricview.model.lyrics import Song, Section, Line


def test_engine_line_activation_by_time():
    song = Song(title="T", sections=[Section(lines=[
        Line(text="a", start=0.0, end=1.0),
        Line(text="b", start=1.0, end=2.0),
        Line(text="c", start=2.0, end=3.0),
    ])])

    engine = LyricEngine(song=song)
    engine.seek(0.5)
    res = engine.tick()
    assert res["visual"]["active_line_index"] == 0

    engine.seek(1.5)
    res = engine.tick()
    assert res["visual"]["active_line_index"] == 1
