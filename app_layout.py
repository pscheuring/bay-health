import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, page_container

# Navigation structure: mapping between page identifiers and their metadata
nav_info = {
    "home": {
        "title": " Home",
        "class_name": "fas fa-solid fa-house",
        "relative_path": "/",
    },
    "health_state": {
        "title": " Gesundheitszustand",
        "class_name": "fas fa-solid fa-suitcase-medical",
        "relative_path": "/health_state/health_state",
    },
    "exercises": {
        "title": " Übungsauswahl",
        "class_name": "fas fa-solid fa-dumbbell",
        "relative_path": "/exercises/exercises",
    },
    "progress": {
        "title": " Trainingsfortschritt",
        "class_name": "fas fa-solid fa-medal",
        "relative_path": "/progress/progress",
    },
}


def create_navbar() -> html.Div:
    """
    Create the left-hand navigation sidebar.

    Returns:
        html.Div: A sidebar component with logo and navigation links.
    """
    navbar = html.Div(
        [
            # Logo link
            html.A(
                href=dash.get_relative_path("/"),
                children=[
                    html.Img(
                        src=dash.get_asset_url("ubt_logo.jpeg"),
                        style={"maxWidth": "60px", "height": "auto"},
                    )
                ],
                className="sidebar-header",
            ),
            html.Div([html.Hr()], style={"padding": "7px 0px 5px 0px"}),

            # Navigation links for each registered page
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.I(className=nav_info[page]["class_name"]),
                            html.Span(nav_info[page]["title"]),
                        ],
                        href=dash.get_relative_path(
                            nav_info[page]["relative_path"]
                        ),
                        active="exact",
                    )
                    for page in nav_info
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="sidebar",
    )
    return navbar


def create_app_layout() -> html.Div:
    """
    Creates the general application layout, including:
    - Navigation sidebar
    - Page content container
    - Persistent dcc.Store components for app state

    Returns:
        html.Div: Main application layout container.
    """
    navbar = create_navbar()

    app_layout = html.Div(
        [
            # Tracks the current URL for page routing
            dcc.Location(id="current-url", refresh="callback-nav"),

            # Persistent storage components for cross-page data sharing
            dcc.Store(id="added-exercises", data=[]),
            dcc.Store(id="health_state", data=[]),
            dcc.Store(id="health-form-store"),
            dcc.Store(id="star-results", data={}),

            # Sidebar container
            dbc.Container(
                [navbar],
                style={
                    "display": "inline-block",
                    "width": "5%",
                },
                fluid=True,
            ),

            # Main content container for page layouts
            dbc.Container(
                [page_container],
                style={
                    "display": "inline-block",
                    "width": "95%",
                },
                fluid=True,
            ),
        ],
    )
    return app_layout
