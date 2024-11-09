import openai
import db
import requests
from dotenv import load_dotenv
import os
from helpers import *
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")


def get_movie_details(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={os.getenv('OMDB_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    
    if data['Response'] == 'True':
        return {
            "title": data['Title'],
            "genre": data['Genre'],
            "plot": data['Plot'],
            "year": int(data['Year']),
        }
    else:
        print(f"Movie with IMDb ID {imdb_id} not found.")
        return None


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


def recommend_movies(user_movies):
    recommendations = []
    
    for movie in user_movies:
        movie_details = get_movie_details(movie['imdb_id'])
        
        if movie_details:
            similar_movies = find_similar_movies(movie_details['genre'], movie_details['plot'], movie_details['year'])
            recommendations.append(similar_movies)
    
    return recommendations


def log_watched_movie(user_id, imdb_id):
    movie_details = get_movie_details(imdb_id)
    if movie_details:
        db.log_movie(user_id, imdb_id, movie_details['title'], movie_details['year'], movie_details['genre'])


def handle_movie_logging_request(user_id, imdb_id):
    log_watched_movie(user_id, imdb_id)
    print(f"Movie {imdb_id} logged successfully for user {user_id}.")


def handle_movie_recommendation_request(user_movies):
    recommendations = recommend_movies(user_movies)
    for film in recommendations:
        print(f"Recommended: {film['title']} ({film['year']}) - Genre: {film['genre']}")


def triage_request(request_type, user_id, imdb_id=None, user_movies=None):
    if request_type == 'log' and imdb_id:
        handle_movie_logging_request(user_id, imdb_id)
    elif request_type == 'recommend' and user_movies:
        handle_movie_recommendation_request(user_movies)
    else:
        print("Invalid request type or missing parameters.")


if __name__ == "__main__":
    user_id = "user123"
    imdb_id = "tt1234567"
    
    triage_request('log', user_id, imdb_id=imdb_id)
    
    user_movies = [{"imdb_id": "tt9876543"}, {"imdb_id": "tt2345678"}]
    triage_request('recommend', user_id, user_movies=user_movies)
