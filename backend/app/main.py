from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import cases, questions

app = FastAPI(
    title="Bar Case Quiz API",
    description="Turns real court opinions into bar-exam-style practice questions.",
    version="0.1.0",
)

# Allow the local frontend dev server to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases.router)
app.include_router(questions.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
