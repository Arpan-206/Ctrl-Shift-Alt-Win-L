from fastapi import FastAPI, HTTPException
from db import *
from helpers import *
from schema import *
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()


@app.get("/suggest_movies/{current_param}")
async def suggest_movies(current_param: str):
    url = f"http://www.omdbapi.com/?apikey={os.getenv('OMDB_API_KEY')}&s={current_param}"
    response = requests.get(url)
    # return a list of all titles
    response_json = response.json()
    if 'Search' not in response_json:
        return HTTPException(status_code=404, detail="No movies found")
    lis = []
    for movie in response_json['Search']:
        lis.append(movie['Title'])
    return lis


@app.post("/movies/")
async def create_movie(movie: MovieCreate):
    with Session(engine) as session:
        movie = create_movie(session, movie)
        return movie
    
@app.get("/{user_id}/movies/")
async def get_movies_by_user_id(user_id: str):
    with Session(engine) as session:
        movies = get_movies_by_user_id(session, user_id)
        return movies

@app.get("/movie/{movie_id}")
async def get_movie_by_id(movie_id: str):
    with Session(engine) as session:
        movie = get_movie_by_id(session, movie_id)
        return movie
    
@app.put("/movie/{movie_id}")
async def update_movie(movie_id: str, movie: MovieCreate):
    with Session(engine) as session:
        movie = update_movie(session, movie_id, movie)
        return movie


@app.on_event("startup")
def on_startup():
    create_db_and_tables()