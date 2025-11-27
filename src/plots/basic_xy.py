from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure


def create_xy_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: Optional[str] = None,
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

    Returns
    -------
    plotly.graph_objs.Figure
        Configured Plotly scatter figure.
    """
    fig: Figure = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=group_col,
        hover_name=None,
        hover_data=df.columns,
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        legend_title=group_col or "Group",
        margin=dict(l=60, r=10, t=40, b=60),
    )

    fig.update_traces(marker=dict(size=8, opacity=0.8))

    return fig
