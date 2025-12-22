import sys

def handle_exit(sig, frame):
    """
    Signal handler that prints a message and exits the program cleanly.

    Parameters
    ----------
    sig : int
        The signal number that triggered the handler.
    frame : frame object
        The current stack frame (unused).

    Returns
    -------
    None
    """
    # Optional: you can add any cleanup logic here (e.g., closing files, flushing logs).
    print(f"Received signal {sig}. Exiting gracefully.")
    sys.exit(0)