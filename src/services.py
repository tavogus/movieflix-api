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
