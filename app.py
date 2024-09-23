import streamlit as st
from streamlit_option_menu import option_menu
from sections.courses import show_course_catalog
from sections.login import show_login, show_registration
from sections.user import show_user_profile
from course_catalog.vocab import vocabulary_practice
from course_catalog.speech import speech_practice
from course_catalog.reading import generate_passage
from course_catalog.pro import pronunciation
import database
from io import BytesIO
from PIL import Image
import base64
page_title = "Soft Skill Trainer"
page_icon = "🤸‍♂️"

layout = "centered"

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_title+ "" + page_icon)

def main():
    # Initialize session state to toggle between login, registration, and other views
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Initialize session state to track page views
    if 'courses' not in st.session_state:
        st.session_state.courses = [
        {"title": "Vocabulary Practice", "description": "Enhance your language skills by mastering new words and their meanings through engaging vocabulary practice."},
        {"title": "Pronunciation Practice", "description": "Improve your spoken clarity and accent with focused pronunciation practice exercises."},
        {"title": "Speech Practice", "description": "Build confidence and fluency in spoken language through targeted speech practice sessions."},
        {"title": "Reading Practice", "description": "Build confidence and fluency in reading english through targeted reading practice sessions."},
    ]
    
    if 'show_profile_completion' not in st.session_state:
        st.session_state.show_profile_completion = False
    if 'show_user_profile' not in st.session_state:
        st.session_state.show_user_profile = False
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False

    if st.session_state.logged_in:
        selected = option_menu(
        menu_title = None,
        options = ["Course Catalog", "View Profile", "Logout"],
        icons = ["book", "person-circle", "box-arrow-right"],
        orientation = "horizontal"
        )

        if selected == "Course Catalog":
            st.session_state.show_course_catalog = True  # Hide course catalog when viewing profile
            st.session_state.show_profile = False  # Show profile on main page
        if selected == "View Profile":
            st.session_state.show_profile = True  # Hide profile when viewing course catalog
            st.session_state.show_user_profile = True
            st.session_state.show_course_catalog = False  # Set to show course catalog
            st.session_state.enrolled_course = False
            st.session_state.show_profile_completion = False
        if selected == "Logout":
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.show_course_catalog = False    
            st.session_state.show_profile = False
            st.session_state.enrolled_course = False
            st.rerun()
        
        if 'enrolled_course' in st.session_state:
            if st.session_state.enrolled_course == "Vocabulary Practice":
                vocabulary_practice()
                st.session_state.show_course_catalog = False
            elif st.session_state.enrolled_course == "Speech Practice":
                st.session_state.show_course_catalog = False
                st.title("Tips and Tricks for Speech Practice🗣️")

                with open("speech_tips.txt", "r", encoding='utf-8') as file:
                    content = file.read()
                st.write(content)
                st.title("Practice Your Speech Here 👇")
                if st.button('Start Recording'):
                    speech_practice()
            elif st.session_state.enrolled_course == "Reading Practice":
                st.session_state.show_course_catalog = False
                st.title("Tips and Tricks for Reading Practice📖")
                with open("reading_tips.txt", "r", encoding='utf-8') as file:
                    content = file.read()
                st.write(content)
                st.title("Practice Reading 👇")
                level = st.selectbox('Choose difficulty level', ('easy', 'medium', 'hard'))
                if st.button('Start Reading'):
                    generate_passage(level)
            elif st.session_state.enrolled_course == "Pronunciation Practice":
                st.session_state.show_course_catalog = False
                st.title("Guide to proper pronunciation: 🗣️")

                with open("pronunciation_guide.txt", "r", encoding='utf-8') as file:
                    content = file.read()
                st.write(content)
                pronunciation()
        if 'show_profile_completion' not in st.session_state:
            st.session_state["show_profile_completion"] = False

        if st.session_state["show_profile_completion"]:
            user = database.get_user(st.session_state.username)
            if user and ('name' not in user or 'age' not in user or 'bio' not in user or 'profile_pic_data' not in user):
                profile_pic = st.file_uploader("Profile Pic", type=["png", "jpg", "jpeg"])
                name = st.text_input("Name")
                age = st.number_input("Age", min_value=0)
                bio = st.text_area("Bio")
                if st.button("update user"):
                    profile_pic_data = None
                    if profile_pic is not None:
                        image = Image.open(profile_pic)
                        buffered = BytesIO()
                        image.save(buffered, format="JPEG")
                        profile_pic_data = base64.b64encode(buffered.getvalue()).decode()
                    database.update_user(st.session_state.username, name, age, bio, profile_pic_data)
                    st.session_state["show_profile_completion"] = False
            else:
                st.session_state["show_profile_completion"] = False   

        # Render content based on the selected sidebar option
        if st.session_state.show_course_catalog:
            show_course_catalog()
        elif st.session_state.show_profile:
            show_user_profile()
    elif st.session_state.show_registration:
        show_registration()
          
    else:
        show_login()

if __name__ == "__main__":
    main()
