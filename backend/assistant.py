import openai
import db
import requests
from swarm import Agent
from swarm.agents import create_triage_agent
from swarm.repl import run_demo_loop
from db import get_movie_details
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")


def recommend_movies(user_movies):
    recommendations = []
    
    for movie in user_movies:
        movie_details = get_movie_details(movie['imdb_id'])
        
        if movie_details:
            similar_movies = find_similar_movies(movie_details['genre'], movie_details['plot'], movie_details['year'])
            recommendations.extend(similar_movies)
    
    return recommendations

def find_similar_movies(genre, plot, year):
    similar_movies = []
    year_range = range(year - 40, year + 40)  
    
    for year in year_range:
        url = f"http://www.omdbapi.com/?s={genre}&y={year}&apikey={os.getenv('OMDB_API_KEY')}"
        response = requests.get(url)
        data = response.json()
        
        if data['Response'] == 'True':
            for movie in data['Search']:
                similar_movies.append({
                    "title": movie['Title'],
                    "imdb_id": movie['imdbID'],
                    "genre": genre,
                    "year": year,
                    "plot": plot
                })
    return similar_movies

def log_watched_movie(user_id, imdb_id):
    movie_details = get_movie_details(imdb_id)
    if movie_details:
        db.log_movie(user_id, imdb_id, movie_details['title'], movie_details['year'], movie_details['genre'])

def log_movie_agent_function(user_id, imdb_id):
    log_watched_movie(user_id, imdb_id)
    print(f"Movie {imdb_id} logged successfully for user {user_id}.")

movie_logging_agent = Agent(
    name="Movie Logging Agent",
    description="""This agent logs the movie watched by the user using the IMDb ID.
    It will store the details of the movie such as the title, genre, and year in the database.""",
    functions=[log_movie_agent_function],
)

movie_recommendation_agent = Agent(
    name="Movie Recommendation Agent",
    description="""You are a movie recommendation agent that suggests movies based on the user's recently watched films.
    You will suggest movies that have similar genres and themes but are from a different time period. 
    You must ask for the IMDb IDs of recent movies watched to suggest recommendations.""",
    functions=[recommend_movies, log_watched_movie],
)

triage_agent = create_triage_agent(
    name="Triage Agent",
    instructions="""You are to triage a user's request and transfer to the right agent.
    If the user wants to get movie recommendations, transfer to the Movie Recommendation Agent.
    If the user wants to log a movie they watched, transfer to the Movie Logging Agent.""",
    agents=[movie_recommendation_agent, movie_logging_agent],
    add_backlinks=True,
)

if __name__ == "__main__":
    run_demo_loop(triage_agent, debug=False)
