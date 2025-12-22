import os
import subprocess
import threading
import time


class _BashSession:
    """A session of a bash shell."""

    def __init__(self):
        # Start a bash process with a predictable prompt
        env = os.environ.copy()
        env["PS1"] = "PROMPT> "
        self._proc = subprocess.Popen(
            ["bash", "--noprofile", "--norc"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
        self._output = ""
        self._lock = threading.Lock()
        self._stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self._stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._stdout_thread.start()
        self._stderr_thread.start()

    def _read_stdout(self):
        for line in self._proc.stdout:
            with self._lock:
                self._output += line

    def _read_stderr(self):
        for line in self._proc.stderr:
            with self._lock:
                self._output += line

    def run(self, command, timeout=5):
        """Run a command in the bash session and return its output."""
        if self._proc.poll() is not None:
            raise RuntimeError("Bash session has terminated")
        with self._lock:
            self._output = ""
        self._proc.stdin.write(command + "\n")
        self._proc.stdin.flush()
        end = time.time() + timeout
        while time.time() < end:
            with self._lock:
                if "PROMPT> " in self._output:
                    out = self._output
                    # Remove the echoed command and the prompt line
                    lines = out.splitlines()
                    if lines and lines[0].strip() == command.strip():
                        lines = lines[1:]
                    if lines and lines[-1].strip().startswith("PROMPT>"):
                        lines = lines[:-1]
                    return "\n".join(lines)
            time.sleep(0.01)
        raise TimeoutError("Command timed out")

    def stop(self):
        """Terminate the bash session."""
        if self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        self._proc.stdin.close()
        self._proc.stdout.close()
        self._proc.stderr.close()