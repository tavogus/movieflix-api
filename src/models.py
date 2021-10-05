import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import database as _database


class Movie(_database.Base):
    __tablename__ = "movies"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, unique=True, index=True)
    categories = _sql.column(_sql.ARRAY(_sql.String))
    insertion_date = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    release_date = _sql.Column(_sql.Integer)
    director = _sql.column(_sql.String)
    synopsis = _sql.column(_sql.String)
    actors = _sql.column(_sql.ARRAY(_sql.String))


class Actor(_database.Base):
    __tablename__ = "actors"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, index=True)