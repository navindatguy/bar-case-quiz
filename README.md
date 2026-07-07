# Bar Case Quiz

Turns real court opinions into bar-exam-style practice questions, with each
question linked back to the source case for a grounded explanation.

## How it works

1. **inupt** — pull case text from the [Caselaw Access Project](https://case.law/)
   bulk data (JSON) into a local database.
2. **Generate** — for a given case + legal topic (e.g. "Fourth Amendment",
   "Motions to Suppress"), an LLM reads the opinion and produces a
   multiple-choice bar-style question, an answer, and a short rationale.
3. **Serve** — a FastAPI backend exposes cases and generated questions. then, a
   React frontend lets a user pick a topic and quiz themselves, with a
   "why?" link that shows the relevant excerpt from the source opinion.

## Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Postgres
- **LLM:** Anthropic API (Claude) for question generation
- **Frontend:** React (Vite)
- **Data:** Caselaw Access Project (CAP) bulk JSON exports

## Project layout

```
bar-case-quiz/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app entrypoint
│   │   ├── config.py          # settings / env vars
│   │   ├── database.py        # DB session/engine setup
│   │   ├── models.py          # SQLAlchemy models (Case, Question)
│   │   ├── schemas.py         # Pydantic request/response models
│   │   ├── routers/
│   │   │   ├── cases.py       # /cases endpoints
│   │   │   └── questions.py   # /questions endpoints
│   │   └── services/
│   │       ├── cap_ingest.py         # loads CAP JSON into DB
│   │       └── question_generator.py # calls Claude to generate questions
│   └── tests/
├── scripts/
│   └── ingest_cap_data.py     # CLI wrapper to run ingestion
├── frontend/                  # React app (quiz UI)
├── data/                      # local CAP downloads (gitignored)
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Setup

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
cp ../.env.example ../.env   # fill in ANTHROPIC_API_KEY and DATABASE_URL
```

### 2. Database

```bash
docker-compose up -d db
```

### 3. Ingest some cases

Download a bulk export or use CAP's API for a jurisdiction/reporter of
interest, then:

```bash
python scripts/ingest_cap_data.py --file data/illinois_cases.json --limit 500
```

### 4. Generate questions

```bash
python -m backend.app.services.question_generator --topic "Motions to Suppress" --count 10
```

### 5. Run the API

```bash
uvicorn backend.app.main:app --reload
```

### 6. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

## Legal / content notes

- Case opinion text from CAP is public domain — safe to store, redistribute,
  and build on.
- llm should exist to create said questions, and not inject anything, so product quality
  is important to look at.
- Every generated question stores a citation and excerpt pointer back to the
  source case, so answers are auditable rather than opaque.
- This is a study aid, not legal advice, and isnt a substitute for
  official bar prep materials. disclaimer in the UI?

## Roadmap

- [ ] CAP ingestion pipeline
- [ ] Question generation + review queue (LLM output should be spot-checked
      before going live, especially for accuracy of the "correct" answer)
- [ ] Topic tagging (map cases to bar exam subjects)
- [ ] Frontend quiz flow
- [ ] Spaced-repetition / missed-question review mode
- [ ] Deploy (Fly.io / Render / Railway for a free-tier-friendly start)

## License

MIT (see `LICENSE`). Case text itself is public domain.
