from typing import List, Dict, Optional, Union
import os
import glob
from datetime import date

import dash
from dash import Output, html, Input
import dash_bootstrap_components as dbc
import pandas as pd
import dash_ag_grid as dag

from pages.progress.layout import create_layout
from constants import MUSCLE_MATRIX, EXERCISES

# Register page with Dash
dash.register_page(__name__)
layout = create_layout()


def get_latest_muscle_svg() -> str:
    """
    Get the latest generated muscle SVG file from the assets folder.

    Returns:
        str: URL to the latest muscle SVG or a fallback default SVG.
    """
    files = glob.glob("assets/muscle_dynamic_*.svg")
    if not files:
        return dash.get_asset_url("muscle_sections.svg")  # Fallback

    latest_file = max(files, key=os.path.getmtime)
    filename = os.path.basename(latest_file)
    return dash.get_asset_url(filename)


def create_muscle_score_table(exercise_ids: List[str], factor: float = 1.0) -> html.Div:
    """
    Create a muscle score table based on selected exercises and a scaling factor.

    Args:
        exercise_ids (List[str]): List of selected exercise IDs.
        factor (float): Scaling factor applied to scores (e.g., recovery factor).

    Returns:
        html.Div: A scrollable table displaying muscle group scores.
    """
    selected_matrix = MUSCLE_MATRIX.loc[exercise_ids] * factor
    muscle_scores = selected_matrix.sum().sort_values(ascending=False)

    df = pd.DataFrame({
        "Muskelgruppe": muscle_scores.index,
        "Score in %": muscle_scores.values.round(2)
    })

    table = dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        size="sm",
        className="table-sm small mb-0",
        style={"fontSize": "0.65rem"}
    )

    return html.Div(
        table,
        style={
            "maxHeight": "250px",
            "overflowY": "auto",
            "overflowX": "auto",
            "border": "1px solid #dee2e6",
            "display": "inline-block"
        }
    )


def create_muscle_summary_text(exercise_ids: List[str], factor: float = 1.0) -> html.Div:
    """
    Create a summary text highlighting muscle groups with high stress.

    Args:
        exercise_ids (List[str]): List of selected exercise IDs.
        factor (float): Scaling factor applied to scores.

    Returns:
        html.Div: Summary section with recommendations.
    """
    selected_matrix = MUSCLE_MATRIX.loc[exercise_ids] * factor
    muscle_scores = selected_matrix.sum()
    high_stress = muscle_scores[muscle_scores > 75]

    if high_stress.empty:
        return html.Div([
            html.H6("Keine Gefahr von Übertraining", className="text-success fw-bold"),
            html.P("Du kannst dein Training wie geplant fortsetzen.")
        ])
    else:
        top_muscles = html.Ul([html.Li(m) for m in high_stress.sort_values(ascending=False).index])
        return html.Div([
            html.H6("Stark beanspruchte Muskelgruppen", className="text-warning fw-bold"),
            html.P(
                "Die folgenden Muskelgruppen wurden bereits intensiv beansprucht. "
                "Wir empfehlen, heute weniger Übungen für diese Muskelgruppen zu machen:"
            ),
            top_muscles
        ])


@dash.callback(
    Output("training-progress-container", "children"),
    Input("added-exercises", "data"),
    Input("star-results", "data"),
)
def render_training_progress(
    exercise_ids: Optional[List[str]],
    star_data: Optional[Dict[str, Union[int, float]]]
) -> html.Div:
    """
    Render the training progress view, including:
    - Summary section with muscle scores, SVG visualization, and warnings
    - Cards for each selected exercise with last training info and input table

    Args:
        exercise_ids (Optional[List[str]]): List of selected exercise IDs.
        star_data (Optional[Dict[str, Union[int, float]]]): Star ratings for recovery.

    Returns:
        html.Div: Complete training progress section.
    """
    if not exercise_ids:
        return html.P("Noch keine Übungen hinzugefügt.", className="text-muted")

    # Recovery adjustment factor based on star ratings
    if star_data:
        total_stars = sum(star_data.values())
        star_factor = 1 / (total_stars / 25)
    else:
        star_factor = 1

    def create_last_training_table(ex_id: str) -> html.Div:
        """
        Create a table showing the last training data for a given exercise.
        (Currently static example data.)
        """
        last_training_date = date.today().strftime("%Y-%m-%d")
        training_data = [
            {"Satz": 1, "Wdh": 12, "Gewicht": 40},
            {"Satz": 2, "Wdh": 10, "Gewicht": 42.5},
            {"Satz": 3, "Wdh": 8,  "Gewicht": 45},
        ]
        df = pd.DataFrame(training_data)
        return html.Div([
            html.H6(f"Letztes Training\n({last_training_date})", className="text-muted"),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size="sm", className="mt-2"),
        ])

    def create_input_table(ex_id: str) -> html.Div:
        """
        Create an input table for logging a new training session.
        """
        return html.Div([
            html.H6("Neues Training eintragen", className="mt-4"),
            dag.AgGrid(
                id={"type": "input-grid", "index": ex_id},
                columnDefs=[
                    {"field": "Satz", "editable": True, "type": "numericColumn"},
                    {"field": "Wdh", "editable": True, "type": "numericColumn"},
                    {"field": "Gewicht", "editable": True, "type": "numericColumn"},
                ],
                rowData=[
                    {"Satz": 1, "Wdh": "", "Gewicht": ""},
                    {"Satz": 2, "Wdh": "", "Gewicht": ""},
                    {"Satz": 3, "Wdh": "", "Gewicht": ""},
                ],
                defaultColDef={"flex": 1, "minWidth": 80, "resizable": True},
                className="ag-theme-alpine",
                style={"height": "180px", "width": "100%"},
            ),
            dbc.Button(
                "Training loggen",
                color="success",
                className="mt-2",
                id={"type": "log-training-btn", "index": ex_id}
            ),
        ])

    # Create exercise cards
    cards = []
    for ex_id in exercise_ids:
        title = next((ex["title"] for ex in EXERCISES if ex["id"] == ex_id), ex_id)
        img_src = next((ex["src"] for ex in EXERCISES if ex["id"] == ex_id), "")

        card = dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(html.Img(src=img_src, className="img-fluid rounded", style={"maxWidth": "100%"}), width=5),
                    dbc.Col(html.Div([
                        html.H5(title, className="card-title"),
                        create_last_training_table(ex_id),
                    ]), width=7),
                ]),
                dbc.Row(dbc.Col(create_input_table(ex_id), width=12), className="mt-4")
            ]),
            className="h-100"
        )

        cards.append(dbc.Col(card, md=4))

    # Create summary section with score table, SVG, and recommendations
    summary_section = dbc.Card(
        dbc.Row([
            dbc.Col(create_muscle_score_table(exercise_ids, factor=star_factor), width=4),
            dbc.Col(html.Img(src=get_latest_muscle_svg(), id="muscle-img", style={"width": "100%", "maxWidth": "300px"}), width=4),
            dbc.Col(create_muscle_summary_text(exercise_ids, factor=star_factor), width=4),
        ], className="mb-4 align-items-start"),
        className="p-4 shadow-sm"
    )

    return html.Div([
        summary_section,
        dbc.Row(cards, className="g-4")
    ])
