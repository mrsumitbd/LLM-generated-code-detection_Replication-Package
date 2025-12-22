from types import TracebackType, FrameType
from typing import Optional

def get_local_frame(exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType) -> FrameType | None:
    """
    Return the frame where the exception was raised.

    Parameters
    ----------
    exc_type : type[BaseException]
        The exception class.
    exc_value : BaseException
        The exception instance.
    exc_traceback : TracebackType
        The traceback object associated with the exception.

    Returns
    -------
    FrameType | None
        The frame where the exception was raised, or None if no traceback is available.
    """
    # If no traceback is provided, we cannot determine the frame.
    if exc_traceback is None:
        return None

    # Walk to the last traceback entry (the point where the exception was raised).
    tb = exc_traceback
    while tb.tb_next is not None:
        tb = tb.tb_next

    # Return the frame associated with that traceback entry.
    return tb.tb_frame