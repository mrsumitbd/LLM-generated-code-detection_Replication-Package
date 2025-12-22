def advance_video_slider_by_n_frames(main_window: 'MainWindow', n=30):
    current_frame = main_window.video_slider.value()
    new_frame = current_frame + n
    main_window.video_slider.setValue(new_frame)
    main_window.update_video_frame(new_frame)