"""
Loads case records from Caselaw Access Project (CAP) bulk JSON exports into
the local database.

CAP bulk files are JSON Lines or JSON arrays depending on export format —
check https://case.law/download/ for the current structure. This module
assumes each record roughly matches CAP's case schema:

    {
      "id": "...",
      "name": "...",
      "citations": [{"cite": "..."}],
      "court": {"name": "..."},
      "jurisdiction": {"name": "..."},
      "decision_date": "YYYY-MM-DD",
      "casebody": {"data": {"opinions": [{"text": "..."}]}},
      "frontend_url": "..."
    }

Adjust the field mapping below if you're pulling from a different CAP export
version or from CourtListener instead.
"""

import json
from pathlib import Path

from sqlalchemy.orm import Session

from backend.app import models


def _extract_full_text(record: dict) -> str:
    """Concatenate all opinion text blocks for a case record."""
    opinions = record.get("casebody", {}).get("data", {}).get("opinions", [])
    return "\n\n".join(op.get("text", "") for op in opinions).strip()


def _record_to_case(record: dict) -> models.Case:
    citations = record.get("citations", [])
    citation = citations[0]["cite"] if citations else ""

    return models.Case(
        cap_id=str(record.get("id")),
        case_name=record.get("name", "")[:500],
        citation=citation,
        court=record.get("court", {}).get("name", ""),
        jurisdiction=record.get("jurisdiction", {}).get("name", ""),
        decision_date=record.get("decision_date", ""),
        full_text=_extract_full_text(record),
        source_url=record.get("frontend_url"),
    )


def ingest_file(file_path: str, db: Session, limit: int | None = None) -> int:
    """Ingest CAP records from a JSON file into the database.

    Supports both a top-level JSON array and JSON Lines (one record per line).
    Returns the number of cases inserted. Skips records already present
    (matched on cap_id) and records with no opinion text.
    """
    path = Path(file_path)
    raw = path.read_text(encoding="utf-8")

    if raw.lstrip().startswith("["):
        records = json.loads(raw)
    else:
        records = [json.loads(line) for line in raw.splitlines() if line.strip()]

    if limit:
        records = records[:limit]

    inserted = 0
    for record in records:
        cap_id = str(record.get("id"))
        exists = db.query(models.Case).filter(models.Case.cap_id == cap_id).first()
        if exists:
            continue

        case = _record_to_case(record)
        if not case.full_text:
            continue  # skip cases with no digitized opinion text

        db.add(case)
        inserted += 1

    db.commit()
    return inserted
