from typing import List
import pydantic as _pydantic
import datetime as _dt

#ACTOR SCHEMAS
class _ActorBase(_pydantic.BaseModel):
    name: str

class ActorCreate(_ActorBase):
    pass

class Actor(_ActorBase):
    id: int

    class Config:
        orm_mode = True

#MOVIE SCHEMAS
class _MovieBase(_pydantic.BaseModel):
    title: str
    categories: List[str] = []
    release_date: int
    director: str
    synopsis: str
    actors: List[str] = []

class MovieCreate(_MovieBase):
    pass

class Movie(_MovieBase):
    id: int
    insertion_date: _dt.datetime

    class Config:
        orm_mode = True