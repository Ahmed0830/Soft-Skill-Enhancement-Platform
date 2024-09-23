import speech_recognition as sr
import streamlit as st
from gtts import gTTS
import io
import pygame

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
    st.title("Practice Your pronunciation")
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
    