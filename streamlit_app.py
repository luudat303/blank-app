import streamlit as st
import numpy as np

menu_items={"Google.com","youtube.com"}
st.set_page_config( layout='wide',
                    initial_sidebar_state="collapsed",
                    menu_items={
                        'Get Help': 'https://www.extremelycoolapp.com/help',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!"
                    })
st.title("Project research")
st.subheader("Project Name")
with st.form('project'):
    left, middle, right = st.columns([2,1,1], vertical_alignment="bottom")

    left.text_input("Write something")
    right.checkbox("Check me")
    middle.form_submit_button("click me")

