import speech_recognition as sr
import streamlit as st
from gtts import gTTS
from dotenv import load_dotenv
import os
import io
import pygame
import cohere

load_dotenv(".env")
cohere_token = os.getenv("cohere_token")
co = cohere.Client(cohere_token)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def record_user_audio():
    with sr.Microphone() as source:
        st.write("Recording... Please say the word:")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    return audio

def check_pronunciation(user_audio, expected_word):
    try:
        # Recognize the user's audio
        user_text = recognizer.recognize_google(user_audio)
        st.write("You said: " + user_text)
        return user_text.lower() == expected_word.lower()
    except sr.UnknownValueError:
        st.write("Could not understand audio.")
        return False
    except sr.RequestError as e:
        st.write("Could not request results; {0}".format(e))
        return False

# Streamlit app layout


def get_pronunciation(user_word):

    if user_word:
        # Convert the user-provided word to speech and play it
        pronunciation = f"{user_word}"
        tts = gTTS(text=pronunciation, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
    else:
        pronunciation = f"Please enter a word."
        tts = gTTS(text=pronunciation, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()

def pronunciation():
    st.markdown("""
            <style>
                .title{
                font-family: Raleway;
                }
                .title-pro{
               font-family: Raleway;
                }
                </style>
                """, unsafe_allow_html=True)
    

    with open("textfiles/pronunciation_guide.txt", "r", encoding='utf-8') as file:
        content = file.read()
        container = st.container(border=True)
        with container:
            st.markdown( 
                f"""
                <h4 class = "title">Guide to proper pronunciation: 🗣️</h4>
                            """, unsafe_allow_html=True)
            st.write(content)
    # st.title("Practice Your pronunciation")
    st.markdown('<h2 class="title-pro">Practice Your Pronunciation</h2>', unsafe_allow_html=True)
    st.write("Enter a word below, and we'll pronounce it for you.")

    user_word = st.text_input("Enter a word:")
    if st.button("Pronunce Word"):
        get_pronunciation(user_word)
    if st.button("Try it yourself!"):
        if user_word:
            user_audio = record_user_audio()
            if check_pronunciation(user_audio, user_word):
                pronunciation = f"Good. Your Pronunciation is correct."
                tts = gTTS(text=pronunciation, lang='en', slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                pygame.mixer.init()
                pygame.mixer.music.load(fp)
                pygame.mixer.music.play()
            else:
                pronunciation = f"Try Again! Your Pronunciation is incorrect."
                tts = gTTS(text=pronunciation, lang='en', slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                pygame.mixer.init()
                pygame.mixer.music.load(fp)
                pygame.mixer.music.play()
        else:
            pronunciation = f"Enter a word first"
            tts = gTTS(text=pronunciation, lang='en', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
def generate_word(level):
    prompt = f"Generate a random {level} level word for vocabulary assessment, without any additional information. Just the word, nothing else"
    response = co.chat(message=prompt)
    return response.text.strip('.')
def pronunciation_test():
    daily_score = 0
    score = 0
    st.markdown('<h2 class="title-pro">Assess Your Pronunciation</h2>', unsafe_allow_html=True)
    level = st.selectbox("Select Your Difficulty", ["easy", "medium", "hard"])
    if level:
        word = generate_word(level)
        st.write(word)
        if st.button("Start Recording"):
            audio = record_user_audio()
            if audio:
                if(check_pronunciation(audio, word)):
                    daily_score +=1
                    score +=1
                    st.write("Daily Score: " + str(daily_score) + " " + "Score: " + str(score))
                else:
                    st.write("Wrong")
            else:
                st.write("Record Your Pronunciation, first")
