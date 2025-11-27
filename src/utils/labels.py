from __future__ import annotations

from typing import Dict


# Basic mapping for common oxide names: LaTeX-style labels
COLUMN_LABEL_MAP: Dict[str, str] = {
    "SiO2":  r"$\mathrm{SiO_2}\,\text{(wt.\%)}$",
    "TiO2":  r"$\mathrm{TiO_2}\,\text{(wt.\%)}$",
    "Al2O3": r"$\mathrm{Al_2O_3}\,\text{(wt.\%)}$",
    "FeO":   r"$\mathrm{FeO}\,\text{(wt.\%)}$",
    "Fe2O3": r"$\mathrm{Fe_2O_3}\,\text{(wt.\%)}$",
    "FeO*":  r"$\mathrm{FeO^*}\,\text{(wt.\%)}$",
    "MnO":   r"$\mathrm{MnO}\,\text{(wt.\%)}$",
    "MgO":   r"$\mathrm{MgO}\,\text{(wt.\%)}$",
    "CaO":   r"$\mathrm{CaO}\,\text{(wt.\%)}$",
    "Na2O":  r"$\mathrm{Na_2O}\,\text{(wt.\%)}$",
    "K2O":   r"$\mathrm{K_2O}\,\text{(wt.\%)}$",
    "P2O5":  r"$\mathrm{P_2O_5}\,\text{(wt.\%)}$",
    "Na2O+K2O": r"$\mathrm{Na_2O + K_2O}\,\text{(wt.\%)}$",
    "Mg#":   r"$\mathrm{Mg\#}$",
}


def get_pretty_label(column_name: str) -> str:
    """
    Map a dataframe column name to a human-readable, LaTeX-style axis label.

    Parameters
    ----------
    column_name : str
        Original column name in the dataframe.

    Returns
    -------
    str
        Label string suitable for Plotly, using LaTeX syntax when possible.
    """
    if column_name in COLUMN_LABEL_MAP:
        return COLUMN_LABEL_MAP[column_name]

    # Fallback: replace underscores with spaces and keep as plain text
    clean_name = column_name.replace("_", " ")
    return clean_name
