from typing import Any, Optional
from enum import Enum

class PrintType(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

class UiWrapper:

    def __init__(self):
        self.captured_output = ""

    def print_text(self, message: Any, print_type: PrintType = PrintType.INFO, end: str = "\n", prefix: Optional[str] = None, flush: bool = False):
        if prefix:
            message = f"[{prefix}] {message}"
        output = f"{message}{end}"
        if flush:
            print(output, end="", flush=True)
        else:
            print(output, end="")

    def print_stream(self, message: str):
        print(message, end="")

    def stream_chunk(self, thread_id: str, chunk: str) -> None:
        print(f"[Thread {thread_id}] {chunk}", end="")

    def start_capture(self) -> None:
        import sys
        self.captured_output = ""
        sys.stdout = self

    def end_capture(self) -> None:
        import sys
        sys.stdout = sys.__stdout__

    def get_capture(self) -> str:
        return self.captured_output

    def write(self, text):
        self.captured_output += text

    def model_changed(self, model):
        pass

    def model_list_updated(self) -> None:
        pass

    def chat_thread_update(self, thread_id):
        pass

    def code_context_update(self):
        pass

    def update_task_info(self, worker_id: str, update: dict = None) -> None:
        pass

    def project_context_changed(self, is_enabled: bool) -> None:
        pass

    def providers_updated(self) -> None:
        pass