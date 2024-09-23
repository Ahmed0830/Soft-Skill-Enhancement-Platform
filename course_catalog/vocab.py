import streamlit as st
import requests
import random
from dotenv import load_dotenv
import os
load_dotenv(".env")
token = os.getenv("token")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": "Bearer " +token}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_words(level):
    seed = random.randint(0, 10000)
    prompt = f"Generate one {level} vocabulary word, its definition, and 3 example sentences using the word. Seed: {seed}"
    response = query({"inputs": prompt})
    if 'generated_text' in response[0]:
        generated_text = response[0]['generated_text']
        # Process the response to remove the prompt if included
        generated_text = generated_text[len(prompt):]
        return generated_text

def sentence_completion(word):
    prompt = f"Create a sentence with the word '{word}' and leave a blank for the word."
    response = query({"inputs": prompt})
    if 'generated_text' in response[0]:
        generated_text = response[0]['generated_text']
        generated_text = generated_text[len(prompt):]
        return generated_text

def generate_synonym(word):
    prompt = f"Generate 5 synonyms for the word '{word}'."
    response = query({"inputs": prompt})
    if 'generated_text' in response[0]:
        generated_text = response[0]['generated_text']
        generated_text = generated_text[len(prompt):]
        return generated_text

def generate_antonym(word):
    prompt = f"Generate 5 antonyms for the word '{word}'."
    response = query({"inputs": prompt})
    if 'generated_text' in response[0]:
        generated_text = response[0]['generated_text']
        generated_text = generated_text[len(prompt):]
        return generated_text

def vocabulary_practice():
    st.title("Vocabulary Practice")
    option = st.selectbox(
    'Choose an exercise',
    ('Word Generation', 'Sentence Completion', 'Synonym Practice', 'Antonym Practice')
)
    if option == 'Word Generation':
        level = st.selectbox('Choose difficulty level', ('easy', 'medium', 'hard'))
        if st.button('Generate Words'):
            words = generate_words(level)
            st.write(words)

    elif option == 'Sentence Completion':
        word = st.text_input('Enter a word')
        if st.button('Generate Sentence'):
            sentence = sentence_completion(word)
            st.write(sentence)

    elif option == 'Synonym Practice':
        word = st.text_input('Enter a word')
        if st.button('Generate Synonyms'):
            synonyms = generate_synonym(word)
            st.write(synonyms)

    elif option == 'Antonym Practice':
        word = st.text_input('Enter a word')
        if st.button('Generate Antonyms'):
            antonyms = generate_antonym(word)
            st.write(antonyms)
