from typing import Any, Optional
from enum import Enum

class PrintType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class UiWrapper:
    def __init__(self):
        self._captured_output = ""

    def print_text(self, message: Any, print_type: PrintType = PrintType.INFO, end: str = "\n", prefix: Optional[str] = None, flush: bool = False):
        formatted_message = f"{prefix} {message}" if prefix else str(message)
        print(f"[{print_type.value}] {formatted_message}", end=end, flush=flush)
        self._captured_output += formatted_message + end

    def print_stream(self, message: str):
        self.print_text(message)

    def stream_chunk(self, thread_id: str, chunk: str) -> None:
        self.print_text(f"Thread {thread_id}: {chunk}")

    def start_capture(self) -> None:
        self._captured_output = ""

    def end_capture(self) -> None:
        pass

    def get_capture(self) -> str:
        return self._captured_output

    def model_changed(self, model):
        self.print_text(f"Model changed: {model}")

    def model_list_updated(self) -> None:
        self.print_text("Model list updated")

    def chat_thread_update(self, thread_id):
        self.print_text(f"Chat thread {thread_id} updated")

    def code_context_update(self):
        self.print_text("Code context updated")

    def update_task_info(self, worker_id: str, update: dict = None) -> None:
        if update:
            self.print_text(f"Task info updated for worker {worker_id}: {update}")
        else:
            self.print_text(f"Task info updated for worker {worker_id}")

    def project_context_changed(self, is_enabled: bool) -> None:
        status = "enabled" if is_enabled else "disabled"
        self.print_text(f"Project context {status}")

    def providers_updated(self) -> None:
        self.print_text("Providers updated")