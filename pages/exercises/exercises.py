import os
import time
import xml.etree.ElementTree as ET
from typing import Dict, List, Any

import dash
from dash import html, Input, Output, State, ctx, MATCH, ALL
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from mistralai import Mistral

from pages.exercises.layout import create_layout
from constants import MUSCLE_SVG_MAPPING, MUSCLE_MATRIX

# Dash Page Registration
dash.register_page(__name__)
layout = create_layout()

# Load environment variables and Mistral setup
load_dotenv()
api_key = os.environ.get("MISTRAL_API_KEY")
model = "mistral-small-latest"
client = Mistral(api_key=api_key)


def classify_score(score: float) -> str:
    """
    Classify a numeric muscle load score into a specific color code.

    Args:
        score (float): Calculated load score for the muscle.

    Returns:
        str: Corresponding hex color code for visualization.
    """
    if score < 10:
        return "#5cf3aa"  # light green
    elif score < 40:
        return "#33b535ff"  # green
    elif score < 70:
        return "#f1f826"  # yellow
    elif score < 100:
        return "#dda304"  # orange
    elif score < 130:
        return "#f71c1c"  # red
    else:
        return "#7f0400"  # dark red


@dash.callback(
    Output({"type": "exercise-output", "index": MATCH}, "children"),
    Input({"type": "exercise-img", "index": MATCH}, "n_clicks"),
    State("health_state", "data"),
    State({"type": "exercise-img", "index": MATCH}, "id"),
)
def analyze_exercise(
    n_clicks: int,
    health_data: Dict[str, Any],
    img_id: Dict[str, str]
):
    """
    Analyze whether a selected exercise is suitable based on the user's health state.
    Uses Mistral AI for natural language assessment.

    Returns:
        - A recommendation card with a traffic light (🔴 🟡 🟢) and explanation.
        - If no health data is provided, a warning alert is returned.
    """
    if not n_clicks:
        return ""

    if health_data is None:
        return dbc.Alert("⚠️ Bitte zuerst deinen Gesundheitszustand eingeben.", color="warning")

    complaints_text = (
        (health_data.get("longterm_text") or "")
        + " "
        + (health_data.get("shortterm_text") or "")
    ).strip()
    exercise = img_id["index"]

    # Prompt (left exactly as you provided)
    prompt = (
        f"Beschwerden: {complaints_text if complaints_text else 'keine'}\n"
        f"Übung: {exercise}\n\n"
        """Du bist ein erfahrener Sportwissenschaftler und Fitnesscoach. Eine Person fragt dich, ob sie eine bestimmte Übung durchführen kann. Sie beschreibt ihre Beschwerden – dabei können sowohl chronische (langfristige) als auch akute (heutige) Probleme vorkommen.

    Bitte bewerte die Übung basierend auf diesen Beschwerden. Gib deine Einschätzung immer im folgenden Stil:

    Beginne mit einem Ampel-Emoji und einer kurzen Einschätzung:
    - 🔴 Nicht empfohlen
    - 🟡 Mit Vorsicht möglich
    - 🟢 Unbedenklich

    Nur wenn die Bewertung 🔴 oder 🟡 ist, gib bitte eine kurze, klare Begründung.  
    Wenn du 🔴 vergibst, erkläre, warum die betroffenen Muskel- oder Gelenkbereiche unbedingt geschont werden sollten und welche Folgen eine Belastung hätte.
    Wenn du 🟡 vergibst, beschreibe konkret, worauf bei der Ausführung geachtet werden sollte oder welche Varianten schonender sind.
    Wenn du 🟢 vergibst, schreibe **🟢 Unbedenklich** und keine weitere Erklärung.

    Schreibe im natürlichen, professionellen Stil. Keine Aufzählungen, keine Floskeln, keine Einleitung oder Verabschiedung.

    ---
    Beispiele:

    Input:
    - Beschwerden: Knieschmerzen bei zu starker Beugung der Beine
    - Übung: Kniebeugen (Langhantel)

    Antwort:
    🟡 Mit Vorsicht möglich: Tiefe Kniebeugen sollten vermieden werden, da starke Beugung die Schmerzen verstärken kann. Empfehlenswert sind Teilwiederholungen bis ca. 90 Grad und der Einsatz von Widerstandsbändern statt Zusatzgewicht.

    Input:
    - Beschwerden: Akute Rückenschmerzen im unteren Rückenbereich
    - Übung: Kreuzheben (konventionell)

    Antwort:
    🔴 Nicht empfohlen: Der untere Rücken sollte derzeit unbedingt geschont werden, da jede zusätzliche Belastung zu einer Verschlimmerung der Beschwerden oder zu einer strukturellen Reizung führen kann.

    Input:
    - Beschwerden: Keine
    - Übung: Liegestütze

    Antwort:
    🟢 Unbedenklich

    Input:
    - Beschwerden: Schulterinstabilität bei Überkopfbewegungen
    - Übung: Schulterdrücken mit Kurzhanteln

    Antwort:
    🔴 Nicht empfohlen: Die Schulter sollte bei Instabilität nicht über Kopf belastet werden, da dies die Gelenkkapsel zusätzlich reizt und zu Ausrenkungen führen kann.

    Input:
    - Beschwerden: Leichtes Ziehen in der Oberschenkelrückseite nach dem Joggen
    - Übung: Beincurls (Maschine)

    Antwort:
    🟡 Mit Vorsicht möglich: Nur mit leichtem Gewicht und kontrollierter Ausführung. Ein sorgfältiges Warm-up und Dehnen der hinteren Oberschenkelmuskulatur vorab ist wichtig.

    Input:
    - Beschwerden: Keine
    - Übung: Klimmzüge (weiter Griff)

    Antwort:
    🟢 Unbedenklich
    """
    )

    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = chat_response.choices[0].message.content.strip()

        return dbc.Card(
            dbc.CardBody([
                html.P(response_text, className="mb-3"),
                html.Div(
                    id={"type": "exercise-feedback", "index": img_id["index"]},
                    className="mt-2"
                )
            ]),
            className="mt-3"
        )

    except Exception as e:
        return dbc.Alert(f"⚠️ Fehler bei der KI-Antwort: {str(e)}", color="danger")


