from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_controls_card() -> dbc.Card:
    """
    Create the left-hand control panel card.

    Returns
    -------
    dbc.Card
        Card containing upload component and plot controls.
    """
    return dbc.Card(
        [
            dbc.CardHeader("Data & Plot Settings"),
            dbc.CardBody(
                [
                    html.H6("1. Upload data file", className="card-title"),
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            ["Drag and Drop or ", html.A("Select a CSV/XLSX file")]
                        ),
                        style={
                            "width": "100%",
                            "height": "70px",
                            "lineHeight": "70px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "marginBottom": "10px",
                        },
                        multiple=False,
                    ),
                    html.Div(
                        id="upload-status",
                        className="text-muted small mb-3",
                    ),
                    html.H6("2. Diagram type", className="card-title mt-2"),
                    dbc.RadioItems(
                        id="diagram-type-radio",
                        options=[
                            {"label": "Custom X-Y", "value": "custom"},
                            {"label": "Harker (SiO2 vs oxide)", "value": "harker"},
                        ],
                        value="custom",
                        inline=False,
                        className="mb-2",
                    ),
                    html.H6("3. Select axes", className="card-title mt-3"),
                    dbc.Label("X-axis"),
                    dcc.Dropdown(
                        id="x-column-dropdown",
                        placeholder="Select X column",
                        options=[],
                        value=None,
                        clearable=False,
                    ),
                    dbc.Label("Y-axis", className="mt-2"),
                    dcc.Dropdown(
                        id="y-column-dropdown",
                        placeholder="Select Y column",
                        options=[],
                        value=None,
                        clearable=False,
                    ),
                    dbc.Label("Group (color by)", className="mt-2"),
                    dcc.Dropdown(
                        id="group-column-dropdown",
                        placeholder="Optional grouping column",
                        options=[],
                        value=None,
                        clearable=True,
                    ),

                ]
            ),
        ],
        className="h-100",
    )
