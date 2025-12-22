def _get_exception_context(exc_type: type[BaseException], exc_value: BaseException, tb: Any) -> dict[str, Any]:
    """Extract relevant context from an exception for logging.

    Args:
        exc_type: The exception type
        exc_value: The exception instance
        tb: The traceback object

    Returns:
        Dictionary with exception context for structured logging
    """
    import traceback
    import linecache
    
    context = {
        "exception_type": exc_type.__name__,
        "exception_module": exc_type.__module__,
        "exception_message": str(exc_value),
        "exception_repr": repr(exc_value),
    }
    
    if tb is not None:
        tb_list = traceback.extract_tb(tb)
        frames = []
        
        for frame_summary in tb_list:
            frame_info = {
                "filename": frame_summary.filename,
                "lineno": frame_summary.lineno,
                "name": frame_summary.name,
                "line": frame_summary.line,
            }
            frames.append(frame_info)
        
        context["traceback_frames"] = frames
        
        if tb_list:
            last_frame = tb_list[-1]
            context["last_frame"] = {
                "filename": last_frame.filename,
                "lineno": last_frame.lineno,
                "name": last_frame.name,
                "line": last_frame.line,
            }
    
    if hasattr(exc_value, "__cause__") and exc_value.__cause__ is not None:
        context["cause"] = str(exc_value.__cause__)
    
    if hasattr(exc_value, "__context__") and exc_value.__context__ is not None:
        context["context"] = str(exc_value.__context__)
    
    return context