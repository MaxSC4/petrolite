from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure

from src.utils.labels import get_pretty_label
from src.utils.plot_style import apply_publication_style


def create_xy_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: Optional[str] = None,
    title: Optional[str] = None,
) -> Figure:
    """
    Create a simple X vs Y scatter plot for geochemical data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing geochemical data.
    x_col : str
        Column name to use for the X axis.
    y_col : str
        Column name to use for the Y axis.
    group_col : str, optional
        Column name used to color points by group (e.g., rock type).
    title : str, optional
        Plot title. If None, a generic "X vs Y" title is used.

    Returns
    -------
    plotly.graph_objs.Figure
        Configured Plotly scatter figure with publication-style layout.
    """
    pretty_x = get_pretty_label(x_col)
    pretty_y = get_pretty_label(y_col)

    if title is None:
        title = f"{pretty_y} vs {pretty_x}"

    fig: Figure = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=group_col,
        hover_name=None,
        hover_data=df.columns,
    )

    fig = apply_publication_style(
        fig=fig,
        x_label=pretty_x,
        y_label=pretty_y,
        title=title,
    )

    return fig
