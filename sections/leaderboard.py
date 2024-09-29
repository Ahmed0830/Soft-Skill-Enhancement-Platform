import streamlit as st
import pandas as pd
from database import get_leaderboard

def create_dataframe(leaderboard):
    df = pd.DataFrame(leaderboard)
    return df
def leaderboard():
    # st.table(df)
    
    st.markdown("""
    <style>
    .container{
                border: 2px solid #FFEB3B;
                border-radius: 15px;
                margin-top: 1em;
                width: 80%; 
                margin-left: 8em;
                margin-top: 4.6em;
                padding: 15px;
                }      
    .leaderboard-title {
        font-size: 1.5em;
        color: #FFA500;
        text-align: center;
        # margin-left: 7em;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
    }
    .leaderboard-container {
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
    }
    .leaderboard-item {
        display: flex;
        justify-content: space-between;
        background-color: transparent;
        border: 1px solid #FFEB3B;
        border-radius: 15px;
        padding: 15px;
        margin-left: 1.3em;
                margin-right: 1.3em;
        margin-bottom: 5px;
        margin-top: 5px;
        width: 100%;
        text-align: center;
        font-size: 1.2em;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    # .leaderboard-item.even {
    #     background-color: #FFC107;
    # }
    # .leaderboard-item.odd {
    #     background-color: #FFEB3B;
    # }
    </style>
    """, unsafe_allow_html=True)
    # st.markdown('<div class = "container">', unsafe_allow_html=True)
    # st.markdown('<div class="leaderboard-title">🏅 Top Scorers 🏅</div>', unsafe_allow_html=True)
    # leaderboard = get_leaderboard()
    # # df = create_dataframe(leaderboard)
    # # st.write(leaderboard)
    # st.markdown('<div class="leaderboard-container">', unsafe_allow_html=True)
    # for index, entry in enumerate(leaderboard):
    #     name = entry['name']
    #     score = entry['daily_score']
    #     if index % 2 == 0:
    #         st.markdown(f'<div class="leaderboard-item" style="background-color: #FFC107;"><div>{name} </div><span class = "score">{score}</span></div>', unsafe_allow_html=True)
    #     else:
    #         st.markdown(f'<div class="leaderboard-item" style="background-color: #FFEB3B;"><div>{name} </div><span class = "score">{score}</span></div>', unsafe_allow_html=True)

    # st.markdown('</div>', unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)
    leaderboard = get_leaderboard()
    html_content = """
        <div class="container">
    <div class="leaderboard-title">🏅 Top Scorers 🏅</div>
    <div class="leaderboard-container">
        """
    for index, entry in enumerate(leaderboard):
        name = entry['name']
        score = entry['daily_score']
        class_name = "even" if index % 2 == 0 else "odd"
        html_content += f'<div class="leaderboard-item {class_name}"><div>{name}</div><span class="score">{score}</span></div>'

    html_content += """
        </div>
    </div>"""

    st.markdown(html_content, unsafe_allow_html=True)
