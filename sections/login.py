import streamlit as st
import database

#User logs in
def show_login():
    with st.form(key='login_form'):
        st.write("Please enter your login details:")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        login_button = st.form_submit_button("Login")
        if login_button:
            if database.check_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username

                user = database.get_user(username)
                if not user.get("name") or not user.get("age") or not user.get("bio"):
                    st.session_state.show_profile_completion = True
                st.rerun()
                
            else:
                st.error("Invalid username or password. Please try again.")

    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state.show_registration = True
        
#New User registers 
def show_registration():
    with st.form(key='registration_form'):
        st.write("Please enter your registration details:")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        register_button = st.form_submit_button("Register")
        if register_button:
            if not username or not password or not confirm_password:
                st.error("All fields are required!")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            elif database.get_user(username):
                st.error("Username already exists!")
            else:
                database.insert_user(username, password)
                st.success("Registration successful! You can now log in.")
                st.session_state.show_registration = False
            

    st.write("Already have an account?")
    if st.button("Back to Login"):
        st.session_state.show_registration = False

