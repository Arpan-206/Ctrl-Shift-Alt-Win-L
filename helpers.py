from models import *
from db import *
import os
from dotenv import load_dotenv
import requests

load_dotenv()


def create_movie(session: Session, movie: Movie):
    # check if the movie wit the same imdb_id and user_id already exists
    existing_movie = session.exec(select(Movie).where(Movie.imdb_id == movie.imdb_id, Movie.user_id == movie.user_id)).first()
    if existing_movie:
        return existing_movie
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

def get_imdb_id_from_title(title: str):
    url = f"http://www.omdbapi.com/?t={title}&apikey={os.getenv('OMDB_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "True":
        return data["imdbID"]
    else:
        return None
    
def get_movie_details(imdb_id: str):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={os.getenv('OMDB_API_KEY')}"
    try:
        response = requests.get(url)

        if response.status_code != 200:
            return None
        
        data = response.json()

        if data["Response"] == "True":
            year = data["Year"]
            
            if "–" in year:
                year = year.split("–")[0]
            
            try:
                year = int(year)
            except ValueError:
                print(f"Invalid year format: {year}")
                year = None 

            return {
                "title": data["Title"],
                "genre": data["Genre"],
                "plot": data["Plot"],
                "year": year,
                "poster": data["Poster"],
            }
        else:
            print(f"Movie with IMDb ID {imdb_id} not found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"JSON decoding error: {e}")
        return None


def create_movie_from_imdb_id(imdb_id: str, user_id: str, session: Session, date_watched, review, rating):
    movie_details = get_movie_details(imdb_id)
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


def timeline_generator(session: Session, user_id: str):
    movies = (
        session.exec(select(Movie).where(Movie.user_id == user_id))
        .all()
    )
    # Sort the movies by date_watched
    movies.sort(key=lambda x: x.date_watched)
    for movie in movies:
        yield movie
    


def get_movie_by_title(session: Session, title: str):
    movie = session.exec(select(Movie).where(Movie.title == title)).first()
    return movie


def get_movie_title_api(title: str):
    url = f"http://www.omdbapi.com/?t={title}&apikey={os.getenv('OMDB_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "True":
        return data["Title"]
    else:
        return None


# Test the functions
def test_functions():
    session = Session(engine)
    test_id = "tt0111161"
    test_user_id = "test_user"
    h = get_movie_details(test_id)
    mv = create_movie_from_imdb_id(test_id, test_user_id, session, "2021-10-10", "Great movie", 10)
    print(mv)
    print(get_movie_by_id(session, 1))
    print(get_movie_by_title(session, h["title"]))
    print(get_movie_title_api(h["title"]))
    print(list(timeline_generator(session, test_user_id)))
    session.close()

