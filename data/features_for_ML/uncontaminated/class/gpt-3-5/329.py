import subprocess

class _BashSession:
    """A session of a bash shell."""

    def __init__(self):
        self.process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop(self):
        self.process.terminate()