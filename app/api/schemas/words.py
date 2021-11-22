from typing import Optional
from pydantic import BaseModel


class BaseWords(BaseModel):
    id: Optional[int] = None
    words: Optional[str] = None
    words_title: Optional[str] = None


class WordsCreate(BaseWords):
    words: str
    words_title: str


class WordsEdit(BaseWords):
    words: Optional[str] = None
    words_title: Optional[str] = None
