from fastapi import FastAPI, HTTPException
from fwordlesolver.solver import WordleSolver
from .schemas import WordleSolveRequest, WordleSolveResponse

app = FastAPI(
    title="Wordle API",
    description="This is an API for Wordle",
    version="1.0.0",
)


@app.post("/wordle-solver/api/wordle", response_model=WordleSolveResponse)
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


@app.get("/wordle-solver/api/ping")
async def ping():
    return {"response": "pong"}
