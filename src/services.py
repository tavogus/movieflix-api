import sqlalchemy.orm as _orm
import fastapi.security as _security
import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import passlib.hash as _hash
import database as _database, models as _models, schemas as _schemas

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


#USER 

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)        



#MOVIE

async def get_movie_by_title(db: _orm.Session, title: str):
    return db.query(_models.Movie).filter(_models.Movie.title == title).first()

async def create_movie(db: _orm.Session, movie: _schemas.MovieCreate):
    db_movie = _models.Movie(**movie.dict())

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return _schemas.Movie.from_orm(db_movie)

async def add_actor_to_movie(db: _orm.Session, movie_id: int, actor_id: int):
    db_movie = db.query(_models.Movie).filter(_models.Movie.id == movie_id).first()
    actors = db.query(_models.Actor).filter(_models.Actor.id == actor_id).first()

    db_movie.actors.append(actors)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return _schemas.Movie.from_orm(db_movie)

async def get_movies(db: _orm.Session):
    movies =  db.query(_models.Movie).all()

    return list(map(_schemas.Movie.from_orm, movies))

async def get_movie(db: _orm.Session, movie_id: int):
    return db.query(_models.Movie).filter(_models.Movie.id == movie_id).first()


#ACTOR

async def get_actor_by_name(db: _orm.Session, name: str):
    return db.query(_models.Actor).filter(_models.Actor.name == name).first()

async def create_actor(db: _orm.Session, actor: _schemas.ActorCreate):
    db_actor = _models.Actor(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor   

async def get_actor(db: _orm.Session, actor_id: int):
    return db.query(_models.Actor).filter(_models.Actor.id == actor_id).first()
