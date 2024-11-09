from models import *
from db import *

def create_movie(session: Session, movie: Movie):
    movie = Movie.from_orm(movie)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

def get_movies_by_user_id(session: Session, user_id: str):
    movies = session.exec(select(Movie).where(Movie.user_id == user_id)).all()
    return movies

def get_movie_by_id(session: Session, movie_id: str):
    movie = session.get(Movie, movie_id)
    return movie

def update_movie(session: Session, movie_id: str, movie: Movie):
    movie = session.get(Movie, movie_id)
    movie = Movie.from_orm(movie)
    movie.update_from_dict(movie.dict())
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie