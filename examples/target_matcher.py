import medspacy
from medspacy.section_detection import SectionRule
from medspacy.ner import TargetRule

nlp = medspacy.load()

# Add the sectionizer because it is not currently in the pipeline
sectionizer = nlp.add_pipe(
    "medspacy_sectionizer",
    config={"rules": None},
)

sectionizer.add(
    [
        SectionRule("chief complaint:", "CHIEF COMPLAINT"),
    ]
)


target_matcher = nlp.get_pipe("medspacy_target_matcher")
target_matcher.add([
    TargetRule("seminoma", "HISTOLOGY"),
    TargetRule("NSGCT", "HISTOLOGY"),
    TargetRule("orchiectomy", "SURGERY"),
    TargetRule("testicular", "PRIMARY_SITE"),
    TargetRule("testicular", "PRIMARY_SITE"),
])

for rule in target_matcher.rules:
    print(rule.literal, rule.category)

print(target_matcher.rules)


    # print(f"Text: {section.text}\n")
