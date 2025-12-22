def stop_now_work():
    if current_task_thread and current_task_thread.is_alive():
        cancel_event.set()
        current_task_thread.join()