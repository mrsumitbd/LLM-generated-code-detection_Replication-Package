import sys
import time
import threading


class SpinnerInterface:
    def __init__(self, message: str = ""):
        self.message = message
        self._spinner_running = False
        self._spinner_thread = None
        self._stop_event = threading.Event()
        self._spinner_chars = ["|", "/", "-", "\\"]
        self._delay = 0.1

    def spin(self) -> None:
        if self._spinner_running:
            return
        self._stop_event.clear()
        self._spinner_thread = threading.Thread(target=self._run_spinner)
        self._spinner_thread.daemon = True
        self._spinner_running = True
        self._spinner_thread.start()

    def _run_spinner(self) -> None:
        idx = 0
        while not self._stop_event.is_set():
            char = self._spinner_chars[idx % len(self._spinner_chars)]
            sys.stdout.write(f"\r{self.message} {char}")
            sys.stdout.flush()
            time.sleep(self._delay)
            idx += 1
        # Clear spinner line
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()

    def finish(self, final_status: str) -> None:
        if not self._spinner_running:
            sys.stdout.write(final_status + "\n")
            sys.stdout.flush()
            return
        self._stop_event.set()
        self._spinner_thread.join()
        self._spinner_running = False
        sys.stdout.write(f"\r{final_status}\n")
        sys.stdout.flush()