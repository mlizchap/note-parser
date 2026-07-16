"""
MongoDB repository functions for parsed notes.

This module is responsible only for database reads and writes.
It should not parse notes or convert DataFrames.
"""

from typing import Any

from pymongo import UpdateOne
from pymongo.collection import Collection
from pymongo.results import BulkWriteResult, DeleteResult, UpdateResult

from core.database import database


notes_collection: Collection = database["notes"]


def save_parsed_notes(
    documents: list[dict[str, Any]],
) -> BulkWriteResult | None:
    """
    Insert or update parsed note documents.

    Uses source_note_id when available. Otherwise falls back to a composite
    key based on MRN, note name, and note date.
    """

    if not documents:
        return None

    operations: list[UpdateOne] = []

    for document in documents:
        source_note_id = document.get("source_note_id")

        if source_note_id:
            note_key = {
                "source": document.get("source"),
                "source_note_id": source_note_id,
            }
        else:
            note_key = {
                "mrn": document["mrn"],
                "note_name": document.get("note_name"),
                "note_date": document.get("note_date"),
            }

        operations.append(
            UpdateOne(
                note_key,
                {
                    "$set": document,
                    "$setOnInsert": {
                        "created_at": document.get("updated_at"),
                    },
                },
                upsert=True,
            )
        )

    return notes_collection.bulk_write(
        operations,
        ordered=False,
    )


def get_notes_by_mrn(
    mrn: str,
    limit: int = 1000,
) -> list[dict[str, Any]]:
    """Return notes for one MRN, ordered by note date."""

    cursor = (
        notes_collection
        .find({"mrn": str(mrn)})
        .sort("note_date", 1)
        .limit(limit)
    )

    return list(cursor)


def get_note_by_id(note_id: Any) -> dict[str, Any] | None:
    """Return one note using its MongoDB _id value."""

    return notes_collection.find_one({"_id": note_id})


def get_notes_by_primary_site(
    primary_site: str,
    limit: int = 1000,
) -> list[dict[str, Any]]:
    """Return notes containing a canonical primary-site value."""

    cursor = (
        notes_collection
        .find({"primary_site": primary_site.lower()})
        .limit(limit)
    )

    return list(cursor)


def update_note_fields(
    note_id: Any,
    fields: dict[str, Any],
) -> UpdateResult:
    """Update selected fields for one note."""

    return notes_collection.update_one(
        {"_id": note_id},
        {"$set": fields},
    )


def delete_note(note_id: Any) -> DeleteResult:
    """Delete one note."""

    return notes_collection.delete_one({"_id": note_id})