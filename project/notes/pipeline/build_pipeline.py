import medspacy

from notes.constants.context_rules import METASTATIC_CONTEXT_RULES
from notes.constants.target_rules import PRIMARY_SITE_RULES

def build_pipeline():
    """Create and configure the MedSpaCy primary-site pipeline."""
    nlp = medspacy.load()

    target_matcher = nlp.get_pipe("medspacy_target_matcher")
    target_matcher.add(PRIMARY_SITE_RULES)

    context = nlp.get_pipe("medspacy_context")
    context.add(METASTATIC_CONTEXT_RULES)

    return nlp