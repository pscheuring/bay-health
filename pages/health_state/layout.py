from dash import html
import dash_bootstrap_components as dbc

from utils import create_footer, create_header, create_star_rating


def create_layout():
    return html.Div(
        dbc.Container(
            [
                create_header(label_link={"Bay Health": "/", "Übungsauswahl": ""}),

                # Gesundheitsabfrage (Input-Section als Card)
                dbc.Card(
                    dbc.CardBody([
                        html.H2(
                            "Gesundheitszustand",
                            className="text-xl font-bold mb-6",
                            style={"color": "rgb(69, 155, 112)"},
                        ),

                        # Langfristige Beschwerden
                        html.Div([
                            html.Label("Hast du langfristige gesundheitliche Beschwerden (z. B. chronische Schmerzen)?", className="text-sm fw-bold"),
                            dbc.RadioItems(
                                id="longterm-complaints-choice",
                                options=[{"label": "Ja", "value": "ja"}, {"label": "Nein", "value": "nein"}],
                                value="nein",
                                inline=True,
                            ),
                            dbc.Collapse(
                                dbc.Textarea(
                                    id="longterm-complaints-text",
                                    placeholder="Bitte beschreibe deine Beschwerden...",
                                    className="mt-2",
                                ),
                                id="longterm-collapse",
                                is_open=False,
                            ),
                        ], className="mb-4"),

                        # Kurzfristige Beschwerden
                        html.Div([
                            html.Label("Hast du heute körperliche Beschwerden?", className="text-sm fw-bold"),
                            dbc.RadioItems(
                                id="shortterm-complaints-choice",
                                options=[{"label": "Ja", "value": "ja"}, {"label": "Nein", "value": "nein"}],
                                value="nein",
                                inline=True,
                            ),
                            dbc.Collapse(
                                dbc.Textarea(
                                    id="shortterm-complaints-text",
                                    placeholder="Was genau hast du heute?",
                                    className="mt-2",
                                ),
                                id="shortterm-collapse",
                                is_open=False,
                            ),
                        ], className="mb-4"),

                        html.Label(
                            "Bewerte deinen aktuellen Zustand anhand der folgenden Aussagen:",
                            className="text-sm fw-bold text-success",
                            style={"marginTop": "2rem"},
                        ),

                        create_star_rating("q1", "1. Körperliches Wohlbefinden:\nFühlst du dich körperlich beschwerdefrei? 👉 1 = sehr starke Beschwerden / 5 = keine Beschwerden"),
                        create_star_rating("q2", "2. Schlafqualität:\nWie gut schläfst du aktuell? 👉 1 = sehr schlechter Schlaf / 5 = sehr erholsamer Schlaf"),
                        create_star_rating("q3", "3. Energie und Appetit:\nFühlst du dich energiegeladen? 👉 1 = energielos / 5 = voller Energie"),
                        create_star_rating("q4", "4. Mentale Klarheit:\nWie klar fühlst du dich mental? 👉 1 = unklar / 5 = sehr klar"),
                        create_star_rating("q5", "5. Emotionale Ausgeglichenheit:\nWie ausgeglichen bist du? 👉 1 = gereizt / 5 = ruhig"),
                        create_star_rating("q6", "6. Motivation und Lebensfreude:\nWie motiviert bist du aktuell? 👉 1 = unmotiviert / 5 = motiviert"),

                        dbc.Button(
                            "Gesundheitsdaten speichern",
                            id="start-training-btn",
                            color="success",
                            className="mt-4",
                            n_clicks=0,
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Gesundheitszustand gespeichert")),
                                dbc.ModalBody(
                                    "Gesundheitszustand erfolgreich gespeichert. "
                                    "Gehe im nächsten Schritt zur Übungsauswahl, um dir anzeigen zu lassen, "
                                    "welche Übungen für dich geeignet sind und passende Übungen auszuwählen."
                                ),
                                dbc.ModalFooter(
                                    dbc.Button("OK", 
                                               id="close-health-modal", 
                                               className="ms-auto", 
                                               n_clicks=0, 
                                               style={
                                                        "backgroundColor": "rgb(71, 158, 116)",
                                                        "borderColor": "rgb(71, 158, 116)",
                                                        "color": "white"
                                                    }
                                    )
                                ),
                            ],
                            id="health-confirm-modal",
                            is_open=False,
                        ),
                    ]),
                    className="bg-white p-6 rounded-2xl shadow max-w-[90rem] mx-auto mt-8",
                ),
                create_footer(),
            ],
            fluid=True
        )
    )
