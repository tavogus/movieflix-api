from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas
from src.models import Movie

app = _fastapi.FastAPI()

_services.create_database()

@app.post("/movies/", response_model=_schemas.Movie)
def create_movie(movie: _schemas.MovieCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_movie = _services.get_movie_by_title(db=db, title=movie.title)
    
    if db_movie:
        raise _fastapi.HTTPException(status_code=400, detail="Already exists a movie with this title")

    return _services.create_movie(db=db, movie=movie)

@app.get("/movies/", response_model=List[_schemas.Movie])
def get_movies(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db),):
    movies = _services.get_movies(db=db, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=_schemas.Movie)
def get_movies(movie_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_movie = _services.get_movie(db=db, movie_id=movie_id)

    if db_movie is None:
        raise _fastapi.HTTPException(status_code=404, detail="No movie found with given id")
    
    return db_movie

@app.post("/actors/", response_model=_schemas.Actor)
def create_actor(actor: _schemas.ActorCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_actor = _services.get_actor_by_name(db=db, name=actor.name)
    
    if db_actor:
        raise _fastapi.HTTPException(status_code=400, detail="Already exists a actor with this name")

    return _services.create_actor(db=db, actor=actor)

