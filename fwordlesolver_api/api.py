from ninja import NinjaAPI
from fwordlesolver.solver import WordleSolver

api = NinjaAPI()


@api.post("/wordle")
def solve_world(request, words: list[str], places: list[str]):
    if not len(words):
        return {"error": "Must provide at least one word"}
    if len(places) != len(words):
        return {"error": "Number of words and places must match"}
    if any(len(w) != len(p) for w, p in zip(words, places)):
        return {"error": "Words and places must have the same length"}
    word_size = len(words[0])
    solver = WordleSolver(word_size)
    for _w, _p in zip(words, places):
        solver.apply_guess(_w, _p)
    return {
        "sug": solver.get_suggestions(),
        "alt": solver.get_not_used_suggestion(),
        "remaining": len(solver.words),
        "used_letters": solver.used_letters,
    }
