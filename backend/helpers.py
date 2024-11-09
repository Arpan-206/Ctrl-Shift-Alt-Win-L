from models import *
from db import *
import os
from dotenv import load_dotenv
import requests

load_dotenv()


def create_movie(session: Session, movie: Movie):
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


def get_movies_by_user_id(session: Session, user_id: str):
    return session.exec(select(Movie).where(Movie.user_id == user_id)).all()


def get_movie_by_id(session: Session, movie_id: str):
    return session.get(Movie, movie_id)


def update_movie(session: Session, movie_id: str, movie: Movie):
    existing_movie = session.get(Movie, movie_id)
    if existing_movie:
        existing_movie.update_from_dict(movie.dict())
        session.commit()
        session.refresh(existing_movie)
        return existing_movie
    return None


def get_movie_details(imdb_id: str):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={os.getenv('OMDB_API_KEY')}"
    response = requests.get(url)
    data = response.json()

    if data["Response"] == "True":
        return {
            "title": data["Title"],
            "genre": data["Genre"],
            "plot": data["Plot"],
            "year": int(data["Year"]),
            "poster": data["Poster"],
        }
    else:
        print(f"Movie with IMDb ID {imdb_id} not found.")
        return None
    
def create_movie_from_imdb_id(imdb_id: str, user_id: str, session: Session):
    movie_details = get_movie_details(imdb_id, session)
    if movie_details:
        movie = Movie(
            imdb_id=imdb_id,
            title=movie_details["title"],
            genre=movie_details["genre"],
            plot=movie_details["plot"],
            year=movie_details["year"],
            user_id=user_id,
            date_watched=date_watched,
            review=review,
            rating=rating,
            poster=movie_details["poster"],
        )
        return create_movie(session, movie)
    else:
        return None