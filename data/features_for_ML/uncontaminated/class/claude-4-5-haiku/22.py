class UiWrapper:

    def __init__(self):
        self._capture_enabled = False
        self._captured_output = []

    def print_text(self, message: Any, print_type: PrintType = PrintType.INFO, end: str = "\n", prefix: Optional[str] = None, flush: bool = False):
        if prefix is None:
            prefix = print_type.value
        
        formatted_message = f"[{prefix}] {message}" if prefix else str(message)
        
        if self._capture_enabled:
            self._captured_output.append(formatted_message)
        
        print(formatted_message, end=end, flush=flush)

    def print_stream(self, message: str):
        if self._capture_enabled:
            self._captured_output.append(message)
        
        print(message, end="", flush=True)

    def stream_chunk(self, thread_id: str, chunk: str) -> None:
        if self._capture_enabled:
            self._captured_output.append(chunk)
        
        print(chunk, end="", flush=True)

    def start_capture(self) -> None:
        self._capture_enabled = True
        self._captured_output = []

    def end_capture(self) -> None:
        self._capture_enabled = False

    def get_capture(self) -> str:
        return "".join(self._captured_output)

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