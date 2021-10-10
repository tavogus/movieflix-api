from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import fastapi.security as _security
import services as _services, schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()

#USER

@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

#MOVIE

@app.post("/movies/", response_model=_schemas.Movie)
async def create_movie(movie: _schemas.MovieCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_movie = await _services.get_movie_by_title(db=db, title=movie.title)
    
    if db_movie:
        raise _fastapi.HTTPException(status_code=400, detail="Already exists a movie with this title")

    return await _services.create_movie(db=db, movie=movie)


@app.post("/movies/{id_movie}/actor/{actor_id}", response_model=_schemas.Movie)
async def add_actor_to_movie(movie_id: int, actor_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.add_actor_to_movie(db=db, movie_id=movie_id, actor_id=actor_id)


@app.get("/movies/", response_model=List[_schemas.Movie])
async def get_movies(db: _orm.Session = _fastapi.Depends(_services.get_db),):
    return await _services.get_movies(db=db)


@app.get("/movies/{movie_id}", response_model=_schemas.Movie)
async def get_movie(movie_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_movie = await _services.get_movie(db=db, movie_id=movie_id)

    if db_movie is None:
        raise _fastapi.HTTPException(status_code=404, detail="No movie found with given id")
    
    return db_movie

#ACTOR

@app.post("/actors/", response_model=_schemas.Actor)
async def create_actor(actor: _schemas.ActorCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_actor = await _services.get_actor_by_name(db=db, name=actor.name)
    
    if db_actor:
        raise _fastapi.HTTPException(status_code=400, detail="Already exists a actor with this name")

    return await _services.create_actor(db=db, actor=actor)

