from lyricview.core.time import TimeEngine


def test_time_engine_seek_and_playback_rate():
    engine = TimeEngine(now_fn=lambda: 10.0)
    engine.state.duration = 30.0
    engine.seek(5.0)
    assert engine.state.current_time == 5.0

    engine.play()
    engine.state.playback_rate = 2.0
    engine._last_wall = 10.0
    engine._sync()
    assert engine.state.current_time >= 5.0


def test_time_engine_pause_stops_updates():
    engine = TimeEngine(now_fn=lambda: 0.0)
    engine.play()
    engine.state.current_time = 1.5
    engine.pause()
    assert engine.state.playing is False
    assert engine.state.current_time == 1.5
