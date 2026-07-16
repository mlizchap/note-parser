import medspacy
# from medspacy.section_detection import SectionRule
# from medspacy.ner import TargetRule
from constants.targets import PRIMARY_SITE_RULES
from constants.context import METASTATIC_CONTEXT_RULES

nlp = medspacy.load()

# Add the sectionizer because it is not currently in the pipeline
sectionizer = nlp.add_pipe(
    "medspacy_sectionizer",
    config={"rules": None},
)

sectionizer.add(
    [
        SectionRule("test:", "HPI"),
        SectionRule("Past Medical History:", "PMH"),
        SectionRule("Family and Social History:", "FSH"),
        SectionRule("Medications:", "MEDICATIONS"),
        SectionRule("Allergies:", "ALLERGIES"),
        SectionRule("Vital Signs:", "VITAL_SIGNS"),
        SectionRule("Chief complAint:", "CHIEF_COMPLAINT"),
        SectionRule("assessment:", "ASSESSMENT"),
        SectionRule("diagnosis:", "DX"),
    ]
)

print(nlp.pipe_names)

# Sample text with various sections
text = """
Chief complaint: patient has nothing.
Other section: Patient presents with severe chest pain. Past medical history includes hypertension and diabetes.
Family history is significant for heart disease.
Current medications include aspirin and metformin.
assessment: patient has lung cancer,
Allergies are noted to penicillin and sulfonamides.
Medications: A, B. for diagnosis of abc,
Vital signs: BP 140/90, HR 88, Temp 37.5°C.
diagnosis: patient has lung cancer 2,
"""

# text = text.lower()

# Process the text
doc = nlp(text)

# Print sections
for section in doc._.sections:
    title_start, title_end = section.title_span
    body_start, body_end = section.body_span

    title = doc[title_start:title_end]
    body = doc[body_start:body_end]

    print("Header:", title.text)
    print("Body:", body.text)


target_matcher = nlp.get_pipe("medspacy_target_matcher")
target_matcher.add([
    TargetRule("seminoma", "HISTOLOGY"),
    TargetRule("NSGCT", "HISTOLOGY"),
    TargetRule("orchiectomy", "SURGERY"),
])


print(target_matcher.rules)


    # print(f"Text: {section.text}\n")
