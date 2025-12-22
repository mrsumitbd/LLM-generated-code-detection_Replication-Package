from types import FrameType, TracebackType

def get_local_frame(exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType) -> FrameType | None:
    LOCAL_FILENAME = "<string>"
    LOCAL_MODULE_DIR = "codegen-backend/app/"
    tb = exc_traceback
    while tb and ((tb.tb_next and tb.tb_frame.f_code.co_filename != LOCAL_FILENAME) or LOCAL_MODULE_DIR in tb.tb_frame.f_code.co_filename):
        tb = tb.tb_next

    frame = tb.tb_frame if tb else None
    return frame