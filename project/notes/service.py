import pandas as pd

from notes.repository import save_parsed_notes
from notes.serializers import dataframe_to_note_documents


def save_parsed_dataframe(parsed_df: pd.DataFrame):
    """Convert a parsed DataFrame and save it to MongoDB."""

    documents = dataframe_to_note_documents(parsed_df)
    return save_parsed_notes(documents)