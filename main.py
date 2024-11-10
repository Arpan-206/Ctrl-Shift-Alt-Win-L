from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.middleware.cors import CORSMiddleware
from db import *
from helpers import *
from schema import *
from assistant import *
import requests
from dotenv import load_dotenv
import os
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

load_dotenv()


app = FastAPI()

security = HTTPBasic()

origins = [
    "*",
    "null",
    "http://localhost",
    "http://localhost:8080",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    # get a list of all userids
    with next(get_session()) as session:
        users = session.exec(select(User)).all()
        # list of all usernames but in bytes
        usernames = [user.user_id.encode("utf8") for user in users]
        if credentials.username.encode("utf8") not in usernames:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        
        correct_password = session.exec(select(User).where(User.user_id == credentials.username)).first().password.encode("utf8")
        is_correct_password = secrets.compare_digest(
            credentials.password.encode("utf-8"), correct_password
        )
        if not is_correct_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        
    return credentials.username

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

# Register a new user
@app.post("/register/")
async def register_user(user: UserCreate):
    with next(get_session()) as session:
        # check if the user already exists
        existing_user = session.exec(select(User).where(User.user_id == user.user_id)).first()
        if existing_user:
            return HTTPException(status_code=409, detail="User already exists")
        user = User.from_orm(user)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    

@app.post("/movies/")
async def cr_movie(
    movie: MovieCreate,
    credentials: HTTPBasicCredentials = Depends(security)
):
    user_id = get_current_username(credentials)
    if not movie.imdb_id:
        movie.imdb_id = get_imdb_id_from_title(movie.title)
        if not movie.imdb_id:
            return HTTPException(status_code=404, detail="IMDB ID not found")
    
    with next(get_session()) as session:
        # check if the movie with the same imdb_id and user_id already exists
        existing_movie = session.exec(select(Movie).where(Movie.imdb_id == movie.imdb_id, Movie.user_id == user_id)).first()
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
            user_id=user_id,
        )

        return create_movie(session, movie)
    
@app.get("/movies/")
async def mv_by_userid(
    credentials: HTTPBasicCredentials = Depends(security)
):
    user_id = get_current_username(credentials)
    with next(get_session()) as session:
        movies = get_movies_by_user_id(session, user_id)
        if not movies or len(movies) == 0:
            return HTTPException(status_code=404, detail="No movies found")
        return movies



@app.put("/movie/{movie_id}")
async def update_movie(movie_id: str, movie: MovieUpdate, credentials: HTTPBasicCredentials = Depends(security)):
    user_id = get_current_username(credentials)
    with Session(engine) as session:
        # check if movie exists
        existing_movie = get_movie_by_id(session, movie_id)
        if not existing_movie:
            return HTTPException(status_code=404, detail="Movie not found")
        # check if the movie has the same user_id
        if existing_movie.user_id != user_id:
            return HTTPException(status_code=403, detail="Unauthorized")
        movie = update_movie(session, movie_id, movie)

        return movie


# recommended movies
@app.get("/recommend_movies/")
async def recommend_movie(credentials: HTTPBasicCredentials = Depends(security)):
    with next(get_session()) as session:
        user_id = get_current_username(credentials)
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
