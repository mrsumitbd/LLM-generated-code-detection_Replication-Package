import threading
import socket
import json
from typing import Callable, List, Any, Optional


class Chat:
    """
    A lightweight wrapper around a socket‑like client that provides
    asynchronous message reception, callback registration, and a
    convenient context‑manager interface.

    Parameters
    ----------
    client : socket.socket or any object exposing ``sendall``,
             ``recv``, ``shutdown`` and ``close`` methods.
    """

    def __init__(self, client: Any) -> None:
        if not hasattr(client, "sendall") or not hasattr(client, "recv"):
            raise TypeError("client must provide sendall() and recv() methods")
        self._client = client
        self._recv_thread: Optional[threading.Thread] = None
        self._running = False
        self._callbacks: List[Callable[[str], None]] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def start(self) -> None:
        """Start the background thread that receives messages."""
        if self._running:
            return
        self._running = True
        self._recv_thread = threading.Thread(
            target=self._recv_loop, daemon=True, name="ChatReceiver"
        )
        self._recv_thread.start()

    def send(self, message: str) -> None:
        """
        Send a UTF‑8 encoded string to the remote peer.

        Parameters
        ----------
        message : str
            The message to send.
        """
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        data = message.encode("utf-8")
        try:
            self._client.sendall(data)
        except Exception as exc:
            raise RuntimeError(f"Failed to send message: {exc}") from exc

    def register_callback(self, cb: Callable[[str], None]) -> None:
        """
        Register a callback that will be invoked for every received
        message.

        Parameters
        ----------
        cb : callable
            A function accepting a single string argument.
        """
        if not callable(cb):
            raise TypeError("callback must be callable")
        with self._lock:
            self._callbacks.append(cb)

    def unregister_callback(self, cb: Callable[[str], None]) -> None:
        """
        Remove a previously registered callback.

        Parameters
        ----------
        cb : callable
            The callback to remove.
        """
        with self._lock:
            if cb in self._callbacks:
                self._callbacks.remove(cb)

    def close(self) -> None:
        """Stop receiving and close the underlying client."""
        self._running = False
        if self._recv_thread:
            self._recv_thread.join(timeout=1.0)
        try:
            self._client.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self._client.close()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Context‑manager support
    # ------------------------------------------------------------------
    def __enter__(self) -> "Chat":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def send_json(self, obj: Any) -> None:
        """
        Serialize *obj* to JSON and send it as a UTF‑8 string.

        Parameters
        ----------
        obj : Any
            The object to serialize.
        """
        try:
            json_str = json.dumps(obj)
        except Exception as exc:
            raise ValueError(f"Object not JSON‑serialisable: {exc}") from exc
        self.send(json_str)

    def receive_json(self) -> Any:
        """
        Blocking call that receives a single UTF‑8 encoded JSON string
        and deserialises it.

        Returns
        -------
        Any
            The deserialised Python object.
        """
        data = self._client.recv(4096)
        if not data:
            raise EOFError("Connection closed")
        try:
            return json.loads(data.decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"Failed to decode JSON: {exc}") from exc

    # ------------------------------------------------------------------
    # Internal implementation
    # ------------------------------------------------------------------
    def _recv_loop(self) -> None:
        """Internal thread target that receives data and dispatches callbacks."""
        while self._running:
            try:
                data = self._client.recv(4096)
                if not data:
                    break
                message = data.decode("utf-8")
                with self._lock:
                    for cb in list(self._callbacks):
                        try:
                            cb(message)
                        except Exception:
                            # Ignore callback errors to keep the loop alive
                            pass
            except Exception:
                # Any exception (including socket errors) terminates the loop
                break

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"<Chat client={self._client!r} running={self._running}>"