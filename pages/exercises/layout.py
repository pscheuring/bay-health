import dash_bootstrap_components as dbc
from dash import html

from utils import create_footer, create_header
from constants import EXERCISES


def create_layout() -> html.Div:
    """
    Create the exercise selection page layout.

    This layout displays a list of available exercises as cards.
    Each card contains an image, title, optional output text,
    and a button to add the exercise to the training plan.
    It also includes a modal confirmation when an exercise is added.

    Returns:
        html.Div: A Dash HTML Div containing the full exercise selection page.
    """
    return html.Div(
        dbc.Container(
            [
                # Page header with breadcrumb navigation
                create_header(label_link={"Bay Health": "/", "Übungsauswahl": ""}),

                # Collapsible section for exercise selection (currently always open)
                dbc.Collapse(
                    id="exercise-collapse",
                    is_open=True,
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # Section title
                                    html.H2(
                                        "Übungsauswahl",
                                        className="text-xl font-bold mb-6",
                                        style={"color": "rgb(69, 155, 112)"},
                                    ),
                                    # Display exercise cards in a responsive row
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Card(
                                                    [
                                                        # Exercise image
                                                        html.Img(
                                                            id={"type": "exercise-img", "index": ex["id"]},
                                                            src=ex["src"],
                                                            className="img-fluid rounded-top cursor-pointer",
                                                            n_clicks=0,
                                                        ),
                                                        # Exercise title and output placeholder
                                                        dbc.CardBody(
                                                            [
                                                                html.H5(
                                                                    ex["title"],
                                                                    className="card-title text-center"
                                                                ),
                                                                html.Div(
                                                                    id={
                                                                        "type": "exercise-output",
                                                                        "index": ex["id"],
                                                                    },
                                                                    className="text-muted text-sm text-center",
                                                                    style={"font-size": "12px"},
                                                                ),
                                                            ]
                                                        ),
                                                        # Button to add exercise
                                                        dbc.Button(
                                                            "Übung hinzufügen",
                                                            id={
                                                                "type": "add-exercise-btn",
                                                                "index": ex["id"],
                                                            },
                                                            color="success",
                                                            size="sm",
                                                            className="mt-2",
                                                            n_clicks=0,
                                                        ),
                                                    ],
                                                    className="shadow rounded-lg",
                                                ),
                                                md=3,
                                            )
                                            for ex in EXERCISES
                                        ],
                                        className="g-4",  # Gap between columns
                                    ),
                                ]
                            ),
                            className=(
                                "bg-white p-6 rounded-2xl shadow max-w-[90rem] mx-auto mt-8"
                            ),
                        )
                    ],
                ),

                # Modal confirmation when exercise is added
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Übung hinzugefügt")),
                        dbc.ModalBody(id="exercise-added-text"),
                        dbc.ModalFooter(
                            dbc.Button(
                                "OK",
                                id="close-exercise-modal",
                                className="ms-auto",
                                n_clicks=0,
                                style={
                                    "backgroundColor": "rgb(71, 158, 116)",
                                    "borderColor": "rgb(71, 158, 116)",
                                    "color": "white",
                                },
                            )
                        ),
                    ],
                    id="exercise-added-modal",
                    is_open=False,
                ),

                # Page footer
                create_footer(),
            ],
            fluid=True,
        )
    )
