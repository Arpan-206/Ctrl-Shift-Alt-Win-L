from fastapi import FastAPI, HTTPException, Depends, Security
from db import *
from helpers import *
from schema import *
import requests
from dotenv import load_dotenv
import os
from fastapi_auth0 import Auth0, Auth0User
import datetime

load_dotenv()

auth = Auth0(
    domain=os.getenv("AUTH0_DOMAIN"),
    api_audience=os.getenv("AUTH0_API_AUDIENCE"),
    scopes={
        "create:movies": "Create movies",
        "read:movies": "Read movies",
        "update:movies": "Update movies",
        "delete:movies": "Delete movies",
        "read:recommendations": "Read recommendations",
    },
)
app = FastAPI()


@app.get("/suggest_movies/{current_param}")
async def suggest_movies(current_param: str):
    url = (
        f"http://www.omdbapi.com/?apikey={os.getenv('OMDB_API_KEY')}&s={current_param}"
    )
    response = requests.get(url)
    # return a list of all titles
    response_json = response.json()
    if "Search" not in response_json:
        return HTTPException(status_code=404, detail="No movies found")
    lis = []
    for movie in response_json["Search"]:
        lis.append(movie["Title"])
    return lis


@app.post("/movies/", dependencies=[Depends(auth.implicit_scheme)])
async def create_movie(
    movie: MovieCreate,
    user: Auth0User = Security(auth.get_user),
):
    print(movie)
    # check if atleast one of the parameters is provided
    if not movie.imdb_id and not movie.title:
        return HTTPException(status_code=400, detail="Either imdb_id or title must be provided")
    movie.user_id = user.id
    with Session(engine) as session:
        movie = create_movie(session, movie)
        return movie


@app.get("/movies/", dependencies=[Depends(auth.implicit_scheme)])
async def mv_by_userid(
    user: Auth0User = Security(auth.get_user)
):
    user_id = user.id
    with Session(engine) as session:
        movies = get_movies_by_user_id(session, user_id)
        if not movies or len(movies) == 0:
            return HTTPException(status_code=404, detail="No movies found")
        return movies



@app.put("/movie/{movie_id}", dependencies=[Depends(auth.implicit_scheme)])
async def update_movie(movie_id: str, movie: MovieUpdate, user: Auth0User = Security(auth.get_user)):
    with Session(engine) as session:
        # check if movie exists
        existing_movie = get_movie_by_id(session, movie_id)
        if not existing_movie:
            return HTTPException(status_code=404, detail="Movie not found")
        # check if the movie has the same user_id
        if existing_movie.user_id != user.id:
            return HTTPException(status_code=403, detail="Unauthorized")
        movie = update_movie(session, movie_id, movie)

        return movie


# recommended movies
@app.get("/recommend_movies/", dependencies=[Depends(auth.implicit_scheme)])
async def recommend_movies(user: Auth0User = Security(auth.get_user)):
    with Session(engine) as session:
        user_id = user.id
        user_movies = get_movies_by_user_id(session, user_id)
        if not user_movies:
            return HTTPException(status_code=404, detail="No movies found")
        recommendations = []
        for movie in user_movies:
            movie_details = get_movie_details(movie["imdb_id"])
            if movie_details:
                # dummy data for now
                similar_movies = [
                    {"title": "The Shawshank Redemption", "imdb_id": "tt0111161", "reason": "is a great movie"},
                    {"title": "The Godfather", "imdb_id": "tt0068646", "reason": "is a great movie"},
                    {"title": "The Dark Knight", "imdb_id": "tt0468569", "reason": "is a great movie"},
                ]
                recommendations.extend(similar_movies)
        return recommendations


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
