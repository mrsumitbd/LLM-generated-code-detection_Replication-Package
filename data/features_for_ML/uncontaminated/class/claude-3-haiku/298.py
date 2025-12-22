import multiprocessing
import os
import random
import string
import subprocess
import time
from typing import List

class ToolFuzzer:
    """Orchestrates fuzzing of MCP tools."""

    def __init__(self, max_concurrency: int = 5):
        self.max_concurrency = max_concurrency
        self.pool = multiprocessing.Pool(processes=self.max_concurrency)
        self.results = []

    def fuzz_tool(self, tool_path: str) -> None:
        """Fuzz a single MCP tool."""
        while True:
            input_data = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 1024)))
            try:
                subprocess.check_output([tool_path], input=input_data.encode(), stderr=subprocess.STDOUT, timeout=10)
            except subprocess.CalledProcessError as e:
                self.results.append((tool_path, input_data, e.output.decode()))
            time.sleep(random.uniform(0.1, 1.0))

    def fuzz_all_tools(self, tool_paths: List[str]) -> None:
        """Fuzz all MCP tools in parallel."""
        self.pool.map(self.fuzz_tool, tool_paths)
        self.pool.close()
        self.pool.join()

    def get_results(self) -> List[tuple]:
        """Return the results of the fuzzing process."""
        return self.results