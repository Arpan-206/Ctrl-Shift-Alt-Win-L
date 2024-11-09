import openai
import db
from dotenv import load_dotenv
import os
from helpers import *
import json
from sqlalchemy.orm import Session

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

def find_similar_movies_via_ai(genre, plot, year):
    prompt = (
        f"Generate movie recommendations based on the user's recently watched films. Use the provided IMDb IDs to retrieve detailed information for each movie, including full plot summaries, genres, and release years. Analyse each movie's plot and genre to identify similar themes and features that define its content.Recommend movies that align closely with these but are set in a different time period. Specifically, find movies that have a similar feel, theme, or storyline but in a differnt setting. The movies selected should be from different time periods check 40 years ahead and behind the year inputed"
        f"Details: Genre: {genre}, Plot Summary: {plot}, Year: {year}. "
        f"For each recommended movie, provide the title, IMDb ID, and a reason in the following format:\n"
        f"Title: <movie title>\nIMDb ID: <imdb_id>\nReason: <detailed reason related to the movie>\n\n"
        f"Recommendations should reflect similar themes or character dynamics in unique settings or time periods."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a movie recommendation engine generating structured responses."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )
    
    recommendations = []
    response_text = response['choices'][0]['message']['content'].strip().split('\n\n')
    
    for item in response_text:
        lines = item.split('\n')
        title = imdb_id = reason = ""
        
        for line in lines:
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
            elif line.startswith("IMDb ID:"):
                imdb_id = line.replace("IMDb ID:", "").strip()
            elif line.startswith("Reason:"):
                reason = line.replace("Reason:", "").strip()
        
        if title and imdb_id and reason:
            recommendations.append({
                "title": title,
                "imdb_id": imdb_id,
                "reason": f'* "{title}" {reason}'
            })
    
    return recommendations


def recommend_movies(user_movies):
    recommendations = []
    
    for movie in user_movies:
        movie_details = get_movie_details(movie['imdb_id'])
        
        if movie_details:
            similar_movies = find_similar_movies_via_ai(
                genre=movie_details['genre'],
                plot=movie_details['plot'],
                year=movie_details['year']
            )
            recommendations.extend(similar_movies)
    
    return recommendations


def log_watched_movie(user_id, imdb_id, session: Session):
    movie_details = get_movie_details(imdb_id)
    if movie_details:
        create_movie_from_imdb_id(imdb_id, user_id, session, "2021-10-10", "Great movie", 8)


def handle_movie_logging_request(user_id, imdb_id, session: Session):
    log_watched_movie(user_id, imdb_id, session)
    print(f"Movie {imdb_id} logged successfully for user {user_id}.")


def handle_movie_recommendation_request(user_movies, session: Session):
    recommendations = recommend_movies(user_movies)
    recommendations_json = json.dumps(recommendations, indent=4)  # Format as JSON
    print("Recommendations in JSON format:")
    print(recommendations_json)


def triage_request(request_type, user_id, imdb_id=None, user_movies=None, session: Session = None):
    if request_type == 'log' and imdb_id:
        handle_movie_logging_request(user_id, imdb_id, session)   
    elif request_type == 'recommend' and user_movies:
        handle_movie_recommendation_request(user_movies, session)  
    else:
        print("Invalid request type or missing parameters.")


if __name__ == "__main__":
    user_id = "user123"
    imdb_id = "tt0111161"

    with next(db.get_session()) as session:
        triage_request('log', user_id, imdb_id=imdb_id, session=session)   

    user_movies = [{"imdb_id": "tt0111161"}, {"imdb_id": "tt13186482"}]
    with next(db.get_session()) as session:
        triage_request('recommend', user_id, user_movies=user_movies, session=session)