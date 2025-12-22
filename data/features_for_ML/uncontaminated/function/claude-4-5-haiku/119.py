def flush_stdin():
    import sys
    import os
    
    if sys.stdin.isatty():
        # For interactive terminals
        try:
            import termios
            import tty
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except (ImportError, OSError):
            # Fallback for systems without termios
            try:
                while True:
                    if not os.read(sys.stdin.fileno(), 1):
                        break
            except (OSError, IOError):
                pass
    else:
        # For non-interactive input
        try:
            while True:
                char = sys.stdin.read(1)
                if not char:
                    break
        except (OSError, IOError):
            pass