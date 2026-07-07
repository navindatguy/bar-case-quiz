"""CLI entrypoint for loading a CAP bulk JSON file into the database.

Usage:
    python scripts/ingest_cap_data.py --file data/illinois_cases.json --limit 500
"""

import argparse

from backend.app.database import SessionLocal, engine, Base
from backend.app.services.cap_ingest import ingest_file


def main():
    parser = argparse.ArgumentParser(description="Ingest CAP bulk case data into the database.")
    parser.add_argument("--file", type=str, required=True, help="Path to a CAP JSON/JSONL export.")
    parser.add_argument("--limit", type=int, default=None, help="Max number of records to ingest.")
    args = parser.parse_args()

    # Ensure tables exist. For real migrations use alembic instead.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        inserted = ingest_file(args.file, db, limit=args.limit)
        print(f"Inserted {inserted} new cases from {args.file}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
