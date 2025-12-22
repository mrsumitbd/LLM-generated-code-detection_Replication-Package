def get_local_frame(exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType) -> FrameType | None:
    tb = exc_traceback
    while tb is not None:
        if tb.tb_frame.f_code.co_name == '<module>':
            return tb.tb_frame
        tb = tb.tb_next
    return None