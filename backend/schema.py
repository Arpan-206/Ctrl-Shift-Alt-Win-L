from models import *
from pydantic import BaseModel
import datetime as da
class MovieBase(BaseModel):
    imdb_id: str
    title: str
    year: int
    plot: str
    poster: str
    genre: str
    date_watched: str
    review: str
    rating: int
    user_id: str

class MovieUpdate(MovieBase):
    pass

class MovieCreate:
    imdb_id: str | None

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True