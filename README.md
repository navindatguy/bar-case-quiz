# Bar Case Quiz

Turns real court opinions into bar-exam-style practice questions, with each
question linked back to the source case for a grounded explanation.

## How it works

1.  pull case text from the [Caselaw Access Project](https://case.law/)
   bulk (JSON) into a local database.
2. for a given case + legal topic (e.g. "Fourth Amendment",
   "Motions to Suppress"), an LLM reads the opinion and produces a
   multiple-choice bar-style question, an answer, and a short rationale.
3.  a FastAPI backend exposes cases and generated questions. then, a
   React frontend lets a user pick a topic and quiz themselves, with a
   "why?" link that shows the relevant excerpt from the source opinion.

## Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Postgres
- **LLM:** localhosted ollama right now...
- **Frontend:** React (Vite)
- **Data:** Caselaw Access Project (CAP) bulk JSON exports


## Legal / content notes

- Case opinion text from CAP is public domain — safe to store, redistribute,
  and build on.
- llm should exist to create said questions, and not inject anything, so product quality
  is important to look at.
- Every generated question stores a citation and excerpt pointer back to the
  source case, so answers are auditable rather than opaque.
- This is a study aid, not legal advice, and isnt a substitute for
  official bar prep materials. disclaimer in the UI?



## License

MIT (see `LICENSE`). Case text itself is public domain.
