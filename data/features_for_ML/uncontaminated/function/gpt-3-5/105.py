def advance_video_slider_by_n_frames(main_window: 'MainWindow', n=30):
    main_window.video_slider.setValue(main_window.video_slider.value() + n)