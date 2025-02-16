from ninja import NinjaAPI, Schema
from fwordlesolver.solver import WordleSolver


class FWordleAPI(NinjaAPI):
    def get_openapi_operation_id(self, operation):
        name = operation.view_func.__name__
        return name.replace(".", "_")


api = FWordleAPI(title="Wordle API", description="This is an API for Wordle")


class WordleSolveRequest(Schema):
    words: list[str]
    places: list[str]
    size: int


class WordleSolveResponse(Schema):
    suggestions: list[str]
    alternatives: list[str]
    remaining: int
    used_letters: list[str]


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
        suggestions=solver.get_suggestions(),
        alternatives=solver.get_not_used_suggestion(),
        remaining=len(solver.words),
        used_letters=list(solver.used_letters),
    )


@api.get("/ping")
def ping(request):
    return {"response": "pong"}
