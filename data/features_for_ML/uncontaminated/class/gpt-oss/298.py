import concurrent.futures
import subprocess
import time
import random
import string
import threading
from typing import List, Dict, Any, Optional


class ToolFuzzer:
    """Orchestrates fuzzing of MCP tools."""

    def __init__(self, max_concurrency: int = 5):
        self.max_concurrency = max_concurrency
        self._tools: List[Dict[str, Any]] = []
        self._results: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = threading.Lock()

    def add_tool(self, name: str, command: List[str], args: Optional[List[str]] = None) -> None:
        """Register a tool to be fuzzed."""
        if args is None:
            args = []
        tool_cfg = {"name": name, "command": command, "args": args}
        self._tools.append(tool_cfg)
        self._results[name] = []

    def _generate_random_input(self, length: int = 20) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def _fuzz_tool(self, tool_cfg: Dict[str, Any], stop_event: threading.Event) -> None:
        name = tool_cfg["name"]
        cmd = tool_cfg["command"] + tool_cfg["args"]
        while not stop_event.is_set():
            random_input = self._generate_random_input()
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = proc.communicate(input=random_input, timeout=5)
                result = {
                    "input": random_input,
                    "stdout": stdout,
                    "stderr": stderr,
                    "returncode": proc.returncode,
                    "timestamp": time.time(),
                }
            except subprocess.TimeoutExpired:
                proc.kill()
                result = {
                    "input": random_input,
                    "stdout": "",
                    "stderr": "timeout",
                    "returncode": None,
                    "timestamp": time.time(),
                }
            except Exception as exc:
                result = {
                    "input": random_input,
                    "stdout": "",
                    "stderr": str(exc),
                    "returncode": None,
                    "timestamp": time.time(),
                }

            with self._lock:
                self._results[name].append(result)

    def run_fuzz(self, duration: int = 60) -> None:
        """Run fuzzing for all registered tools concurrently for the given duration."""
        stop_event = threading.Event()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrency) as executor:
            futures = [
                executor.submit(self._fuzz_tool, tool_cfg, stop_event)
                for tool_cfg in self._tools
            ]
            time.sleep(duration)
            stop_event.set()
            # Wait for all threads to finish
            concurrent.futures.wait(futures, timeout=10)

    def get_results(self) -> Dict[str, List[Dict[str, Any]]]:
        """Return collected fuzzing results."""
        with self._lock:
            return {k: list(v) for k, v in self._results.items()}

    def __repr__(self) -> str:
        return f"<ToolFuzzer concurrency={self.max_concurrency} tools={len(self._tools)}>"