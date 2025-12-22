from __future__ import annotations
from typing import Any, Dict, Optional
import threading
import queue
import uuid
import time


class ResearchAgent:
    """
    A simple research agent that sends queries to a message thread and collects responses.
    """

    def __init__(self, app: Any, thread: Any):
        """
        Initialize the ResearchAgent with an application context and a message thread.

        :param app: The application context (can be any object).
        :param thread: The message thread used for communication.
        """
        self.app = app
        self.thread = thread
        self._query_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self._response_dict: Dict[str, str] = {}
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """
        Start the background worker thread that processes queries.
        """
        if self._worker_thread and self._worker_thread.is_alive():
            return
        self._stop_event.clear()
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

    def stop(self) -> None:
        """
        Stop the background worker thread.
        """
        self._stop_event.set()
        if self._worker_thread:
            self._worker_thread.join()
            self._worker_thread = None

    def send_query(self, query: str) -> str:
        """
        Send a query to the message thread and return a unique query ID.

        :param query: The query string to send.
        :return: A unique query ID.
        """
        query_id = str(uuid.uuid4())
        self._query_queue.put((query_id, query))
        return query_id

    def get_response(self, query_id: str, timeout: float = 5.0) -> Optional[str]:
        """
        Retrieve the response for a given query ID.

        :param query_id: The unique query ID.
        :param timeout: Maximum time to wait for the response.
        :return: The response string or None if not available.
        """
        start = time.time()
        while time.time() - start < timeout:
            if query_id in self._response_dict:
                return self._response_dict.pop(query_id)
            time.sleep(0.05)
        return None

    def _worker(self) -> None:
        """
        Internal worker that processes queries from the queue.
        """
        while not self._stop_event.is_set():
            try:
                query_id, query = self._query_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                # Send the query to the thread and wait for a response
                self.thread.send_message(query)
                response = self.thread.wait_for_response(timeout=10.0)
                self._response_dict[query_id] = response
            except Exception as e:
                self._response_dict[query_id] = f"Error: {e}"
            finally:
                self._query_queue.task_done()