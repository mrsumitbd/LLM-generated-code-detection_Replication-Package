from typing import Callable, Optional
import threading
import logging

try:
    # pyngrok is the preferred library for creating tunnels
    from pyngrok import ngrok
    from pyngrok.exception import PyngrokError
except Exception:
    ngrok = None  # type: ignore
    PyngrokError = Exception  # type: ignore

def _start_tunnel(port: int,
                  url_callback: Optional[Callable[[str], None]],
                  error_callback: Optional[Callable[[str], None]]) -> None:
    """
    Internal helper that runs in a separate thread to start the tunnel
    and invoke callbacks. This keeps the main thread non‑blocking.
    """
    try:
        # pyngrok will automatically start the ngrok process if needed
        tunnel = ngrok.connect(port, bind_tls=True)
        public_url = tunnel.public_url
        if url_callback:
            url_callback(public_url)
    except Exception as exc:
        if error_callback:
            error_callback(str(exc))
        else:
            logging.error("Tunnel error: %s", exc)

def start_tunnel_for_api(port: int = 5000,
                         url_callback: Optional[Callable[[str], None]] = None,
                         error_callback: Optional[Callable[[str], None]] = None) -> bool:
    """
    Convenience function to start tunnel for API server

    Args:
        port: API server port
        url_callback: Callback function for when tunnel URL is available
        error_callback: Callback function for tunnel errors

    Returns:
        bool: True if tunnel startup was initiated successfully
    """
    if ngrok is None:
        # pyngrok is not available; cannot start a tunnel
        if error_callback:
            error_callback("pyngrok is not installed; cannot start tunnel.")
        else:
            logging.error("pyngrok is not installed; cannot start tunnel.")
        return False

    # Start the tunnel in a background thread so the caller is not blocked
    thread = threading.Thread(
        target=_start_tunnel,
        args=(port, url_callback, error_callback),
        daemon=True
    )
    try:
        thread.start()
        return True
    except Exception as exc:
        if error_callback:
            error_callback(str(exc))
        else:
            logging.error("Failed to start tunnel thread: %s", exc)
        return False