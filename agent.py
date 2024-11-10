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

# Initialize recognizer

r = sr.Recognizer()

def listen():
    # listen once
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not get that")
            return ""
        except sr.RequestError:
            print("Sorry, I did not get that")
            return ""


def openai_initial_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a bunch of agents wearing a trench coat under the name, Journey. Your collective goal is to help users log movies they've watched and provide movie recommendations."},
            {"role": "system", "content": "Your personal role is of just a manager, aa triage. You are responsible for managing the user requests and delegating them to the right agent. You can only answer using one of 4 words: 'help', 'recommend', 'log', 'exit'."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    response_text = response['choices'][0]['message']['content']
    return response_text 

def main():
    while True:
        text = listen()
        if text == "exit":
            break
        response = openai_initial_response(text)
        speak(response)

if __name__ == "__main__":
    main()