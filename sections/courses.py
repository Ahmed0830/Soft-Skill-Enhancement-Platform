import streamlit as st
def show_course_catalog():
    st.markdown(f"""<h2 class = "title">Course Catalog</h2>
              """, unsafe_allow_html=True)
    st.markdown(f"""<h4 class = "title">Explore Our Courses👇</h4>
              """, unsafe_allow_html=True)

    # Inject custom CSS for course cards
    st.markdown(
        """
        <style>
        .title{
                font-family: Raleway;
                text-align: left;
                }
        .course-card {
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.2s;
            color: white;
            background-color: transparent;
        }
        .course-card:hover {
            transform: scale(1.02);
        }
        .course-title {
            font-size: 20px;
        }
        .course-description {
            margin: 10px 0;
        }
        .enroll-button {
            background-color: transparent;
            border: 1px solid #ddd;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    for i, course in enumerate(st.session_state.courses):
        # Using HTML to create styled course cards
        st.markdown(
            f"""
            <div class="course-card">
                <div class="course-title">{course["title"]}</div>
                <div class="course-description">{course["description"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"{course['title']}", key=f"practice_{i}"):
            st.session_state.enrolled_course = course["title"]
            st.rerun()