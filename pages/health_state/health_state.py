from typing import Any, Dict, List

import dash
from dash import html, Input, Output, State, ctx, MATCH, ALL
from pages.health_state.layout import create_layout

# Dash page registration
dash.register_page(__name__, path="/health_state/health_state")
layout = create_layout()


@dash.callback(
    Output("health_state", "data"),
    Input("start-training-btn", "n_clicks"),
    State("longterm-complaints-choice", "value"),
    State("longterm-complaints-text", "value"),
    State("shortterm-complaints-choice", "value"),
    State("shortterm-complaints-text", "value"),
    State("star-results", "data"),
    prevent_initial_call=True,
)
def save_health_state(
    n_clicks: int,
    longterm_choice: str,
    longterm_text: str,
    shortterm_choice: str,
    shortterm_text: str,
    star_results: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Save the current health state data into a dcc.Store.

    Args:
        n_clicks (int): Click count for the "Start Training" button.
        longterm_choice (str): Choice regarding long-term complaints ("yes"/"no").
        longterm_text (str): Additional description of long-term complaints.
        shortterm_choice (str): Choice regarding short-term complaints ("yes"/"no").
        shortterm_text (str): Additional description of short-term complaints.
        star_results (dict): Dictionary of star ratings for recovery questions.

    Returns:
        dict: Stored health state data.
    """
    return {
        "longterm_choice": longterm_choice,
        "longterm_text": longterm_text,
        "shortterm_choice": shortterm_choice,
        "shortterm_text": shortterm_text,
        "star_ratings": star_results,
    }


@dash.callback(
    Output("longterm-collapse", "is_open"),
    Input("longterm-complaints-choice", "value"),
)
def toggle_longterm_input(value: str) -> bool:
    """
    Toggle the long-term complaints input area.

    Args:
        value (str): Selected value for long-term complaints.

    Returns:
        bool: True if "yes" is selected, False otherwise.
    """
    return value == "ja"


@dash.callback(
    Output("shortterm-collapse", "is_open"),
    Input("shortterm-complaints-choice", "value"),
)
def toggle_shortterm_input(value: str) -> bool:
    """
    Toggle the short-term complaints input area.

    Args:
        value (str): Selected value for short-term complaints.

    Returns:
        bool: True if "yes" is selected, False otherwise.
    """
    return value == "ja"


@dash.callback(
    Output({"type": "star", "question": MATCH, "index": ALL}, "children"),
    Input({"type": "star", "question": MATCH, "index": ALL}, "n_clicks"),
    State({"type": "star", "question": MATCH, "index": ALL}, "id"),
)
def update_star_display(
    n_clicks_list: List[int],
    ids: List[Dict[str, Any]],
) -> List[html.I]:
    """
    Update the star display for the star rating components.

    Args:
        n_clicks_list (list): Number of clicks for each star.
        ids (list): List of star component IDs.

    Returns:
        list: Updated list of HTML star icons.
    """
    triggered = ctx.triggered_id
    selected_index = triggered["index"] if triggered else 0

    return [
        html.I(
            className="bi bi-star-fill" if i <= selected_index else "bi bi-star"
        )
        for i in range(1, 6)
    ]


@dash.callback(
    Output("health-confirm-modal", "is_open"),
    [Input("start-training-btn", "n_clicks"), Input("close-health-modal", "n_clicks")],
    [State("health-confirm-modal", "is_open")],
)
def toggle_health_modal(
    submit_clicks: int, close_clicks: int, is_open: bool
) -> bool:
    """
    Toggle the health confirmation modal.

    Args:
        submit_clicks (int): Click count for the start button.
        close_clicks (int): Click count for the close modal button.
        is_open (bool): Current modal open state.

    Returns:
        bool: Updated modal open state.
    """
    if submit_clicks or close_clicks:
        return not is_open
    return is_open


@dash.callback(
    Output("star-results", "data"),
    Input({"type": "star", "question": ALL, "index": ALL}, "n_clicks"),
    State({"type": "star", "question": ALL, "index": ALL}, "id"),
    State("star-results", "data"),
    prevent_initial_call=True,
)
def update_star_results(
    n_clicks_list: List[int],
    id_list: List[Dict[str, Any]],
    current_data: Dict[str, int],
) -> Dict[str, int]:
    """
    Update the star rating results in dcc.Store.

    Args:
        n_clicks_list (list): List of click counts for all stars.
        id_list (list): List of star component IDs.
        current_data (dict): Current stored star rating data.

    Returns:
        dict: Updated star rating data.
    """
    ctx_trigger = ctx.triggered_id
    if ctx_trigger is None:
        return dash.no_update

    question = ctx_trigger["question"]
    rating = ctx_trigger["index"]

    updated = current_data.copy()
    updated[question] = rating
    return updated
