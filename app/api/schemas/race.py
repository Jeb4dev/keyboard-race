from typing import Optional
from pydantic import BaseModel


class BaseRace(BaseModel):
    id: Optional[int] = None
    date: Optional[str] = None
    ranking: Optional[int] = None
    total_participants: Optional[int] = None
    wpm: Optional[int] = None
    epm: Optional[int] = None
    accuracy: Optional[int] = None
    time: Optional[int] = None
    errors: Optional[int] = None


class RaceCreate(BaseRace):
    ranking: int
    total_participants: int
    wpm: int
    epm: int
    accuracy: int
    time: int


class RaceEdit(BaseRace):
    id: int
    ranking: Optional[int]
    total_participants: Optional[int]
    wpm: Optional[int]
    epm: Optional[int]
    accuracy: Optional[int]
    time: Optional[int]
