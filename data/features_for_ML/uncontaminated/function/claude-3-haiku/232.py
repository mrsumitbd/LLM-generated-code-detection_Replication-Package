def signal_handler(sig, frame):
    """
    This function is called when a signal is received by the program.

    Args:
        sig (int): The signal number that was received.
        frame (frame): The current stack frame.
    """
    import sys
    print(f"Signal {sig} received. Exiting...")
    sys.exit(0)