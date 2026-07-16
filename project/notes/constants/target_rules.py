from medspacy.ner import TargetRule

PRIMARY_SITE_RULES = [
    TargetRule("testis", "PRIMARY_SITE"),
    TargetRule("testicular", "PRIMARY_SITE"),
    TargetRule("lung", "PRIMARY_SITE"),
    TargetRule("liver", "PRIMARY_SITE"),
    TargetRule("mediastinum", "PRIMARY_SITE"),
    TargetRule("mediastinal", "PRIMARY_SITE"),
    TargetRule("breast", "PRIMARY_SITE"),
]