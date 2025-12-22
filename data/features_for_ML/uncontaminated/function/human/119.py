import sys
from termios import TCIOFLUSH, tcflush
import msvcrt

def flush_stdin():
    try:
        from termios import TCIOFLUSH, tcflush

        tcflush(sys.stdin, TCIOFLUSH)
    except Exception:
        try:
            import msvcrt

            while msvcrt.kbhit():
                msvcrt.getch()
        except Exception:
            pass