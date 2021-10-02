import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()

@app.post("/movies/", response_model=_schemas.Movie)
def create_movie(movie: _schemas.MovieCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_movie = _services.get_movie_by_title(db=db, title=movie.title)
    
    if db_movie:
        raise _fastapi.HTTPException(status_code=400, detail="Already exists a movie with this title")

    return _services.create_movie(db=db, movie=movie)

