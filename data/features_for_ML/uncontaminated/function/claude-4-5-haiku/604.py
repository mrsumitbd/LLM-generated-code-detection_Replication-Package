from types import TracebackType, FrameType

def get_local_frame(exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType) -> FrameType | None:
    if exc_traceback is None:
        return None
    
    frame = exc_traceback.tb_frame
    
    while frame is not None:
        if frame.f_back is None:
            return frame
        frame = frame.f_back
    
    return exc_traceback.tb_frame