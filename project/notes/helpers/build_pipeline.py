import medspacy

from contstants.target_rules import PRIMARY_SITE_RULES
from contstants.context_rules import METASTATIC_CONTEXT_RULES
# from project.notes.contstants.section_rules import 

def build_pipeline():
    """Create and configure the MedSpaCy primary-site pipeline."""
    nlp = medspacy.load()

    target_matcher = nlp.get_pipe("medspacy_target_matcher")
    target_matcher.add(PRIMARY_SITE_RULES)

    context = nlp.get_pipe("medspacy_context")
    context.add(METASTATIC_CONTEXT_RULES)

    return nlp
    # """Build and configure the MedSpaCy NLP pipeline."""

    # nlp = medspacy.load()

    # #
    # # Sectionizer
    # #
    # # sectionizer = nlp.add_pipe(
    # #     "medspacy_sectionizer",
    # #     config={"rules": None},
    # #     last=True,
    # # )
    # # sectionizer.add(NOTE_SECTION_RULES)

    # #
    # # Target Matcher
    # #
    # target_matcher = nlp.get_pipe("medspacy_target_matcher")
    # target_matcher.add(PRIMARY_SITE_RULES)

    # #
    # # Context
    # #
    # context = nlp.get_pipe("medspacy_context")
    # context.add(METASTATIC_CONTEXT_RULES)

    # return nlp