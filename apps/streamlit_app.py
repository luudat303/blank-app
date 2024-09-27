import streamlit as st
import numpy as np
import warnings
from modules.redisClient import redis_cli
warnings.filterwarnings('ignore')

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
st.write(redis_cli.get_key('key1'))