from __future__ import annotations


from dash import Dash, Input, Output, State, dash_table
from src.utils.data_io import parse_uploaded_file, get_numeric_and_categorical_columns
from src.plots.basic_xy import create_xy_scatter

import dash_bootstrap_components as dbc
import pandas as pd
import io



from src.components.layout import create_layout


def create_app() -> Dash:
    """
    Application factory for the Dash app.

    Returns
    -------
    Dash
        Configured Dash application instance.
    """
    app: Dash = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
        title="Geochemical Diagram Generator",
    )

    app.layout = create_layout(app)

    @app.callback(
        Output("data-store", "data"),
        Output("upload-status", "children"),
        Output("data-preview", "children"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        prevent_initial_call=True,
    )
    def handle_file_upload(contents: str | None, filename: str | None):
        """
        Handle file upload and store parsed dataframe as JSON.

        Returns
        -------
        tuple
            (data_json, status_message, preview_component)
        """
        if contents is None or filename is None:
            raise dash.exceptions.PreventUpdate  # type: ignore[attr-defined]

        try:
            df = parse_uploaded_file(contents, filename)
        except Exception as exc:  # noqa: BLE001
            return None, f"Error reading file: {exc}", ""

        # Basic preview: show first 10 rows
        preview_table = dash_table.DataTable(
            columns=[{"name": c, "id": c} for c in df.columns],
            data=df.head(10).to_dict("records"),
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"fontSize": 12},
        )

        return df.to_json(date_format="iso", orient="split"), f"Loaded file: {filename}", preview_table

    @app.callback(
        Output("x-column-dropdown", "options"),
        Output("y-column-dropdown", "options"),
        Output("group-column-dropdown", "options"),
        Input("data-store", "data"),
    )
    def update_column_dropdowns(data_json: str | None):
        """
        Update dropdown options based on uploaded dataframe.

        Parameters
        ----------
        data_json : str | None
            JSON representation of the dataframe.

        Returns
        -------
        tuple
            Options for X, Y, and group dropdowns.
        """
        if data_json is None:
            return [], [], []

        df = pd.read_json(io.StringIO(data_json), orient="split")
        numeric_cols, non_numeric_cols = get_numeric_and_categorical_columns(df)

        numeric_options = [{"label": col, "value": col} for col in numeric_cols]
        group_options = [{"label": col, "value": col} for col in non_numeric_cols]

        return numeric_options, numeric_options, group_options

    @app.callback(
        Output("main-graph", "figure"),
        Input("x-column-dropdown", "value"),
        Input("y-column-dropdown", "value"),
        Input("group-column-dropdown", "value"),
        Input("data-store", "data"),
    )
    def update_main_graph(
        x_col: str | None,
        y_col: str | None,
        group_col: str | None,
        data_json: str | None,
    ):
        """
        Update the main graph when axes, group, or data change.

        Returns
        -------
        plotly.graph_objs.Figure
            Scatter figure or empty figure if requirements are not met.
        """
        import plotly.graph_objects as go
        import pandas as pd

        if data_json is None or x_col is None or y_col is None:
            return go.Figure()

        df = pd.read_json(io.StringIO(data_json), orient="split")

        fig = create_xy_scatter(df, x_col, y_col, group_col)
        return fig


    return app


# Global app instance used by Dash
app: Dash = create_app()
