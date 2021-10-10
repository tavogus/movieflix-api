from typing import List, Optional
import pydantic as _pydantic
import datetime as _dt

#USER SCHEMAS
class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True

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
    categories: str
    release_date: int
    director: str
    synopsis: str

class MovieCreate(_MovieBase):
    pass

class Movie(_MovieBase):
    id: int
    insertion_date: _dt.datetime
    actors: List[Actor] = []

    class Config:
        orm_mode = True