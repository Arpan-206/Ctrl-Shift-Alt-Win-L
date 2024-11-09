import openai
import db
from dotenv import load_dotenv
import os
from helpers import *
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

def find_similar_movies_via_ai(genre, plot, year):
    prompt = (
        f"Generate movie recommendations based on the user's recently watched movie details. "
        f"The movie has the following details: Genre: {genre}, Plot Summary: {plot}, and Year: {year}. "
        f"Identify movies that have a similar feel, theme, or storyline but are set in different time periods. "
        f"List movie titles that fit these criteria, capturing similar theme but offering unique settings."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a movie recommendation engine make sure that there are no duplicate recommendations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    
    recommended_movies = response['choices'][0]['message']['content'].strip().split('\n')
    result = []
    for title in recommended_movies:
        if title:
            result.append({"title": title})
    return result


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
    for film in recommendations:
        print(f"Recommended: {film['title']}")


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

    user_movies = [{"imdb_id": "tt0111161"}, {"imdb_id": "tt0111161"}]
    with next(db.get_session()) as session:
        triage_request('recommend', user_id, user_movies=user_movies, session=session)
