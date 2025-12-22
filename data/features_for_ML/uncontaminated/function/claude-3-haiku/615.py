def handle_exit(sig, frame):
    """
    This function is called when the program receives a signal to exit.
    
    Args:
        sig (int): The signal number that was received.
        frame (frame): The current stack frame.
    """
    print(f"Received signal {sig}, exiting...")
    import sys
    sys.exit(0)