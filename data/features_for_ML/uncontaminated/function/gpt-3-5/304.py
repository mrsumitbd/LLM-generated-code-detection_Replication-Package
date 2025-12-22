def _get_exception_context(exc_type: type[BaseException], exc_value: BaseException, tb: Any) -> dict[str, Any]:
    return {
        'exception_type': exc_type.__name__,
        'exception_message': str(exc_value),
        'traceback': ''.join(traceback.format_tb(tb))
    }