from __future__ import annotations

from typing import Optional

from plotly.graph_objs import Figure


def apply_publication_style(
    fig: Figure,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    title: Optional[str] = None,
) -> Figure:
    """
    Apply a consistent publication-style layout to a Plotly figure.

    The goal is to produce figures that are directly usable in publications
    (clean background, clear axes, legible fonts).

    Parameters
    ----------
    fig : Figure
        Plotly figure to style.
    x_label : str, optional
        Label for the X axis (can contain LaTeX syntax).
    y_label : str, optional
        Label for the Y axis (can contain LaTeX syntax).
    title : str, optional
        Figure title. Can be None for publication plates.

    Returns
    -------
    Figure
        The same figure instance, modified in-place for convenience.
    """
    base_font_size: int = 14

    fig.update_layout(
        template="simple_white",  # clean white background, no clutter
        font=dict(
            family="Helvetica, Arial, sans-serif",
            size=base_font_size,
        ),
        title=dict(
            text=title or "",
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=base_font_size + 2),
        ),
        margin=dict(l=70, r=20, t=40, b=70),
        legend=dict(
            title=None,
            borderwidth=0,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=base_font_size - 2),
        ),
    )

    fig.update_xaxes(
        title_text=x_label,
        showline=True,
        linewidth=1.5,
        linecolor="black",
        mirror=True,
        ticks="inside",
        tickwidth=1.0,
        ticklen=6,
        showgrid=False,
        zeroline=False,
    )

    fig.update_yaxes(
        title_text=y_label,
        showline=True,
        linewidth=1.5,
        linecolor="black",
        mirror=True,
        ticks="inside",
        tickwidth=1.0,
        ticklen=6,
        showgrid=False,
        zeroline=False,
    )

    fig.update_traces(
        marker=dict(
            size=7,
            opacity=0.85,
            line=dict(width=0.6, color="black"),
        )
    )

    return fig
