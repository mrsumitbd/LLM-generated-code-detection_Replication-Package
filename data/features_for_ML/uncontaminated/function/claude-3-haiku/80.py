def extract_exception_chain(exception: Exception) -> List[str]:
    """
    Extract the full exception chain for detailed error reporting.

    Args:
        exception: The exception to extract the chain from

    Returns:
        List of exception messages in the chain, from most specific to root cause
    """
    exception_chain = []
    current_exception = exception

    while current_exception:
        exception_chain.append(str(current_exception))
        current_exception = current_exception.__cause__ or current_exception.__context__

    return exception_chain