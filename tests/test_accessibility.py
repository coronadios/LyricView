from lyricview.accessibility import AccessibilityProfile, build_accessibility_profile, prefers_reduced_motion


def test_prefers_reduced_motion_honors_environment():
    assert prefers_reduced_motion({"LYRICVIEW_REDUCED_MOTION": "true"}) is True
    assert prefers_reduced_motion({"prefers-reduced-motion": "1"}) is True
    assert prefers_reduced_motion({"LYRICVIEW_REDUCED_MOTION": "false"}) is False


def test_build_accessibility_profile_defaults():
    profile = build_accessibility_profile({"reduced_motion": True, "high_contrast": True})
    assert isinstance(profile, AccessibilityProfile)
    assert profile.reduced_motion is True
    assert profile.high_contrast is True
    assert profile.keyboard_navigation is True
