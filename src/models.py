import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import database as _database
import passlib.hash as _hash


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
        
class MovieActor(_database.Base):
    __tablename__ = "movie_actor"
    movie_id = _sql.Column(_sql.Integer, _sql.ForeignKey("movies.id"), primary_key=True)
    actor_id = _sql.Column(_sql.Integer, _sql.ForeignKey("actors.id"), primary_key=True) 

class Movie(_database.Base):
    __tablename__ = "movies"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, unique=True, index=True)
    categories = _sql.Column(_sql.String)
    insertion_date = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    release_date = _sql.Column(_sql.Integer)
    director = _sql.Column(_sql.String)
    synopsis = _sql.Column(_sql.String)
    actors = _orm.relationship("Actor", secondary="movie_actor", back_populates="movies", cascade="all, delete")


class Actor(_database.Base):
    __tablename__ = "actors"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, index=True)
    movies = _orm.relationship("Movie", secondary="movie_actor", back_populates="actors", cascade="all, delete")