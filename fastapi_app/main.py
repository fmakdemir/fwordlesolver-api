from fastapi import FastAPI, HTTPException
from fwordlesolver.solver import WordleSolver
from .schemas import (
    HealthResponse,
    PingResponse,
    WordleSolveRequest,
    WordleSolveResponse,
)

app = FastAPI(
    title="Wordle API",
    description="This is an API for Wordle",
    version="1.0.0",
)


@app.post(
    "/wordle-solver/api/wordle",
    operation_id="solve_wordle",
    response_model=WordleSolveResponse,
)
async def solve_wordle(req: WordleSolveRequest):
    if len(req.places) != len(req.words):
        raise HTTPException(
            status_code=400, detail="Number of words and places must match"
        )
    if any(len(w) != len(p) for w, p in zip(req.words, req.places)):
        raise HTTPException(
            status_code=400, detail="Words and places must have the same length"
        )
    solver = WordleSolver(req.size)
    for _w, _p in zip(req.words, req.places):
        solver.apply_guess(_w, _p)
    return WordleSolveResponse(
        suggestions=solver.get_suggestions(),
        alternatives=solver.get_not_used_suggestion(),
        remaining=len(solver.words),
        used_letters=list(solver.used_letters),
    )


@app.get("/wordle-solver/api/ping", operation_id="ping", response_model=PingResponse)
async def ping():
    return PingResponse(response="pong")


@app.get(
    "/wordle-solver/api/health", operation_id="health", response_model=HealthResponse
)
async def health():
    return HealthResponse(status="ok", response="ok")
