import sys

from notes.pipeline.build_pipeline import build_pipeline
from notes.loaders.read_notes_from_csv import read_notes_from_csv
from notes.parsers.parse_notes import parse_notes
from notes.service import save_parsed_dataframe

if __name__ == "__main__":
    """
    Processes notes and produces a dataframe consisting of parsed data fields per note

    args:
        - mrn
    output:
        - df
    """
    mrn = None

    # get MRN arg (if exists only processes 1 mrn at a time)
    for arg in sys.argv[1:]:
        if arg.startswith("mrn="):
            mrn = arg.split("=", 1)[1]
    
    nlp = build_pipeline()
    df = read_notes_from_csv(mrn)


    parsed_df = parse_notes(df, nlp)

    result = save_parsed_dataframe(parsed_df)
    