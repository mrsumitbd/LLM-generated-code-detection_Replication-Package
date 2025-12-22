def advance_video_slider_by_n_frames(main_window: 'MainWindow', n=30):
    video_processor = main_window.video_processor
    if video_processor.media_capture:
        current_position = int(main_window.videoSeekSlider.value())
        new_position = current_position + n
        if new_position > video_processor.max_frame_number:
            new_position = video_processor.max_frame_number
        main_window.videoSeekSlider.setValue(new_position)
        main_window.video_processor.process_current_frame()