import medspacy
from medspacy.ner import TargetRule
from medspacy.visualization import visualize_ent

nlp = medspacy.load()

target_matcher = nlp.get_pipe("medspacy_target_matcher")

target_matcher.add([
    TargetRule("seminoma", "HISTOLOGY"),
    TargetRule("NSGCT", "HISTOLOGY"),
    TargetRule("lung", "ANATOMIC_SITE"),
    TargetRule("testis", "ANATOMIC_SITE"),
])

text = """
Chief complaint:
No evidence of seminoma.
NSGCT of the right testis with metastatic disease to the lung.
assessment: abc
"""

doc = nlp(text)

html = visualize_ent(doc, jupyter=False)

with open("medspacy_visualization.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved visualization to medspacy_visualization.html")