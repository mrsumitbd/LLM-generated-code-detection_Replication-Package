def advance_video_slider_by_n_frames(main_window: 'MainWindow', n=30):
    """Advance the video slider by n frames."""
    if not hasattr(main_window, 'video_slider') or main_window.video_slider is None:
        return
    
    current_value = main_window.video_slider.value()
    maximum_value = main_window.video_slider.maximum()
    new_value = min(current_value + n, maximum_value)
    main_window.video_slider.setValue(new_value)