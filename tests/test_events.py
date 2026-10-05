from lyricview.core.engine import LyricEngine
from lyricview.model.lyrics import Song, Section, Line, Word


def test_engine_emits_line_and_word_events():
    song = Song(
        sections=[
            Section(
                lines=[
                    Line(
                        text="Hello world",
                        start=0.0,
                        end=2.0,
                        words=[
                            Word(text="Hello", start=0.0, end=1.0),
                            Word(text="world", start=1.0, end=2.0),
                        ],
                    )
                ]
            )
        ]
    )

    engine = LyricEngine(song=song)
    fired = []
    engine.on("linechange", lambda idx: fired.append(("line", idx)))
    engine.on("wordchange", lambda idx: fired.append(("word", idx)))

    engine.seek(1.5)
    engine.tick()

    assert ("line", 0) in fired
    assert ("word", 1) in fired


def test_engine_emits_structured_progress_event():
    song = Song(
        sections=[
            Section(
                lines=[
                    Line(
                        text="Hello world",
                        start=0.0,
                        end=2.0,
                        words=[
                            Word(text="Hello", start=0.0, end=1.0),
                            Word(text="world", start=1.0, end=2.0),
                        ],
                    )
                ]
            )
        ]
    )

    engine = LyricEngine(song=song)
    progress = []
    engine.on("progress", lambda payload: progress.append(payload))

    engine.seek(1.5)
    engine.tick()

    assert progress
    payload = progress[-1]
    assert payload["current_time"] == 1.5
    assert payload["active_line_index"] == 0
    assert payload["active_word_index"] == 1
