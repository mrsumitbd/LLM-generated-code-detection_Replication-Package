def extract_exception_chain(exception: Exception) -> List[str]:
    chain = []
    while exception:
        chain.append(str(exception))
        exception = exception.__cause__
    return chain