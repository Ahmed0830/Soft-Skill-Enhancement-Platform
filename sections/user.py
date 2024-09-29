import streamlit as st
import database
import base64
from PIL import Image
from io import BytesIO
def show_user_profile():
    st.markdown(f"""<h2 class = "title">User Profile</h2>
              """, unsafe_allow_html=True)
    # st.title("User Profile")
    if 'username' in st.session_state:
        email = database.get_user(st.session_state.username)
        st.session_state.name = database.get_details(email, 'name')
        st.session_state.age = database.get_details(email, 'age')
        st.session_state.bio = database.get_details(email, 'bio')
        st.session_state.email = database.get_details(email, 'email')
# Use the CSS class for the image
        if email:
            st.markdown(
                """
            <style>
            .title{
                font-family: Raleway;
                text-align: left;
                }
            .stImage{
            # display: flex;
            # justify-content: center;
            }
            .stContainer > div{ width: 80%; margin: auto; }
            .profile-card {
            # border: 1px solid #ddd;
            # border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            # width: 80%;
            text-align: center;

        }
        .name {
            font-size: 18px;
        }
        img{
        border-radius: 15px;
        width: 170px;
        height: 170px;
        object-fit: cover;
        }
        .profile-data{
        # text-align: left;
        font-family: RaleWay;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        }
        .row {
            display: flex;
            justify-content: space-between;
            width: 100%;
        }
        .cell {
            flex: 1;
            padding: 15px;
            text-align: justify;
            }
          </style>
        """, unsafe_allow_html=True) 
            with open("textfiles/profile_default.txt", "r", encoding='utf-8') as file:
                content = file.read()
            profile_pic_base64 = content
            container = st.container(border=True)
            with container:
                if email.get('profile_pic'):
                    profile_pic_data = base64.b64decode(email['profile_pic'])
                    profile_pic_base64 = base64.b64encode(profile_pic_data).decode('utf-8')
                    image = Image.open(BytesIO(profile_pic_data))
                    section1, section2 = st.columns([1, 3])
                    with section1:
                        st.image(image)
                    # st.markdown(f"""<div class = "profile-card">
                    # <div class = "profile-data">
                    # <div class = "row">
                    # <p class = "cell name">
                    col1, col2 = st.columns(2)
                    with section2:
                        with st.container(border=True):
                            st.markdown( 
                            f"""
                            <h5 class = "title">Title: Vocabulary Virtuoso</h5>
                            """, unsafe_allow_html=True)
                            st.write(f"Name: {st.session_state.get('name', 'Anonymous User')}")
                            st.write("DOB: 23-09-1978")
                        if st.button("Update Profile"):
                                show_profile_completion()
                    with col1:
                        with st.container(border=True):
                            st.write(f"Name: {st.session_state.get('name', 'Anonymous User')}")
                        with st.container(border=True):
                            st.write(f"Email: {st.session_state.get('email')}")
                    with col2:
                        with st.container(border=True):
                            # st.write(f"Age: {st.session_state.get('age', 'Not provided')}")
                            st.write("Phone Number: "+ "+91-9391838342")
                        with st.container(border=True):
                            st.write(f"Bio: {st.session_state.get('bio', 'Not provided')}")
                    # st.write(f"Name: st.session_state.get('name', 'Anonymous User'))")
                             
                    # <p class = "cell email">
                    # st.write(f"Email: {st.session_state.get('email')}")
                    # </p>
                    # </div>
                    # <div class = "row">
                    # <p class = "cell age">
                    # st.write(f"Age: {st.session_state.get('age', 'Not provided')}")
                    # </p>
                    # <p class = "cell bio">
                    # st.write(f"Bio: {st.session_state.get('bio', 'Not provided')}")
                    # </p>
                    # </div>
                    # </div>
                    # </div>
                    # """, unsafe_allow_html=True)    
                else:
                    st.error("User not found.")
            
    else:
        st.error("You need to log in to view your profile.")

def show_profile_completion():
    with st.form(key = "update-form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        profile_pic = st.file_uploader("Profile Pic", type=["png", "jpg", "jpeg"])
        bio = st.text_area("Bio")
        
        update_user = st.form_submit_button('Update Profile')
        if update_user:
            profile_pic_data = None
            if profile_pic is not None:
                image = Image.open(profile_pic)
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                profile_pic_data = base64.b64encode(buffered.getvalue()).decode()
            database.update_user(st.session_state.username, name, age, "I'm an actor", profile_pic_data)



    