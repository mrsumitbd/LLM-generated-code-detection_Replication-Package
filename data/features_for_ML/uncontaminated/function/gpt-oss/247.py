import sys

def stream_output(stream, prefix):
    """
    Read lines from the given stream and write them to standard output,
    each line prefixed with the provided prefix string.

    Parameters
    ----------
    stream : Iterable[str]
        A file-like object or any iterable yielding lines of text.
    prefix : str
        The string to prepend to each line before printing.

    Returns
    -------
    None
    """
    for line in stream:
        # Remove trailing newline to avoid double newlines
        stripped = line.rstrip("\n")
        sys.stdout.write(f"{prefix}{stripped}\n")
        sys.stdout.flush()