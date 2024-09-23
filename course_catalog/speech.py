import speech_recognition as sr
import requests
import streamlit as st
from gtts import gTTS
import io
import pygame
from dotenv import load_dotenv
import os
load_dotenv(".env")
token = os.getenv("token")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": "Bearer "+ token}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
# Initialize recognizer
def speech_practice():
   
    recognizer = sr.Recognizer()
   
    # Use the microphone as source for input
    with sr.Microphone() as source:
        st.write("Say something:")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            st.write("You said: " + text)
        except sr.UnknownValueError:
            st.write("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            st.write("Could not request results from Google Web Speech API; {0}".format(e))
        prompt = f"Consider yourself an actual person, and respond to this {text}"
        response = query({"inputs": prompt})
        if 'generated_text' in response[0]:
            generated_text = response[0]['generated_text']
                # Process the response to remove the prompt if included
            generated_text = generated_text[len(prompt):]
            st.write(generated_text)
            tts = gTTS(text=generated_text, lang='en',slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
# if st.button("Start Recording"):
#     speech_practice()