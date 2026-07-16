from datetime import datetime
from pydantic import BaseModel, Field


class ParsedNote(BaseModel):
    mrn: str

    note_name: str | None = None
    note_date: datetime | None = None
    note_text: str

    primary_site: str | None = None
    # histology: list[str] = Field(default_factory=list)

    source: str | None = None