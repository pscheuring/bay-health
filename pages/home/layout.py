from typing import Dict, Any

import dash
import dash_bootstrap_components as dbc
from dash import html
from utils import create_button, create_footer, create_header

# Dictionary containing the card configuration for the home page
COL_CARDS: Dict[str, Dict[str, Any]] = {
    "button-health_state": {
        "h2": "Gesundheitszustand",
        "p": (
            "Hier kannst du deinen Gesundheitszustand eingeben. "
            "Anschließend kannst du deine bevorzugten Übungen finden "
            "und deine eigenen Übungen hinzufügen."
        ),
        "path": "/health_state/health_state",
        "image_path": "health_state.jpg",
        "button_id": "button-health-state",
        "type": "button",
        "label": "Gehe zu Trainingsfortschritt",
        "color": "success",
        "icon_class_name": "fas fa-solid fa-suitcase-medical pr-2",
    },
    "button-exercises": {
        "h2": "Übungsauswahl",
        "p": (
            "Hier kannst du deine bevorzugten Übungen finden "
            "und deine eigenen Übungen hinzufügen. "
            "Anschließend kannst du deine Trainingsfortschritte betrachten."
        ),
        "path": "/exercises/exercises",
        "image_path": "exercises.jpg",
        "button_id": "button-exercises",
        "type": "button",
        "label": "Gehe zu Übungsauswahl",
        "color": "success",
        "icon_class_name": "fas fa-solid fa-dumbbell pr-2",
    },
    "button-progress": {
        "h2": "Trainingsfortschritt",
        "p": (
            "Hier kannst du deine Trainingsfortschritte betrachten. "
            "Anschließend kannst du deine bevorzugten Übungen finden "
            "und deine eigenen Übungen hinzufügen."
        ),
        "path": "/progress/progress",
        "image_path": "progress.jpg",
        "button_id": "button-progress",
        "type": "button",
        "label": "Gehe zu Trainingsfortschritt",
        "color": "success",
        "icon_class_name": "fas fa-solid fa-medal pr-2",
    }
}


def create_page_col(page: Dict[str, Any]) -> dbc.Col:
    """
    Create a Bootstrap column containing a navigation card for a given page.

    Args:
        page (dict): Configuration dictionary for the card, including
            title, description, path, image, and button details.

    Returns:
        dbc.Col: Dash Bootstrap Column containing the card layout.
    """
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        # Card title
                        html.H2(
                            page["h2"],
                            className="mb-2",
                            style={
                                "text-align": "center",
                                "font-weight": "bold",
                                "font-size": "30px",
                            },
                        ),
                        # Card description
                        html.P(
                            page["p"],
                            className="mb-3",
                            style={"text-align": "center"},
                        ),
                        # Card image (clickable)
                        html.A(
                            href=dash.get_relative_path(page["path"]),
                            children=[
                                html.Img(
                                    src=dash.get_asset_url(page["image_path"]),
                                    className="w-full object-cover mb-3",
                                    style={"height": "200px"},
                                )
                            ],
                        ),
                        # Navigation button
                        create_button(
                            {"type": "button", "index": page["button_id"]},
                            page["label"],
                            page["color"],
                            page["icon_class_name"],
                        ),
                    ]
                )
            ],
            className=(
                "hover:bg-gray-100 hover:border-gray-200 "
                "rounded-lg shadow-sm h-100 mb-1"
            ),
            style={"backgroundColor": "#F1EFEF"},
        ),
        md=4,
        className="mb-4",
    )


def create_layout() -> html.Div:
    """
    Create the main layout for the home page.

    This includes:
    - A header with breadcrumb navigation
    - Page title and subtitle
    - A row of navigation cards for each page
    - A footer

    Returns:
        html.Div: Dash HTML div containing the complete home page layout.
    """
    return html.Div(
        dbc.Container(
            [
                # Header with breadcrumb
                create_header(label_link={"Bay Health": "/", "Home": ""}),

                # Title & subtitle
                dbc.Row(
                    [
                        html.H1(
                            "Bay Health",
                            style={
                                "font-size": "60px",
                                "text-align": "center",
                                "font-weight": "bold",
                            },
                        ),
                        html.H1(
                            "Dein Körper, dein Plan – verletzungssicher trainieren.",
                            style={
                                "font-size": "32px",
                                "text-align": "center",
                                "font-style": "italic",
                                "color": "rgb(69, 155, 112)",
                            },
                        ),
                    ],
                    className="h-100 mt-3",
                ),

                # Navigation cards
                dbc.Row(
                    [create_page_col(COL_CARDS[key]) for key in COL_CARDS],
                    className="h-100 mt-3",
                ),

                # Footer
                create_footer(),
            ],
            fluid=True,
        )
    )
