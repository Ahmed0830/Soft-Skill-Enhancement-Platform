import streamlit as st
import database
import base64
def show_user_profile():
    st.title("User Profile")

    if 'username' in st.session_state:
        user = database.get_user(st.session_state.username)
        if user:
            st.markdown(
    """
    <style>
    .stImage{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100px;
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the CSS class for the image
            if user:
                if user.get('profile_pic'):
                    profile_pic_data = base64.b64decode(user['profile_pic'])
                    st.image(profile_pic_data, width=100)
            st.write(f"Email: {user['email']}")
            st.write(f"Name: {user.get('name', 'Not provided')}")
            st.write(f"Age: {user.get('age', 'Not provided')}")
            st.write(f"Bio: {user.get('bio', 'Not provided')}")
        
        else:
            st.error("User not found.")
        
    else:
        st.error("You need to log in to view your profile.")

    