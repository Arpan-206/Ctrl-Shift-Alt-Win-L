'''
import openai
openai.api_key = "your_openai_api_key"

file_response = openai.File.create(
  file=open("log_data.csv", "rb"),
  purpose='fine-tune'
)

file_id = file_response["id"]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a data visualizer and movie recommendation assistant."},
        {"role": "user", "content": "Generate movie recommendations based on the user's recently watched films. Use the provided IMDb IDs to retrieve detailed information for each movie, including full plot summaries, genres, and release years. Analyse each movie's plot and genre to identify similar themes and features that define its content.Recommend movies that align closely with these but are set in a different time period. Specifically, find movies that have a similar feel, theme, or storyline but in a differnt setting. "}
    ],
    tools=[
        {
            "type": "code_interpreter",
            "resource": {"file_ids": [file_id]}
        }
    ]
)

print(response)
'''
import openai
import db
from swarm import Agent
from swarm.agents import create_triage_agent
from swarm.repl import run_demo_loop

openai.api_key = 'add a key :(' 

def get_movie_details(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=your_omdb_api_key"
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

def recommend_movies(user_movies):
    recommendations = []
    
    for movie in user_movies:
        movie_details = get_movie_details(movie['imdb_id'])
        
        if movie_details:
            similar_movies = find_similar_movies(movie_details['genre'], movie_details['plot'], movie_details['year'])
            recommendations.extend(similar_movies)
    
    return recommendations

def find_similar_movies(genre, plot, year):
    # NEED TO USE OMDb API HERE 
    return [
        {"title": "Movie 1", "imdb_id": "tt1234567", "genre": genre, "year": year + 20, "plot": "A similar plot from a different time period."},
        {"title": "Movie 2", "imdb_id": "tt2345678", "genre": genre, "year": year - 15, "plot": "Another similar plot with a twist in a different era."}
    ]

def log_watched_movie(user_id, imdb_id):
    movie_details = get_movie_details(imdb_id)
    if movie_details:
        db.log_movie(user_id, imdb_id, movie_details['title'], movie_details['year'], movie_details['genre'])

def suggest_movies(user_id):
    recent_movies = db.get_recent_movies(user_id)
    
    recommendations = recommend_movies(recent_movies)
    
    for rec in recommendations:
        print(f"Recommended: {rec['title']} ({rec['year']}) - Genre: {rec['genre']}")
    

movie_recommendation_agent = Agent(
    name="Movie Recommendation Agent",
    description="""You are a movie recommendation agent that suggests movies based on the user's recently watched films.
    You will suggest movies that have similar genres and themes but are from a different time period. 
    You must ask for the IMDb IDs of recent movies watched to suggest recommendations.""",
    functions=[suggest_movies, log_watched_movie],
)

triage_agent = create_triage_agent(
    name="Triage Agent",
    instructions="""You are to triage a user's request and transfer to the right agent.
    If the user wants to get movie recommendations, transfer to the Movie Recommendation Agent.
    If the user wants to log a movie they watched, transfer to the Movie Logging Agent.""",
    agents=[movie_recommendation_agent],
    add_backlinks=True,
)

if __name__ == "__main__":
    run_demo_loop(triage_agent, debug=False)
