from models import *
from pydantic import BaseModel

class MovieBase(BaseModel):
    imdb_id: str
    title: str
    year: int
    plot: str
    poster: str
    date_watched: str
    review: str
    rating: int
    user_id: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True