class SpinnerInterface:
    def __init__(self, message: str, delay: float = 0.1):
        self.message = message
        self.delay = delay
        self.running = False

    def spin(self) -> None:
        import sys
        import time
        import itertools

        self.running = True
        spinner = itertools.cycle(['|', '/', '-', '\\'])
        while self.running:
            sys.stdout.write(f"\r{self.message} {next(spinner)}")
            sys.stdout.flush()
            time.sleep(self.delay)

    def finish(self, final_status: str) -> None:
        self.running = False
        sys.stdout.write(f"\r{self.message} {final_status}\n")
        sys.stdout.flush()