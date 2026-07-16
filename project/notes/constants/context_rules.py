from medspacy.context import ConTextRule

METASTATIC_CONTEXT_RULES = [
    ConTextRule("metastatic to", "METASTATIC", direction="FORWARD"),
    ConTextRule("metastasis to", "METASTATIC", direction="FORWARD"),
    ConTextRule("metastases to", "METASTATIC", direction="FORWARD"),
    ConTextRule("mets to", "METASTATIC", direction="FORWARD"),
    ConTextRule("mets in", "METASTATIC", direction="FORWARD"),
    ConTextRule("metastasis in", "METASTATIC", direction="FORWARD"),
    ConTextRule("metastases in", "METASTATIC", direction="FORWARD"),
]