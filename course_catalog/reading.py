import streamlit as st
import requests
import random
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_passage(level):
    seed = random.randint(0, 10000)
    
    prompt = f"Generate a {level} passage for reading practice. Seed: {seed}, Don't generate the seed"
    response = query(({"inputs": prompt}))
    if 'generated_text' in response[0]:
        generated_text = response[0]['generated_text']
        generated_text = generated_text[len(prompt):]
        st.write(generated_text)
