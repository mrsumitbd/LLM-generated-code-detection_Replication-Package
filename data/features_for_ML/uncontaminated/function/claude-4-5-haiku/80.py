def extract_exception_chain(exception: Exception) -> List[str]:
    """
    Extract the full exception chain for detailed error reporting.

    Args:
        exception: The exception to extract the chain from

    Returns:
        List of exception messages in the chain, from most specific to root cause
    """
    chain = []
    current = exception
    
    while current is not None:
        chain.append(str(current))
        current = current.__cause__ or current.__context__
    
    return chain