import streamlit as st 
from modules.redisClient import redis_cli 
from modules.similarweb import SimilarWeb
import json 
import plotly.express as px
import plotly.graph_objects as go
import logging
import pandas as pd
import numpy as np

st.set_page_config(layout='wide',
                    initial_sidebar_state="collapsed",
                    page_icon="⚙️")
st.title("Research")
sm_cli = SimilarWeb()
cookies = redis_cli.get_key("SIMILAR_WEB_COOKIES")
sm_cli.set_cookies(json.loads(cookies))
with st.form("search"):
    search_project,submit_search = st.columns([5,1], vertical_alignment="bottom")
    with search_project:
        project_name =  st.text_input("**Project Name**")
    with submit_search:
        st.form_submit_button("Search",use_container_width=True,type="primary")

def get_project_overview():

    data= {"site":"theluxurycloset.com","tags":["closet","luxury"],"title":"designer online luxury shopping usa | the luxury closet","description":"at the luxury closet usa, save up to 90% off rrp on authentic, new and pre-loved luxury brands. shop watches, bags, shoes for both men & women.","category":"Lifestyle/Jewelry_and_Luxury_Products","yearFounded":"Lifestyle/Jewelry_and_Luxury_Products","globalRanking":72520}
    
    with project_info:
        html = "<table style='width: 100%;'>"
        html += f"<tr><td>Title</td><td>{data['title']}</td></tr>"
        html += f"<tr><td>Description</td><td>{data['description']}</td></tr>"
        html += f"<tr><td>Category</td><td>{data['category']}</td></tr>"
        html += f"<tr><td>Year Founded</td><td>{data['yearFounded']} seconds</td></tr>"
        html += f"<tr><td>Global Ranking</td><td>{data['globalRanking']}</td></tr>"
        html += "</table>"
        st.markdown(html,unsafe_allow_html=True)


def get_project_traffic():
    data = sm_cli.ApiWebsiteOverview_EngagementOverview()
    col1  , col2 = st.columns([2,2])
    
    html = "<table style='width: 100%;'>"
    html += "<tr><th>Metric</th><th>Value</th></tr>"
    html += f"<tr><td>Bounce Rate</td><td>{data['BounceRate']:.2%}</td></tr>"
    html += f"<tr><td>Avg Month Visits</td><td>{data['AvgMonthVisits']:,.0f}</td></tr>"
    html += f"<tr><td>Avg Visit Duration</td><td>{data['AvgVisitDuration']:,.2f} seconds</td></tr>"
    html += f"<tr><td>Pages Per Visit</td><td>{data['PagesPerVisit']:,.2f}</td></tr>"
    html += f"<tr><td>Total Pages Views</td><td>{data['TotalPagesViews']:,.0f}</td></tr>"
    html += "</table>"
    st.markdown(html,unsafe_allow_html=True)

@st.fragment()
def get_traffic_source():
    data = sm_cli.ApiMarketingMixTotal_TrafficSourcesOverview()
    
    chart_data = pd.DataFrame({
        "columns": data['Desktop'].keys(),
        "Total": data['Total'].values(),
        "Desktop": data['Desktop'].values(),
        "MobileWeb": data['MobileWeb'].values()
    })
  
    @st.fragment()
    def get_chart(data):
        
            source_type = st.selectbox("Source Type",['Total','Desktop','MobileWeb'])
            df = pd.DataFrame(data)
            fig = px.pie(df, values=source_type, names='columns',
                 height=300, width=200, color_discrete_map={
                    "Organic Search": '#636EFA',
                    "Social":  '#EF553B',
                    "Email":  '#00CC96',
                    "Display Ads": '#AB63FA',
                    "Direct": '#FFA15A',
                    "Referrals":  '#19D3F3',
                    "Paid Search": '#FF6692'                    
                  })
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
            st.plotly_chart(fig, use_container_width=True)
    col1, col2  = st.columns([1,2])
    with col1:      
        get_chart(chart_data)
    with col2:
        st.bar_chart(
           chart_data,
            x="columns",
            y= ['Desktop', 'MobileWeb'],
            horizontal=True,
            stack=False
        )
    
def branch_key():
    data = sm_cli.ApiSearchBrandedKeywordsWorldWide_Branded()
    chart_data={
        'columns': data.keys(),
        'value': data.values() 
    }
    df = pd.DataFrame(chart_data)
    
    fig = px.pie(df, values='value', names='columns',
                 height=300, width=200,)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)
    
@st.fragment()
def sm_keyworld():
    with st.form("Select"):
        col1, col2, col3 = st.columns([1,2,1],vertical_alignment="bottom")
        with col1:
            country = st.text_input("Country",value=999)
        with col2:
            source_type = st.selectbox('Source Type',['Total','Desktop','MobileWeb'])
        with col3:
            st.form_submit_button(use_container_width=True)
    data = sm_cli.ApiNewSearchKeywordsWorldWide_Keyword(country=country, webSource=source_type)
    st.table(data)
    
if project_name:
    sm_cli.set_domain(project_name)
    st.markdown(f'''
        <h2 style='text-align: center; color: grey;'><a href="https://{project_name}">https://{project_name}</a></h2>''',unsafe_allow_html=True)
    st.divider()
    project_info, project_overview = st.columns([2,2])
    with project_info:
        get_project_overview()
    # with project_overview:
    #     get_project_traffic()
    ###############################
    # get_traffic_source()
    ###############################
    st.divider()
    # Keyword
    # col1, col2 = st.columns([1,3])
    # with col1:
    #     branch_key()
    # with col2:
    #      sm_keyworld()
    # st.divider()
    

