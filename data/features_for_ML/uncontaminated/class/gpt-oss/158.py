from flask import Flask, jsonify


class WatcherHealthServer:
    """Simple HTTP health endpoint for watcher monitoring."""

    def __init__(self, watcher, port=8080):
        """
        Initialize the health server.

        Parameters
        ----------
        watcher : object
            The watcher instance to monitor. It should expose either an
            ``is_healthy`` method or a ``status`` attribute that evaluates
            to a truthy value when healthy.
        port : int, optional
            The port on which the HTTP server will listen. Defaults to 8080.
        """
        self.watcher = watcher
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        """Configure the Flask routes for the health endpoint."""

        @self.app.route("/health")
        def health():
            """
            Health check endpoint.

            Returns a JSON payload indicating whether the watcher is healthy.
            HTTP status code 200 is returned for healthy, 503 otherwise.
            """
            healthy = True
            try:
                if hasattr(self.watcher, "is_healthy"):
                    healthy = bool(self.watcher.is_healthy())
                elif hasattr(self.watcher, "status"):
                    healthy = bool(self.watcher.status)
            except Exception:
                healthy = False

            status_code = 200 if healthy else 503
            return jsonify({"healthy": healthy}), status_code

    def run(self):
        """Start the Flask development server."""
        self.app.run(host="0.0.0.0", port=self.port)