@dash.callback(
    Output({"type": "exercise-feedback", "index": MATCH}, "children"),
    Input({"type": "add-exercise-btn", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def show_added_feedback(n_clicks: int):
    """Show feedback when a user adds an exercise."""
    if n_clicks:
        return "✅ Übung wurde hinzugefügt."
    raise dash.exceptions.PreventUpdate


@dash.callback(
    Output("added-exercises", "data"),
    Input({"type": "add-exercise-btn", "index": ALL}, "n_clicks"),
    State({"type": "add-exercise-btn", "index": ALL}, "id"),
    State("added-exercises", "data"),
    prevent_initial_call=True
)
def store_added_exercise(
    n_clicks_list: List[int],
    ids: List[Dict[str, str]],
    current_data: List[str]
) -> List[str]:
    """Store selected exercises in session state."""
    if not any(n_clicks_list):
        raise dash.exceptions.PreventUpdate

    triggered = ctx.triggered_id
    if not isinstance(triggered, dict) or "index" not in triggered:
        raise dash.exceptions.PreventUpdate

    ex_id = triggered["index"]
    if current_data is None:
        current_data = []
    if ex_id not in current_data:
        current_data.append(ex_id)

    return current_data


@dash.callback(
    Output("muscle-img", "src"),
    Input("added-exercises", "data"),
    Input("star-results", "data")
)
def update_muscle_svg(exercise_ids: List[str], star_data: Dict[str, int]) -> str:
    """
    Update SVG muscle diagram colors based on exercise selection
    and star rating factor.
    """
    if not exercise_ids:
        raise dash.exceptions.PreventUpdate

    if star_data:
        total_stars = sum(star_data.values())
        star_factor = 1 / (total_stars / 25)
    else:
        star_factor = 1

    muscle_scores = (MUSCLE_MATRIX.loc[exercise_ids] * star_factor).sum()

    muscle_to_color = {
        muscle: classify_score(score)
        for muscle, score in muscle_scores.items()
        if score >= 0.3
    }

    input_file = "assets/muscle_sections.svg"
    output_filename = f"muscle_dynamic_{int(time.time())}.svg"
    output_path = f"assets/{output_filename}"
    ns = {"svg": "http://www.w3.org/2000/svg"}

    tree = ET.parse(input_file)
    root = tree.getroot()

    for muscle, color in muscle_to_color.items():
        if muscle not in MUSCLE_SVG_MAPPING:
            continue

        group_id = MUSCLE_SVG_MAPPING[muscle]["group"]
        path_ids = MUSCLE_SVG_MAPPING[muscle]["paths"]

        for g in root.findall(".//svg:g", ns):
            if g.attrib.get("id") == group_id:
                style = g.attrib.get("style", "")
                g.attrib["style"] = style.replace("display:none", "display:inline")

        for path in root.findall(".//svg:path", ns):
            if path.attrib.get("id") in path_ids:
                style = path.attrib.get("style", "")
                parts = [s for s in style.split(";") if s.strip()]
                updated = []
                filled = False
                for p in parts:
                    if p.strip().startswith("fill:"):
                        updated.append(f"fill:{color}")
                        filled = True
                    else:
                        updated.append(p)
                if not filled:
                    updated.append(f"fill:{color}")
                path.attrib["style"] = ";".join(updated)

    tree.write(output_path)
    return dash.get_asset_url(output_filename)
