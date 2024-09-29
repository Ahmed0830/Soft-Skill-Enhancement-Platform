import streamlit as st
from dotenv import load_dotenv
import os
import cohere

load_dotenv(".env")
cohere_token = os.getenv("cohere_token")
co = cohere.Client(cohere_token)

def generate_passage(level):
    message = f"Generate {level} passage for reading practice, without any additional text"
    response = co.chat(message=message)
    st.write(response.text)

def reading():
    st.markdown("""
            <style>
                .title{
                font-family: Raleway;
                }
                </style>
                """, unsafe_allow_html=True)
    

    with open("textfiles/reading_tips.txt", "r", encoding='utf-8') as file:
        content = file.read()
        container = st.container(border=True)
        with container:
            st.markdown( 
                f"""
                <h4 class = "title">Tips and Tricks for Reading Practice📖</h4>
                            """, unsafe_allow_html=True)
            st.write(content)
    st.title("Practice Reading 👇")
    level = st.selectbox('Choose difficulty level', ('easy', 'medium', 'hard'))
    if st.button('Start Reading'):
        generate_passage(level)
