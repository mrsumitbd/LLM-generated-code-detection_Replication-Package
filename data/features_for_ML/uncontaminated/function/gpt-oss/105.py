def advance_video_slider_by_n_frames(main_window: 'MainWindow', n=30):
    """
    Advance the video slider by `n` frames, clamping to the slider's maximum.
    If the main window has a video player, also update its position.
    """
    # Try to get the slider widget
    slider = getattr(main_window, "video_slider", None)
    if slider is None:
        return

    # Current position and maximum
    try:
        current = slider.value()
        maximum = slider.maximum()
    except Exception:
        return

    # Compute new position
    new_pos = current + n
    if new_pos > maximum:
        new_pos = maximum
    if new_pos < 0:
        new_pos = 0

    # Set the slider to the new position
    try:
        slider.setValue(new_pos)
    except Exception:
        pass

    # If a video player exists, sync its position
    video_player = getattr(main_window, "video_player", None)
    if video_player is not None:
        try:
            # Some players use milliseconds; assume slider units match
            video_player.setPosition(new_pos)
        except Exception:
            pass

    # Optional: refresh the UI if needed
    if hasattr(main_window, "update"):
        try:
            main_window.update()
        except Exception:
            pass