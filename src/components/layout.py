from __future__ import annotations

from typing import Any

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from src.components.controls import create_controls_card
from src.components.plots_area import create_plots_card


def create_layout(app: Dash) -> html.Div:
    """
    Create the main page layout for the application.

    Parameters
    ----------
    app : Dash
        Dash application instance, used if layout requires access to app properties.

    Returns
    -------
    html.Div
        Root layout container.
    """
    return dbc.Container(
        [
            html.H1(
                "Geochemical Diagram Generator",
                className="my-4",
            ),
            html.P(
                "Upload geochemical datasets and create customizable geochemical diagrams.",
                className="text-muted",
            ),
            dcc.Store(id="data-store"),  # stores the uploaded dataframe as JSON
            dbc.Row(
                [
                    dbc.Col(create_controls_card(), md=4),
                    dbc.Col(create_plots_card(), md=8),
                ],
                className="mt-3",
            ),
        ],
        fluid=True,
    )
