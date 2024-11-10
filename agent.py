import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

def detect_intent(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            
            {"role": "user", "content": text},
        ]

    )

def movie_recommendation_agent():
    speak("You have chosen the movie recommendation agent.")
    # Add your movie recommendation logic here
    speak("Here are some movie recommendations for you.")

def movie_logging_agent():
    speak("You have chosen the movie logging agent.")
    # Add your movie logging logic here
    speak("Please tell me the movie you want to log.")

def main():
    speak("Hello, I am your AI agent. How can I assist you today?")
    while True:
        user_input = listen()
        if user_input:
            intent = detect_intent(user_input)
            if intent == "recommend":
                movie_recommendation_agent()
            elif intent == "log":
                movie_logging_agent()
            elif intent == "exit":
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I can only help with movie recommendations, logging movies, or exiting.")

if __name__ == "__main__":
    main()