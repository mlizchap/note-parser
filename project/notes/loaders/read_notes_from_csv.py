from pathlib import Path
import pandas as pd


# def read_notes_from_csv(
#     csv_path: str | Path,
#     mrn: str | None = None,
# ) -> pd.DataFrame:
#     """
#     Read clinical notes from a CSV.

#     Required columns:
#         - mrn
#         - note_text

#     Optional columns:
#         - note_name
#         - any additional metadata
#     """

#     df = pd.read_csv(csv_path, dtype={"mrn": str})

#     required_columns = {"mrn", "note_text"}
#     missing_columns = required_columns - set(df.columns)

#     if missing_columns:
#         raise ValueError(
#             f"Missing required columns: {sorted(missing_columns)}"
#         )

#     if mrn is not None:
#         df = df[df["mrn"] == str(mrn)]

#     return df.reset_index(drop=True)
def read_notes_from_csv(mrn: str | None = None) -> pd.DataFrame:

    """PLACEHOLDER for fetching data from Palantir."""
    # TO update: use read_notes_from_csv(csv_path, mrn)
    notes_data = [
        {
            "mrn": "111",
            "note_name": "Initial Consultation",
            "note_text": "primary mediastinal NSGCT.",
        },
        {
            "mrn": "333",
            "note_name": "Initial Consultation",
            "note_text": "presents for testis cancer.",
        },
        {
            "mrn": "444",
            "note_name": "Initial Consultation",
            "note_text": "testicular germ cell seminoma.",
        },
    ]

    df = pd.DataFrame(notes_data)

    if mrn is not None:
        df = df[df["mrn"] == mrn]

    return df