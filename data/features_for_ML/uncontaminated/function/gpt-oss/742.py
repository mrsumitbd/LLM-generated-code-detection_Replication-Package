from flask import Flask

def create_app():
    """
    Create and configure a Flask application instance.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello, World!"

    return app