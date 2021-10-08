import sqlalchemy.orm as _orm
import database as _database, models as _models, schemas as _schemas


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_movie_by_title(db: _orm.Session, title: str):
    return db.query(_models.Movie).filter(_models.Movie.title == title).first()

def create_movie(db: _orm.Session, movie: _schemas.MovieCreate):
    db_movie = _models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.Movie).offset(skip).limit(limit).all()

def get_movie(db: _orm.Session, movie_id: int):
    return db.query(_models.Movie).filter(_models.Movie.id == movie_id).first()

def get_actor_by_name(db: _orm.Session, name: str):
    return db.query(_models.Actor).filter(_models.Actor.name == name).first()

def create_actor(db: _orm.Session, actor: _schemas.ActorCreate):
    db_actor = _models.Actor(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor   
