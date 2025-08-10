import dash
from dash import html
import dash_bootstrap_components as dbc
from typing import Dict, Any


def create_breadcrumbs(label_link: Dict[str, str]) -> dbc.Breadcrumb:
    """
    Create a breadcrumb navigation component.

    Args:
        label_link (Dict[str, str]): Dictionary mapping breadcrumb labels to their target paths.

    Returns:
        dbc.Breadcrumb: A Bootstrap breadcrumb component.
    """
    return dbc.Breadcrumb(
        items=[
            {
                "label": label,
                "href": dash.get_relative_path(link),
                "external_link": True,
                "active": label == list(label_link)[-1],  # Mark last item as active
            }
            for label, link in label_link.items()
        ]
    )


def create_header(label_link: Dict[str, str]) -> dbc.Navbar:
    """
    Create a page header with breadcrumb navigation.

    Args:
        label_link (Dict[str, str]): Dictionary of breadcrumb labels and links.

    Returns:
        dbc.Navbar: A Bootstrap navbar component containing breadcrumbs.
    """
    return dbc.Navbar(
        [
            html.Div(
                [
                    dbc.Row(
                        [dbc.Col(create_breadcrumbs(label_link=label_link))],
                        className=(
                            "g-0 font-normal opacity-50 transition-all "
                            "hover:text-blue-500 hover:opacity-100 mt-3"
                        ),
                    ),
                ],
            ),
        ],
        className="bg-transparent pb-2.5 me-1 flex flex-col-reverse justify-between gap-6 md:flex-row",
    )


def create_footer() -> html.Footer:
    """
    Create a footer component.

    Returns:
        html.Footer: Footer with credits and year.
    """
    return html.Footer(
        dbc.Container(
            [
                html.A(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P("©2025", className="font-light"),
                                        html.P(
                                            "made by Braig & Scheuring",
                                            className=(
                                                "font-regular antialiased font-mono font-family:'Courier New'"
                                            ),
                                        ),
                                    ],
                                    className=(
                                        "inline-block flex flex-col-reverse justify-end gap-2 "
                                        "md:flex-row md:items-center"
                                    ),
                                )
                            ]
                        )
                    ]
                )
            ],
            fluid=True,
        ),
        className=(
            "inline-block bg-transparent mt-4 flex flex-col-reverse justify-end gap-1 "
            "md:flex-row md:items-center mr-2"
        ),
    )


def create_button(button_id: Dict[str, Any], label: str, color: str, icon_class_name: str) -> dbc.Button:
    """
    Create a Bootstrap button with an icon.

    Args:
        button_id (Dict[str, Any]): Button ID (can be a pattern-matching ID for callbacks).
        label (str): Button text label.
        color (str): Bootstrap button color (e.g., 'success', 'primary').
        icon_class_name (str): CSS class for the icon.

    Returns:
        dbc.Button: Configured button with icon and label.
    """
    return dbc.Button(
        id=button_id,
        children=[html.I(className=icon_class_name), label],
        color=color,
        className="w-100 dbc-button",
        n_clicks=0,
    )


def create_star_rating(question_id: str, question_text: str) -> html.Div:
    """
    Create a star rating component (1–5 stars).

    Args:
        question_id (str): Unique question identifier.
        question_text (str): Text for the question; if it contains a newline,
                             the first line is treated as a headline and the
                             second as a description.

    Returns:
        html.Div: Star rating UI with clickable stars for selection.
    """
    # Split text into headline and optional description
    lines = question_text.split("\n", 1)
    headline = lines[0]
    description = lines[1] if len(lines) > 1 else ""

    return html.Div(
        [
            # Headline and optional description
            html.Div(
                [
                    html.Strong(headline),
                    html.Br(),
                    html.Span(description, style={"whiteSpace": "pre-line"}),
                ],
                className="mb-1",
            ),
            # Star buttons
            html.Div(
                [
                    dbc.Button(
                        html.I(className="bi bi-star"),  # Empty star icon
                        id={"type": "star", "question": question_id, "index": i},
                        color="link",
                        className="p-0 m-0 fs-4",
                        n_clicks=0,
                    )
                    for i in range(1, 6)
                ],
                id=f"stars-{question_id}",
                className="mb-3 d-flex gap-2",
            ),
        ]
    )
