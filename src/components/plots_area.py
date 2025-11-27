from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_plots_card() -> dbc.Card:
    """
    Create the right-hand plot display card.

    Returns
    -------
    dbc.Card
        Card containing data preview and main plot.
    """
    return dbc.Card(
        [
            dbc.CardHeader("Data Preview & Plot"),
            dbc.CardBody(
                [
                    html.H6("Data preview"),
                    html.Div(
                        id="data-preview",
                        className="mb-3",
                    ),
                    html.H6("Diagram"),
                    dcc.Graph(
                        id="main-graph",
                        figure={},
                        style={"height": "500px"},
                    ),
                ]
            ),
        ],
        className="h-100",
    )
