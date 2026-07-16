# Overview
- This application takes in a csv of raw data and creates data with discreet fields as well as an application for viewing the data and comparing to other sources
- [PIC/chart]: csv from databricks -> parsed fields -> compare to other data sources -> display findings

# Sections
## Field Extraction per note
- uses a csv file of raw notes to process and output a df of parsed note data
- to run: `$python main.py mrn=123`
- args:
    - mrn (opt)
        - if provided, only processes that MRN
        - otherwise processes all MRNs in DF
- output: mrn | primary_site | ...other fields | note (one row per note)

## Source Compare
- given a field name, compares values accross data sources
- to run: `$python main.py field=dx_date`
- args:
    - field_name: field used to compare accross sources
- output: mrn | field_name | ...sources | notes | status | final

## API
- using the output from the field extraction, creates and saves a mongo db Note obj
    - schema: `{ mrn: { site: { notes: [ ...fields, ...note_info ] } } }`
    - models:
        - Note:
            - mrn
            - site
            - note_date
            - note_text
            - note_name
- create queries and mutations 
    - queries
        - all notes: per note
        - consolidated notes: per primary site per mrn
        - patient field data: patient data for all srouces
    <!-- - mutations -->

## APP
- uses the parsed notes object to view and analyze
- to run:
    - with dummy data:
    - with gql data:
- routes:
    - home
        - nav
            - Detailed notes
            - Notes consolidated by site
            - Source compare
            - Note search
            - Patient search
    - /notes/compare
        - displays a table of all sources: mrn | caisis | msk | notes | status | final
    - /notes/details/all
        - displays parsed notes in sheet, each row is one note
        - when clicked goes to patient/timeline/:mrn
    - /notes/consolidated
        - displays final outcomes of parsed notes, one row per mrn per primary site
    - /patient/timeline/:mrn
        - shows note details per MRN in timeline format
    - /patient/table/:mrn
        - - shows note details per MRN in table format

# Other
- start mongo: `brew services start mongodb-community`
- verify mongo is running: `brew services list`
- test connection: `mongosh`
    - show dbs
    - use [table]
    - show collections
    - view all docs in collection: db.notes.find().pretty()
    - view one: db.notes.findOne()
    - count docs: db.notes.countDocuments()
    - clear docs: db.notes.deleteMany({})
- run notes: in project dir - `python -m notes.main`



notes
One document per note:
{
  "_id": "note-id",
  "mrn": "12345",
  "primary_sites": ["testis"],
  "note_date": "2026-07-16",
  "note_name": "Follow-up",
  "note_text": "...",
  "extractions": {
    "primary_site": {
      "value": "testis",
      "evidence": "testicular cancer",
      "rule_id": "testicular_rule"
    }
  }
}
patients
{
  "_id": "12345",
  "mrn": "12345",
  "primary_sites": ["testis"]
}
field_comparisons
{
  "mrn": "12345",
  "field_name": "dx_date",
  "values": {
    "caisis": "2025-01-01",
    "msk": "2025-01-02",
    "notes": "2025-01-01"
  },
  "status": "variance",
  "final_value": "2025-01-01"
}

MongoDB
GraphQL for app queries
REST for uploads/jobs/exports
Frontend: React + Vite

REST
```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/patients/{mrn}")
def get_patient(mrn: str):
    return {"mrn": mrn}


@app.post("/parse")
def parse_notes():
    # call your parser
    return {"status": "complete"}
```


project/
├── notes/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── constants/
│   │   ├── __init__.py
│   │   ├── context_rules.py
│   │   ├── target_rules.py
│   │   └── section_rules.py
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── build_pipeline.py
│   │
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── csv_loader.py
│   │   └── palantir_loader.py
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── note_parser.py
│   │   └── oncology_history.py
│   │
│   ├── field_parsers/
│   │   ├── __init__.py
│   │   ├── primary_site.py
│   │   ├── histology.py
│   │   ├── diagnosis_date.py
│   │   └── stage.py
│   │
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── context.py
│   │   ├── normalization.py
│   │   └── segmentation.py
│   │
│   └── tests/
│       ├── test_primary_site.py
│       ├── test_note_parser.py
│       └── test_context.py
│
├── patientdata/
│   ├── __init__.py
│   ├── main.py
│   ├── compare_sources.py
│   ├── consolidate.py
│   ├── adjudication.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── caisis.py
│   │   ├── msk.py
│   │   └── registry.py
│   └── tests/
│       ├── test_compare_sources.py
│       └── test_consolidate.py
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── notes/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── service.py
│   └── patientdata/
│       ├── routes.py
│       ├── schemas.py
│       └── service.py
│
└── app/
