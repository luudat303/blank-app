import streamlit as st 
from modules.redisClient import redis_cli 
from modules.similarweb import SimilarWeb
import json 

st.set_page_config(layout='wide',
                    initial_sidebar_state="collapsed",
                    page_icon="⚙️")
st.title("Settings")

with st.form("Import cookies"):
        cookies = st.text_input("Similar web cookies")
        st.form_submit_button()
        
similarweb =  SimilarWeb()
similarweb.set_cookies(cookies)
## Persistent cookies into Redis 
redis_cli.set_key("SIMILAR_WEB_COOKIES", json.dumps(similarweb.cookies))

# cookies = redis_cli.get_key("SIMILAR_WEB_COOKIES")
# st.write(json.loads(cookies))

    