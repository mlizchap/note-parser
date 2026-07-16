import re
import sys

import medspacy
import pandas as pd
from loguru import logger
from medspacy.context import ConTextRule
from medspacy.ner import TargetRule
# from extract_fields_from_notes.contstants.context import METASTATIC_CONTEXT_RULES
# from extract_fields_from_notes.contstants.targets import PRIMARY_SITE_RULES

logger.remove()

# def build_primary_site_pipeline():
#     """Create and configure the MedSpaCy primary-site pipeline."""
#     nlp = medspacy.load()

#     target_matcher = nlp.get_pipe("medspacy_target_matcher")
#     target_matcher.add(PRIMARY_SITE_RULES)

#     context = nlp.get_pipe("medspacy_context")
#     context.add(METASTATIC_CONTEXT_RULES)

#     return nlp


def has_context_modifier(ent, category: str) -> bool:
    """Return whether an entity has a ConText modifier category."""
    expected = category.upper()

    for modifier in ent._.modifiers:
        modifier_category = getattr(modifier, "category", "")

        if not modifier_category:
            rule = getattr(modifier, "rule", None)
            modifier_category = getattr(rule, "category", "")

        if str(modifier_category).upper() == expected:
            return True

    return False


def is_current(ent) -> bool:
    """Return whether an entity describes current patient disease."""
    return (
        not ent._.is_negated
        and not ent._.is_historical
        and not ent._.is_family
        and not ent._.is_hypothetical
        and not ent._.is_uncertain
        and not has_context_modifier(ent, "METASTATIC")
    )


def canonical_primary_site(ent) -> str:
    """Normalize extracted primary-site text."""
    text = ent.text.strip().lower()

    if "testi" in text:
        return "testis"

    return text


def split_note_into_clauses(note_text: str) -> list[str]:
    """Split a note into independently processed clauses."""
    return [
        clause.strip()
        for clause in re.split(r"(?<=[.;])\s+|\n+", str(note_text))
        if clause.strip()
    ]


def extract_primary_sites_from_note(note_text: str, nlp) -> list[str]:
    """Extract canonical current primary sites from one clinical note."""
    primary_sites = []

    for clause in split_note_into_clauses(note_text):
        doc = nlp(clause)

        primary_sites.extend(
            canonical_primary_site(ent)
            for ent in doc.ents
            if ent.label_ == "PRIMARY_SITE" and is_current(ent)
        )

    return list(dict.fromkeys(primary_sites))


def parse_notes(df: pd.DataFrame, nlp) -> pd.DataFrame:
    """Extract primary sites from every note in a DataFrame."""
    # required_columns = {"mrn", "note_text"}
    # missing_columns = required_columns - set(df.columns)

    # if missing_columns:
    #     raise ValueError(
    #         f"Missing required columns: {sorted(missing_columns)}"
    #     )

    results = []

    for row in df.itertuples(index=False):
        primary_sites = extract_primary_sites_from_note(
            row.note_text,
            nlp,
        )

        row_dict = row._asdict()

        results.append(
            {
                "mrn": row.mrn,
                "primary_site": (
                    " | ".join(primary_sites)
                    if primary_sites
                    else "UNKNOWN"
                ),
                **{
                    k: v
                    for k, v in row_dict.items()
                    if k != "mrn"
                },
            }
        )

    return pd.DataFrame(results)




# def parse_notes(mrn):
#     """
#     Takes in an mrn and returns and the original notes_df and returns a df with extracted datafields
#     """
#     # nlp = build_primary_site_pipeline()
#     # notes_df = read_notes_from_palantir(mrn)
#     # result_df = extract_primary_sites(notes_df, nlp)

#     # if result_df.empty:
#     #     raise ValueError(f"MRN '{mrn}' not found in dataset.")
    
#     # check for proper col names in dataset
#         # if missing -> throw error improper cols: expected [col list]

#     # add fields to df
#     # for each row in result_df
#         # dx_date = extract_field_note(row.note_text, "dx_date")
#         # igcccg_risk_group = extract_field_note(row.note_text, "igcccg_risk_group")
#         # ... other fields
        
#         # add to df:
#         #     add field val to row, dx_date (lit): dx_date (val)
    
#     print(result_df)
#     return result_df

# # if __name__ == "__main__":
# #     """
# #     Parses notes for an MRN
# #     """
# #     mrn = None

# #     # get MRN arg (if exists only processes 1 mrn at a time)
# #     for arg in sys.argv[1:]:
# #         if arg.startswith("mrn="):
# #             mrn = arg.split("=", 1)[1]

# #     nlp = build_primary_site_pipeline()
# #     notes_df = read_notes_from_palantir(mrn)
# #     result_df = extract_primary_sites(notes_df, nlp)

# #     # add fields to df
# #     # for each row in result_df
# #         # dx_date = extract_field_note(row.note_text, "dx_date")
# #         # igcccg_risk_group = extract_field_note(row.note_text, "igcccg_risk_group")
# #         # ... other fields
        
# #         # add to df:
# #             # add field val to row, dx_date (lit): dx_date (val)
    
# #     # return df
# #     print(result_df)