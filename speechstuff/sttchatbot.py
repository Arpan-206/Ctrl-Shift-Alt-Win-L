import openai
import db
from dotenv import load_dotenv
import os
from helpers import *
import json
import requests
from sqlalchemy.orm import Session
from rich import print
from fuzzywuzzy import process

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


def get_user_movie_history(user_id: str, session: Session):
    return get_movies_by_user_id(session, user_id)

def analyze_intent(user_input):
    prompt = f"""
    The following are examples of recommendation requests:
    - "Can you recommend a movie?"
    - "I'm looking for a good film to watch."
    - "Any movie suggestions based on what I've seen?"
    - "What movie should I watch next?"
    - "Give me a suggestion for a movie."
    
    User input: "{user_input}"
    
    Based on this input, answer with either "Yes" if it sounds like a recommendation request,
    or "No" if it does not.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant designed to understand if a user is asking for a movie recommendation. Try to understand the intent and meaning of what the user is asking."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    
    # test
    print("Response:", response)

    try:
        result = response['choices'][0]['message']['content'].strip()
        return result.lower() == "yes"
    except (KeyError, IndexError) as e:
        print(f"Error accessing response: {e}")
        return False

def triage_request(request_type, user_id, imdb_id=None, user_movies=None, session=None, user_input=None):
    if request_type == 'log' and imdb_id:
        handle_logging_request(user_id, imdb_id, session)
    elif request_type == 'recommend' and user_movies:
        handle_recommendation_request(user_movies, session)
    elif request_type == 'check_recommendation' and user_input:
        is_recommendation = analyze_intent(user_input)
        if is_recommendation:
            print("User is asking for a recommendation.")
            handle_recommendation_request(user_movies, session)
        else:
            print("User is not asking for a recommendation.")
    elif request_type == 'log_by_title' and user_input:
        handle_logging_request_by_title(user_input, user_id, session)
    else:
        print("Invalid request type or missing parameters.")


def handle_logging_request(user_id, imdb_id, session):
    movie_details = get_movie_details(imdb_id)
    if movie_details:
        create_movie_from_imdb_id(imdb_id, user_id, session, "2021-10-10", "Great movie", 8)


def handle_logging_request_by_title(user_input, user_id, session):
    imdb_id = get_imdb_id_from_title(user_input)
    
    if imdb_id:
        handle_logging_request(user_id, imdb_id, session)
    else:
        #no exact match
        similar_titles = get_similar_titles(user_input)
        if similar_titles:
            print("I couldn't find an exact match, but here are some similar titles:")
            for index, title in enumerate(similar_titles):
                print(f"{index + 1}. {title}")
            
            user_choice = int(input("Please choose the number of the movie: "))
            chosen_movie = similar_titles[user_choice - 1]
            imdb_id = get_imdb_id_from_title(chosen_movie)
            handle_logging_request(user_id, imdb_id, session)
        else:
            print("No similar titles found.")


def handle_recommendation_request(user_movies, session):
    recommendations = recommend_movies(user_movies)
    recommendations_json = json.dumps(recommendations, indent=4)  
    print("Recommendations:", recommendations_json)


def recommend_movies(user_movies):
    recommendations = []
    for movie in user_movies:
        imdb_id = movie.imdb_id 
        movie_details = get_movie_details(imdb_id)  
        
        if movie_details:
            similar_movies = find_similar_movies_via_ai(
                genre=movie_details['genre'],
                plot=movie_details['plot'],
                year=movie_details['year']
            )
            recommendations.extend(similar_movies)
    
    return recommendations


def find_similar_movies_via_ai(genre, plot, year):
    prompt = (
        f"Generate movie recommendations based on the user's recently watched films. "
        f"Use the provided IMDb IDs to retrieve detailed information for each movie, "
        f"including full plot summaries, genres, and release years. "
        f"Analyse each movie's plot and genre to identify similar themes and features that define its content. "
        f"Recommend movies that align closely with these but are set in a different time period. "
        f"Specifically, find movies that have a similar feel, theme, or storyline but in a different setting. "
        f"The movies selected should be from different time periods, check 40 years ahead and behind the year inputed. "
        f"Details: Genre: {genre}, Plot Summary: {plot}, Year: {year}. "
        f"For each recommended movie, provide the title, IMDb ID, and a reason in the following format, in a JSON format (also only output JSON, don't enclose it in code syntax)\n"
        f"Title: <movie title>\nIMDb ID: <imdb_id>\nReason: <detailed reason related to the movie>\n\n"
        f"Recommendations should reflect similar themes or character dynamics in unique settings or time periods, also the JSON should be perfectly valid everytime consisting only of valid list of recommendations and nothing else."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a movie recommendation engine generating structured responses."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    response_text = response['choices'][0]['message']['content'].strip().split('\n\n')
    try:
        data = json.loads(response_text[0])
    except json.JSONDecodeError as e:
        print(response_text)
        print(f"Error: {e}")
        data = []

    return data


def get_similar_titles(title):
    url = f"http://www.omdbapi.com/?s={title}&apikey={os.getenv('OMDB_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("Response") == "True":
        similar_titles = [movie["Title"] for movie in data["Search"]]
        return similar_titles
    else:
        return []


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


def get_imdb_id_from_title(title: str):
    url = f"http://www.omdbapi.com/?t={title}&apikey={os.getenv('OMDB_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "True":
        return data["imdbID"]
    else:
        return None


def read_user_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":
    user_input = read_user_input_from_file('user_input.txt')
    user_id = "K59hHJDq7e00x4p3s6FBm0foh4Lin2OC@clients"
    imdb_id = "tt0111161"

    with next(db.get_session()) as session:
        user_movies = get_user_movie_history(user_id, session)
        triage_request('check_recommendation', user_id, user_input=user_input, user_movies=user_movies, session=session)
