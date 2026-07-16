"""
medspacy_context_demo.py

Demonstrates how to:
1. Load a MedSpaCy pipeline.
2. Add TargetRules for cancer-related entities.
3. Add a custom ConText rule for metastatic sites.
4. Process example clinical sentences.
5. Print whether each entity is negated, historical, uncertain,
   hypothetical, associated with family history, or metastatic.

Install:
    python -m pip install medspacy

Run:
    python medspacy_context_demo.py
"""

from __future__ import annotations

from typing import Any

import medspacy
from medspacy.context import ConTextRule
from medspacy.ner import TargetRule


def build_pipeline() -> Any:
    """Create and configure a MedSpaCy pipeline."""
    nlp = medspacy.load()

    target_matcher = nlp.get_pipe("medspacy_target_matcher")
    target_matcher.add(
        [
            # TargetRule("testicular cancer", "CANCER"),
            TargetRule("lung cancer", "CANCER"),
            TargetRule("seminoma", "HISTOLOGY"),
            TargetRule("NSGCT", "HISTOLOGY"),
            TargetRule("testis", "PRIMARY_SITE"),
            TargetRule("testicular", "PRIMARY_SITE"),
            TargetRule("lung", "PRIMARY_SITE"),
            TargetRule("liver", "PRIMARY_SITE"),
            TargetRule("hip", "PRIMARY_SITE"),
            TargetRule("mediastinum", "PRIMARY_SITE"),
        ]
    )

    context = nlp.get_pipe("medspacy_context")

    # Custom rules that mark a following entity as metastatic.
    # We detect this status by inspecting the entity's attached modifiers.
    context.add(
        [
            ConTextRule("metastatic to", "METASTATIC", direction="FORWARD"),
            ConTextRule("metastasis to", "METASTATIC", direction="FORWARD"),
            ConTextRule("metastases to", "METASTATIC", direction="FORWARD"),
            ConTextRule("mets to", "METASTATIC", direction="FORWARD"),
            ConTextRule("metastasis in", "METASTATIC", direction="FORWARD"),
            ConTextRule("metastases in", "METASTATIC", direction="FORWARD"),
        ]
    )

    return nlp


def modifier_category(modifier: Any) -> str:
    """Safely read a modifier's category across MedSpaCy versions."""
    category = getattr(modifier, "category", "")
    if category:
        return str(category).upper()

    rule = getattr(modifier, "rule", None)
    return str(getattr(rule, "category", "")).upper()


def has_modifier(entity: Any, category: str) -> bool:
    """Return True when an entity has a ConText modifier of a category."""
    expected = category.upper()
    modifiers = getattr(entity._, "modifiers", [])
    return any(modifier_category(modifier) == expected for modifier in modifiers)


def get_context_labels(entity: Any) -> dict[str, bool]:
    """Return built-in and custom ConText labels for an entity."""
    return {
        "negated": bool(getattr(entity._, "is_negated", False)),
        "historical": bool(getattr(entity._, "is_historical", False)),
        "uncertain": bool(getattr(entity._, "is_uncertain", False)),
        "hypothetical": bool(getattr(entity._, "is_hypothetical", False)),
        "family": bool(getattr(entity._, "is_family", False)),
        "metastatic": has_modifier(entity, "METASTATIC"),
    }


def print_entities(nlp: Any, text: str) -> None:
    """Process text and print every entity with its ConText labels."""
    doc = nlp(text)

    print("=" * 90)
    print(text.strip())
    print("-" * 90)

    if not doc.ents:
        print("No entities detected.")
        return

    for entity in doc.ents:
        labels = get_context_labels(entity)
        active_labels = [name for name, active in labels.items() if active]

        print(f"Entity: {entity.text!r}")
        print(f"Category: {entity.label_}")
        print(f"Context: {', '.join(active_labels) if active_labels else 'affirmed/current'}")

        modifiers = getattr(entity._, "modifiers", [])
        if modifiers:
            print(
                "Modifiers:",
                ", ".join(
                    modifier_category(modifier) or str(modifier)
                    for modifier in modifiers
                ),
            )
        print()


def main() -> None:
    nlp = build_pipeline()

    examples = [
        # "No evidence of seminoma.",
        # "possible seminoma.",
        # "History of NSGCT.",
        # "Possible lung cancer.",
        # "His father had testicular cancer.",
        # "If seminoma develops, obtain imaging.",
        # "tested negative for lung cancer"
        # "Testicular cancer metastatic to lung and liver.",
        # "NSGCT of the right testis with metastases to the right hip.",
        # "Primary mediastinal NSGCT without lung metastases.",
        "pain in testis",
        "no evidence of lung cancer on CT scan. later showed results for a testicular cancer from surgery"
    ]

    print("Pipeline:", nlp.pipe_names)

    for example in examples:
        print_entities(nlp, example)


if __name__ == "__main__":
    main()