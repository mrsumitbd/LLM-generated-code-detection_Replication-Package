class _BashSession:
    """A session of a bash shell."""

    def __init__(self):
        self._process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self._running = True

    def stop(self):
        if self._running:
            self._process.terminate()
            self._process.wait()
            self._running = False

    def run_command(self, command):
        if self._running:
            self._process.stdin.write(command + '\n')
            self._process.stdin.flush()
            output = self._process.stdout.read().strip()
            error = self._process.stderr.read().strip()
            return output, error
        else:
            raise ValueError('The bash session has been stopped.')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()