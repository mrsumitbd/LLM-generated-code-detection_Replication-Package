def even_numbers(n):
    """Return a list of even integers from 0 up to and including n."""
    if n < 0:
        return []
    return [i for i in range(0, n + 1, 2)]