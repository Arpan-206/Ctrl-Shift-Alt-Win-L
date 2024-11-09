from typing import Annotated
from sqlmodel import Field, SQLModel, select

# This file is for defining the models only.

class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    imdb_id: str = Field(max_length=100)
    title: str = Field(max_length=100)
    year: int = Field()
    plot: str = Field(max_length=1000)
    poster: str = Field(max_length=1000)
    genre: str = Field(max_length=100)
    date_watched: str = Field(max_length=100) 
    review: str = Field(max_length=1000)
    rating: int = Field()
    user_id: str = Field(max_length=100)
    