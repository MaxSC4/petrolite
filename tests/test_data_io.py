from __future__ import annotations

import base64
import io

import pandas as pd

from src.utils.data_io import parse_uploaded_file, get_numeric_and_categorical_columns


def _make_upload_contents_from_csv(csv_text: str) -> str:
    """
    Helper to simulate dcc.Upload contents string from raw CSV text.
    """
    encoded = base64.b64encode(csv_text.encode("utf-8")).decode("utf-8")
    return f"data:text/csv;base64,{encoded}"


def test_parse_uploaded_file_csv() -> None:
    csv_text = "A,B\n1,2\n3,4\n"
    contents = _make_upload_contents_from_csv(csv_text)
    df = parse_uploaded_file(contents, "test.csv")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["A", "B"]
    assert df.shape == (2, 2)


def test_get_numeric_and_categorical_columns() -> None:
    df = pd.DataFrame(
        {
            "SiO2": [50.1, 52.3],
            "MgO": [7.1, 5.2],
            "RockType": ["basalt", "andesite"],
        }
    )
    num_cols, cat_cols = get_numeric_and_categorical_columns(df)
    assert "SiO2" in num_cols and "MgO" in num_cols
    assert "RockType" in cat_cols
