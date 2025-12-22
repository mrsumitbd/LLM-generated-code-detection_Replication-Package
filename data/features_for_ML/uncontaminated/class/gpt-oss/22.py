from typing import Any, Optional, Dict
from enum import Enum, auto
import sys


class PrintType(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class UiWrapper:
    def __init__(self):
        # Buffer for captured output
        self._capture_buffer: str = ""
        self._capturing: bool = False
        # Optional: store chunks per thread if needed
        self._thread_chunks: Dict[str, str] = {}

    def print_text(
        self,
        message: Any,
        print_type: PrintType = PrintType.INFO,
        end: str = "\n",
        prefix: Optional[str] = None,
        flush: bool = False,
    ):
        """Print a message with optional type and prefix."""
        parts = []
        if prefix:
            parts.append(f"{prefix}:")
        if print_type == PrintType.INFO:
            parts.append("[INFO]")
        elif print_type == PrintType.WARNING:
            parts.append("[WARNING]")
        elif print_type == PrintType.ERROR:
            parts.append("[ERROR]")
        parts.append(str(message))
        output = " ".join(parts)
        print(output, end=end, flush=flush)

    def print_stream(self, message: str):
        """Print a raw stream message."""
        print(message, end="")

    def stream_chunk(self, thread_id: str, chunk: str) -> None:
        """Append a chunk to the capture buffer if capturing."""
        if self._capturing:
            self._capture_buffer += chunk
        # Store per-thread chunks if needed
        self._thread_chunks.setdefault(thread_id, "")
        self._thread_chunks[thread_id] += chunk

    def start_capture(self) -> None:
        """Begin capturing output."""
        self._capturing = True
        self._capture_buffer = ""

    def end_capture(self) -> None:
        """Stop capturing output."""
        self._capturing = False

    def get_capture(self) -> str:
        """Return the captured output."""
        return self._capture_buffer

    def model_changed(self, model):
        """Notify that the model has changed."""
        self.print_text(f"Model changed to {model}", PrintType.INFO)

    def model_list_updated(self) -> None:
        """Notify that the model list has been updated."""
        self.print_text("Model list updated", PrintType.INFO)

    def chat_thread_update(self, thread_id):
        """Notify that a chat thread has been updated."""
        self.print_text(f"Chat thread {thread_id} updated", PrintType.INFO)

    def code_context_update(self):
        """Notify that the code context has been updated."""
        self.print_text("Code context updated", PrintType.INFO)

    def update_task_info(self, worker_id: str, update: dict = None) -> None:
        """Notify that a task has been updated."""
        info = f"Worker {worker_id} update: {update}" if update else f"Worker {worker_id} updated"
        self.print_text(info, PrintType.INFO)

    def project_context_changed(self, is_enabled: bool) -> None:
        """Notify that the project context has changed."""
        state = "enabled" if is_enabled else "disabled"
        self.print_text(f"Project context {state}", PrintType.INFO)

    def providers_updated(self) -> None:
        """Notify that providers have been updated."""
        self.print_text("Providers updated", PrintType.INFO)