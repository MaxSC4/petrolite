from __future__ import annotations

import base64
import io
from typing import Tuple, Optional

import pandas as pd


def parse_uploaded_file(
    contents: str,
    filename: str,
) -> pd.DataFrame:
    """
    Parse a Dash dcc.Upload contents string into a pandas DataFrame.

    Parameters
    ----------
    contents : str
        Base64-encoded contents string from dcc.Upload.
    filename : str
        Original filename, used to infer file type.

    Returns
    -------
    pd.DataFrame
        Parsed DataFrame.

    Raises
    ------
    ValueError
        If the file cannot be parsed or the format is unsupported.
    """
    if "," not in contents:
        raise ValueError("Invalid upload contents format.")

    content_type, content_string = contents.split(",", 1)

    decoded: bytes = base64.b64decode(content_string)

    if filename.lower().endswith(".csv"):
        return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    if filename.lower().endswith((".xls", ".xlsx")):
        return pd.read_excel(io.BytesIO(decoded))

    raise ValueError(f"Unsupported file type: {filename}")


def get_numeric_and_categorical_columns(
    df: pd.DataFrame,
) -> Tuple[list[str], list[str]]:
    """
    Split DataFrame columns into numeric and non-numeric (categorical) lists.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    tuple[list[str], list[str]]
        List of numeric column names and list of non-numeric column names.
    """
    numeric_cols: list[str] = df.select_dtypes(include="number").columns.tolist()
    non_numeric_cols: list[str] = [
        col for col in df.columns if col not in numeric_cols
    ]
    return numeric_cols, non_numeric_cols
