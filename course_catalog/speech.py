import speech_recognition as sr
import streamlit as st
from gtts import gTTS
import io
import pygame
from dotenv import load_dotenv
import os
import cohere
load_dotenv(".env")
cohere_token = os.getenv("cohere_token")

co = cohere.Client(cohere_token)

preamble="""## Task & Context
You are a friend, not an AI chatbot, keep it short, fun, upbeat and conversational"""

# Initialize recognizer
def speech_practice():
    st.markdown("""
            <style>
                .title{
                font-family: Raleway;
                }
                </style>
                """, unsafe_allow_html=True)
    

    with open("textfiles/speech_tips.txt", "r", encoding='utf-8') as file:
        content = file.read()
        container = st.container(border=True)
        with container:
            st.markdown( 
                f"""
                <h4 class = "title">Tips and Tricks for Speech Practice🗣️</h4>
                            """, unsafe_allow_html=True)
            st.write(content)
    st.title("Practice Your Speech Here 👇")
    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
    
        # Use the microphone as source for input
        with sr.Microphone() as source:
            st.write("Say something:")
            audio = recognizer.listen(source)
            
            try:
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio)
                st.write("You said: " + text)
            except sr.UnknownValueError:
                st.write("Google Web Speech API could not understand audio")
            except sr.RequestError as e:
                st.write("Could not request results from Google Web Speech API; {0}".format(e))
            if text:
                chat_history = []
                chat_history.append({"role": "User", "text": text})
                response = co.chat(message=text, preamble=preamble, chat_history=chat_history) 
                chat_history.append({"role": "Chatbot", "text": response.text})
                
                # Make it more upbeat and conversational
                # message = "Make it more upbeat and conversational."
                # chat_history.append({"role": "User", "text": message})
                # response = co.chat(message=message, preamble=preamble, chat_history=chat_history)
                
                # chat_history.append({"role": "Chatbot", "text": response.text})
                
                st.write(response.text)
                tts = gTTS(text=response.text, lang='en',slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                pygame.mixer.init()
                pygame.mixer.music.load(fp)
                pygame.mixer.music.play()
