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
    category: str
    release_date: str
    director: str
    synopsis: str
    actors: List[Actor] = []

class MovieCreate(_MovieBase):
    pass

class Movie(_MovieBase):
    id: int
    insertion_date: _dt.datetime

    class Config:
        orm_mode = True