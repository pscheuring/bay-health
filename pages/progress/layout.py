from dash import html
import dash_bootstrap_components as dbc


def create_layout() -> dbc.Card:
    """
    Create the layout for the training progress page.

    This layout includes:
    - A title ("Trainingsfortschritt")
    - A container div where training progress components will be dynamically inserted.

    Returns:
        dbc.Card: A Dash Bootstrap Card containing the training progress layout.
    """
    return dbc.Card(
        dbc.CardBody(
            [
                # Section title
                html.H2(
                    "Trainingsfortschritt",
                    className="text-xl font-bold mb-6",
                    style={"color": "rgb(69, 155, 112)"},
                ),
                # Container for dynamic training progress elements
                html.Div(id="training-progress-container"),
            ]
        ),
        className="mt-4 mb-4",
    )