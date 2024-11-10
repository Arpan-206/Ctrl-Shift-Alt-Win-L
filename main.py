from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from db import *
from helpers import *
from schema import *
from assistant import *
import requests
from dotenv import load_dotenv
import os
from fastapi_auth0 import Auth0, Auth0User



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

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def cr_movie(
    movie: MovieCreate,
    user: Auth0User = Security(auth.get_user),
):

    if not movie.imdb_id:
        movie.imdb_id = get_imdb_id_from_title(movie.title)
        if not movie.imdb_id:
            return HTTPException(status_code=404, detail="IMDB ID not found")
    
    with Session(engine) as session:
        # check if the movie with the same imdb_id and user_id already exists
        existing_movie = session.exec(select(Movie).where(Movie.imdb_id == movie.imdb_id, Movie.user_id == user.id)).first()
        if existing_movie:
            return HTTPException(status_code=409, detail="Movie already exists")
    
        mv_data = get_movie_details(movie.imdb_id)
        if not mv_data:
            return HTTPException(status_code=404, detail="Movie not found")
        movie = MovieBase(
            title=movie.title,
            imdb_id=movie.imdb_id,
            year=mv_data["year"],
            plot=mv_data["plot"],
            poster=mv_data["poster"],
            genre=mv_data["genre"],
            date_watched=movie.date_watched,
            review=movie.review,
            rating=movie.rating,
            user_id=user.id,
        )

        return create_movie(session, movie)
    
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
async def recommend_movie(user: Auth0User = Security(auth.get_user)):
    with next(get_session()) as session:
        user_id = user.id
        user_movies = get_user_movie_history(user_id, session)
        recommendations = json.loads(handle_movie_recommendation_request(user_movies, session))

        for recommendation in recommendations:
            # add movie data from omdb
            movie_data = get_movie_details(recommendation["IMDb ID"])
            recommendation["Year"] = movie_data["year"]
            recommendation["Plot"] = movie_data["plot"]
            recommendation["Poster"] = movie_data["poster"]
            recommendation["Genre"] = movie_data["genre"]

        return recommendations



@app.on_event("startup")
def on_startup():
    create_db_and_tables()
