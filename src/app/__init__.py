from __future__ import annotations


from dash import Dash, Input, Output, State, dash_table
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import io

from src.components.layout import create_layout
from src.utils.data_io import parse_uploaded_file, get_numeric_and_categorical_columns
from src.plots.basic_xy import create_xy_scatter
from src.plots.harker import create_harker_scatter



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
        Input("diagram-type-radio", "value"),
        Input("x-column-dropdown", "value"),
        Input("y-column-dropdown", "value"),
        Input("group-column-dropdown", "value"),
        Input("data-store", "data"),
    )
    def update_main_graph(
        diagram_type: str,
        x_col: str | None,
        y_col: str | None,
        group_col: str | None,
        data_json: str | None,
    ):
        """
        Update the main graph when diagram type, axes, group, or data change.

        Parameters
        ----------
        diagram_type : str
            Selected diagram type ("custom" or "harker").
        x_col : str | None
            Selected X-axis column for custom diagrams.
        y_col : str | None
            Selected Y-axis column.
        group_col : str | None
            Selected grouping (color by) column.
        data_json : str | None
            JSON representation of the dataframe.

        Returns
        -------
        plotly.graph_objs.Figure
            Updated figure based on current settings.
        """
        import plotly.graph_objects as go

        if data_json is None or y_col is None:
            return go.Figure()

        df = pd.read_json(io.StringIO(data_json), orient="split")

        # Harker mode: X is locked to SiO2
        if diagram_type == "harker":
            try:
                fig = create_harker_scatter(
                    df=df,
                    y_col=y_col,
                    group_col=group_col,
                    base_col="SiO2",
                )
            except ValueError as exc:
                # If SiO2 is missing, show an empty figure with an informative title
                fig = go.Figure()
                fig.update_layout(
                    title=str(exc),
                    xaxis_title="",
                    yaxis_title="",
                )
            return fig

        # Default: custom X-Y diagram
        if x_col is None:
            return go.Figure()

        fig = create_xy_scatter(df, x_col, y_col, group_col)
        return fig

    @app.callback(
        Output("x-column-dropdown", "disabled"),
        Input("diagram-type-radio", "value"),
    )
    def toggle_x_dropdown_disabled(diagram_type: str) -> bool:
        """
        Disable the X-axis dropdown when Harker mode is selected,
        since the X axis is fixed to SiO2.

        Parameters
        ----------
        diagram_type : str
            Selected diagram type.

        Returns
        -------
        bool
            True if the X-axis dropdown should be disabled, False otherwise.
        """
        return diagram_type == "harker"



    return app


# Global app instance used by Dash
app: Dash = create_app()
