def get_local_frame(exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType) -> FrameType | None:
    if exc_traceback is None:
        return None
    
    frame = exc_traceback.tb_frame
    while frame.f_back:
        frame = frame.f_back
    
    return frame