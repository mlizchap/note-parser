from typing import Any

import pandas as pd

def normalize_primary_site(value) -> str | None:
    if value is None or pd.isna(value):
        return None

    value = str(value).strip()

    if not value or value.upper() == "UNKNOWN":
        return None

    return value

def parse_pipe_delimited(value: Any) -> list[str]:
    """
    Convert a pipe-delimited field into a list.

    Examples:
        "testis | mediastinum" -> ["testis", "mediastinum"]
        "UNKNOWN" -> []
        None -> []
    """

    if value is None:
        return []

    # Only use pd.isna on scalar values.
    if not isinstance(value, (list, tuple, set, dict, pd.Series, pd.DataFrame)):
        if pd.isna(value):
            return []

    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, (pd.Series, pd.DataFrame)):
        raise TypeError(
            "Expected one cell value, but received a pandas "
            f"{type(value).__name__}."
        )

    text = str(value).strip()

    if not text or text.upper() == "UNKNOWN":
        return []

    return [
        item.strip()
        for item in text.split("|")
        if item.strip()
    ]


def dataframe_to_note_documents(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Convert each parsed DataFrame row into a MongoDB document."""

    required_columns = {"mrn", "note_text"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df.columns.duplicated().any():
        duplicates = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate DataFrame columns found: {duplicates}")

    documents = []

    for row in df.to_dict(orient="records"):
        documents.append(
            {
                "mrn": str(row["mrn"]),
                "note_name": row.get("note_name"),
                "note_date": row.get("note_date"),
                "note_text": str(row.get("note_text", "")),
                # "primary_site": normalize_primary_site(
                #     row.get("primary_site")
                # ),
                "primary_site": row.get("primary_site"),
                "histology": parse_pipe_delimited(
                    row.get("histology")
                ),
                "source": row.get("source"),
                "source_note_id": row.get("source_note_id"),
            }
        )

    return documents