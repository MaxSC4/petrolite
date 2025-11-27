from __future__ import annotations

from typing import Optional

import pandas as pd
from plotly.graph_objs import Figure

from src.plots.basic_xy import create_xy_scatter
from src.utils.labels import get_pretty_label
from src.utils.plot_style import apply_publication_style


def create_harker_scatter(
    df: pd.DataFrame,
    y_col: str,
    group_col: Optional[str] = None,
    base_col: str = "SiO2",
) -> Figure:
    """
    Create a Harker-style diagram (base_col vs y_col) with publication styling.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing geochemical data.
    y_col : str
        Oxide column plotted on the Y axis (e.g., MgO, FeO, CaO).
    group_col : str, optional
        Column used to color points by group (e.g., rock type).
    base_col : str, optional
        Column used as the Harker base axis, typically "SiO2".

    Returns
    -------
    plotly.graph_objs.Figure
        Harker-style scatter figure with publication-style layout.

    Raises
    ------
    ValueError
        If the base_col is not present in the dataframe.
    """
    if base_col not in df.columns:
        raise ValueError(
            f'Harker diagram requires column "{base_col}" in the dataset.'
        )

    pretty_x = get_pretty_label(base_col)
    pretty_y = get_pretty_label(y_col)
    title = f"Harker diagram: {pretty_y} vs {pretty_x}"

    fig: Figure = create_xy_scatter(
        df=df,
        x_col=base_col,
        y_col=y_col,
        group_col=group_col,
        title=title,
    )

    fig = apply_publication_style(
        fig=fig,
        x_label=pretty_x,
        y_label=pretty_y,
        title=title,
    )

    return fig
