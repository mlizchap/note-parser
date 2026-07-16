install packages: python -m pip install pymongo fastapi uvicorn pydantic-settings

db config:
project/
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── database.py

create env
MONGODB_URI=mongodb://127.0.0.1:27017
MONGODB_DATABASE=clinical_note_parser

.gitignore
.env

core/config
```
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://127.0.0.1:27017"
    mongodb_database: str = "clinical_note_parser"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
```

core/database.py
```
from pymongo import MongoClient
from pymongo.database import Database

from project.core.config import settings


client = MongoClient(
    settings.mongodb_uri,
    serverSelectionTimeoutMS=5000,
)

database: Database = client[settings.mongodb_database]


def verify_database_connection() -> None:
    """Raise an exception if MongoDB cannot be reached."""
    client.admin.command("ping")
```

test connection
```
from project.core.database import verify_database_connection

verify_database_connection()
print("MongoDB connected")
```

create models:
project/
├── api/
│   ├── main.py
│   ├── models/
│   │   ├── job.py        ← Job model goes here
│   │   ├── note.py
│   │   └── patient.py
│   ├── notes/
│   └── patientdata/
│
├── notes/
├── patientdata/
└── app/

job:
{ "job_type": "note_extraction", "status": "running", "created_at": "...", "completed_at": null, "input_file": "notes.csv", "processed_count": 200, "error_count": 3 }

note

patient



in notes:
models.py
Defines the validated note shape, such as ParsedNote.
```
from datetime import datetime
from pydantic import BaseModel, Field


class ParsedNote(BaseModel):
    mrn: str

    note_name: str | None = None
    note_date: datetime | None = None
    note_text: str

    primary_site: list[str] = Field(default_factory=list)
    histology: list[str] = Field(default_factory=list)

    source: str | None = None
```

serializers.py
Converts your parsed DataFrame rows into MongoDB-ready dictionaries.
```python
"""
Converts between DataFrames, ParsedNote models, and MongoDB documents.
"""

from typing import Any

import pandas as pd

from notes.models import ParsedNote


def parse_pipe_delimited(value: Any) -> list[str]:
    """
    Converts:
        "testis | mediastinum" -> ["testis", "mediastinum"]
        "UNKNOWN" -> []
        None -> []
    """
    if value is None or pd.isna(value):
        return []

    value = str(value).strip()

    if value == "" or value.upper() == "UNKNOWN":
        return []

    return [
        item.strip()
        for item in value.split("|")
        if item.strip()
    ]


def dataframe_row_to_model(row: dict[str, Any]) -> ParsedNote:
    """
    Convert one parsed DataFrame row into a ParsedNote model.
    """

    return ParsedNote(
        mrn=str(row["mrn"]),
        note_name=row.get("note_name"),
        note_date=row.get("note_date"),
        note_text=row.get("note_text", ""),

        primary_site=parse_pipe_delimited(
            row.get("primary_site")
        ),

        histology=parse_pipe_delimited(
            row.get("histology")
        ),

        source=row.get("source"),
    )


def dataframe_to_models(
    df: pd.DataFrame,
) -> list[ParsedNote]:
    """
    Convert a parsed DataFrame into ParsedNote models.
    """

    return [
        dataframe_row_to_model(row)
        for row in df.to_dict("records")
    ]


def model_to_document(
    note: ParsedNote,
) -> dict[str, Any]:
    """
    Convert ParsedNote into a MongoDB document.
    """

    return note.model_dump(
        mode="python",
        exclude_none=True,
    )


def models_to_documents(
    notes: list[ParsedNote],
) -> list[dict[str, Any]]:
    """
    Convert ParsedNote models into MongoDB documents.
    """

    return [
        model_to_document(note)
        for note in notes
    ]
```

repository.py
Contains direct MongoDB operations:
```python
"""
MongoDB repository functions for parsed notes.

This module is responsible only for database reads and writes.
It should not parse notes or convert DataFrames.
"""

from typing import Any

from pymongo import UpdateOne
from pymongo.collection import Collection
from pymongo.results import BulkWriteResult, DeleteResult, UpdateResult

from project.core.database import database


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
```

service.py
Coordinates the workflow:
```python
from notes.parsers.parse_notes import parse_notes
from notes.repository import save_parsed_notes
from notes.serializers import dataframe_to_note_documents


def parse_and_save_notes(df, nlp):
    parsed_df = parse_notes(df, nlp)
    documents = dataframe_to_note_documents(parsed_df)
    return save_parsed_notes(documents)
```