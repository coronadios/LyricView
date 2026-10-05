from lyricview.motion.primitives import interpolate, ease_in_out_cubic
from lyricview.motion.scroll_controller import ScrollController


def test_interpolate_eases():
    assert abs(interpolate(0, 10, 0.0) - 0.0) < 1e-6
    assert abs(interpolate(0, 10, 1.0) - 10.0) < 1e-6
    mid = interpolate(0, 10, 0.5, ease_in_out_cubic)
    assert 0.0 < mid < 10.0


def test_scroll_controller_steps_towards_target():
    ctl = ScrollController(position=0.0, velocity=0.0, stiffness=50.0, damping=8.0)
    target = 100.0
    pos = ctl.step(target, 0.016)
    assert pos != 0.0
