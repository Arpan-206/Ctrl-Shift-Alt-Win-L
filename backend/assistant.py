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
