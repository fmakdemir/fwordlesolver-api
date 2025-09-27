from pydantic import BaseModel


class WordleSolveRequest(BaseModel):
    words: list[str]
    places: list[str]
    size: int


class WordleSolveResponse(BaseModel):
    suggestions: list[str]
    alternatives: list[str]
    remaining: int
    used_letters: list[str]
