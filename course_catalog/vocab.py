import streamlit as st
from dotenv import load_dotenv
import os
import cohere
import random

load_dotenv(".env")
cohere_token = os.getenv("cohere_token")
co = cohere.Client(cohere_token)

# preamble="""## Task & Context
# You are helping with vocabulary practice, so generate random words according to difficulty, and different word everytime"""
def generate_words(level):
    prompts = ["Generate one {level} vocabulary word, its definition, and 3 example sentences using the word.", "Provide a {level} vocabulary word along with its definition and three example sentences demonstrating its use.", "Generate a single {level} vocabulary word, define it, and construct three example sentences with that word.", "Create one {level} vocabulary term, include its definition, and give three sentences as examples using this word."]

    message = random.choice(prompts).format(level=level)
    response = co.generate(prompt=message, temperature=0.7)

    return response.generations[0].text.strip()


def sentence_completion(word):
    message = f"Create a sentence with {word}."
    response = co.chat(message=message)
    return response.text
# def check_sentence(sentence, word):
#     message = f"Does this {word} fit into blank of this {sentence}. Say Correct for yes and Wrong for no"
#     response = co.chat(message=message)
#     return response.text

def generate_synonym(word):
    message = f"Generate 5 synonyms for the word '{word}'."
    response = co.chat(message=message)
    return response.text

def generate_antonym(word):
    message = f"Generate 5 antonyms for the word '{word}'."
    response = co.chat(message=message)
    return response.text

def generate_assessment(level):
    prompts = ["Generate one {level} vocabulary word,  without any additional information.", "Provide a {level} vocabulary word, without any additional information.", "Generate a single {level} vocabulary word, without any additional information.", "Create one {level} vocabulary term,  without any additional information."]
    message = random.choice(prompts).format(level=level)
    response = co.chat(message=message)
    return response.text

def checkDefine(user_define, word):
    message = f"Is '{user_define}' the correct definition of '{word}'? Answer 'Yes' or 'No' only."
    response = co.chat(message=message)
    return response.text

def vocabulary_practice():
    if 'word' not in st.session_state:
        st.session_state.word = ""
    if 'user_define' not in st.session_state:
        st.session_state.user_define = ""
    st.markdown("""
            <style>
                .title{
                font-family: Raleway;
                }
                </style>
                """, unsafe_allow_html=True)
    

    with open("textfiles/vocab_guide.txt", "r", encoding='utf-8') as file:
        content = file.read()
        container = st.container(border=True)
        with container:
            st.markdown( 
                f"""
                <h4 class = "title">Tips and Tricks for Vocabulary Practice📖</h4>
                            """, unsafe_allow_html=True)
            st.write(content)
        st.markdown( 
                f"""
                <h3 class = "title">Vocabulary Practice</h3>
                            """, unsafe_allow_html=True)
    # st.title("Vocabulary Practice")
    with st.container(border=True): 
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
    st.markdown( 
                f"""
                <h3 class = "title">Assess Your Vocabulary</h3>
                            """, unsafe_allow_html=True)
    # st.title("Assess Your Vocabulary")
    with st.container(border=True): 
        selected = st.selectbox('Choose an assessment',
        ('Word Definition', 'Sentence Completion', 'Synonym Practice', 'Antonym Practice'))
        if selected == "Word Definition":
            level = st.selectbox("Select assessment level", ("easy", "medium", "hard"))
            user_define = ""
            word = ""
            if st.button("Generate Word"):
                st.session_state.word = generate_assessment(level)
                st.write(st.session_state.word)
            st.session_state.user_define = st.text_input("Define the word", st.session_state.user_define)

            if st.button("Check"):
                if st.session_state.user_define:
                    output = checkDefine(st.session_state.user_define, st.session_state.word)
                    st.session_state.output = output
                    st.write(st.session_state.output)
                else:
                    st.write("No definition entered!")
