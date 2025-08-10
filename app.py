from typing import Tuple

import dash
import dash_bootstrap_components as dbc
from flask import Flask
from app_layout import create_app_layout


def create_app() -> Tuple[Flask, dash.Dash]:
    """
    Create and configure the Flask and Dash application instances.

    Returns:
        Tuple[Flask, dash.Dash]: 
            - Flask server instance for WSGI hosting.
            - Dash application instance for rendering the UI.
    """
    # Base Flask server (needed for Dash integration & potential backend routes)
    flask_server = Flask(__name__)

    # Dash application setup
    dash_app = dash.Dash(
        __name__,
        external_scripts=[{"src": "/assets/tailwind.css"}],  # Tailwind CSS
        server=flask_server,
        use_pages=True,  # Enable Dash Pages routing
        pages_folder="pages",
        assets_folder="assets",
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            # Bootstrap Icons for star ratings
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
            dbc.icons.FONT_AWESOME,
            dbc.icons.BOOTSTRAP,
        ],
        suppress_callback_exceptions=True,  # Avoid callback errors before elements exist
    )

    return flask_server, dash_app


# Create the app instances
server, app = create_app()

# Set the app layout
app.layout = create_app_layout()

if __name__ == "__main__":
    app.run(debug=True)
    server = app.server
