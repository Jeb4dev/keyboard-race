from typing import Optional
from pydantic import BaseModel


class BaseStatistics(BaseModel):
    id: Optional[int] = None
    best_wpm: Optional[int] = None
    best_accuracy: Optional[int] = None
    total_races: Optional[int] = None
    total_wins: Optional[int] = None
    average_wpm: Optional[float] = None
    average_epm: Optional[float] = None
    average_accuracy: Optional[float] = None
    average_time: Optional[float] = None
