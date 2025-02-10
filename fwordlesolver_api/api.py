from ninja import NinjaAPI, Schema
from fwordlesolver.solver import WordleSolver

api = NinjaAPI(title="Wordle API", description="This is an API for Wordle")


class WordleSolveRequest(Schema):
    words: list[str]
    places: list[str]
    size: int


class WordleSolveResponse(Schema):
    suggestions: list[str]
    alternatives: list[str]
    remaining: int
    used_letters: set[str]


@api.post("/wordle", response=WordleSolveResponse)
def solve_wordle(request, req: WordleSolveRequest) -> WordleSolveResponse:
    if len(req.places) != len(req.words):
        return {"error": "Number of words and places must match"}
    if any(len(w) != len(p) for w, p in zip(req.words, req.places)):
        return {"error": "Words and places must have the same length"}
    solver = WordleSolver(req.size)
    for _w, _p in zip(req.words, req.places):
        solver.apply_guess(_w, _p)
    return WordleSolveResponse(
        solver.get_suggestions(),
        solver.get_not_used_suggestion(),
        len(solver.words),
        solver.used_letters,
    )
