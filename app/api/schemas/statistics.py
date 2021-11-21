from typing import Optional
from pydantic import BaseModel


class BaseRace(BaseModel):
    id: Optional[int] = None
    best_wpm: Optional[int] = None
    best_accuracy: Optional[int] = None
    total_races: Optional[int] = None
    total_wins: Optional[int] = None
    average_wpm: Optional[float] = None
    average_epm: Optional[float] = None
    average_accuracy: Optional[float] = None
    average_time: Optional[float] = None


class StatisticsCreate(BaseRace):
    best_wpm: Optional[int]
    best_accuracy: Optional[int]
    total_races: Optional[int]
    total_wins: Optional[int]
    average_wpm: Optional[float]
    average_epm: Optional[float]
    average_accuracy: Optional[float]
    average_time: Optional[float]


class StatisticsGet(BaseRace):
    id: int


class StatisticsEdit(BaseRace):
    best_wpm: Optional[int]
    best_accuracy: Optional[int]
    total_races: Optional[int]
    total_wins: Optional[int]
    average_wpm: Optional[float]
    average_epm: Optional[float]
    average_accuracy: Optional[float]
    average_time: Optional[float]


class StatisticsDelete(BaseRace):
    id: int




