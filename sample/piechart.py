 # col1  , col2 , col3 = st.columns(3)
    # with col1:
    #     st.subheader("Total")
    #     data = sm_cli.ApiMarketingMixTotal_TrafficSourcesOverview()
    #     chart_data={
    #         'header': data['Desktop'].keys(),
    #         'Total': data['Total'].values(),
    #         'Desktop': data['Desktop'].values(),
    #         'MobileWeb': data['MobileWeb'].values()
    #     }
    #     df = pd.DataFrame(chart_data)
    #     fig = px.pie(df, values='Total', names='header',
    #              height=300, width=200)
    #     fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    #     st.plotly_chart(fig, use_container_width=True)
    # with col2:
    #     st.subheader("Desktop")
    #     chart_data={
    #         'header': data['Desktop'].keys(),
    #         'Total': data['Total'].values(),
    #         'Desktop': data['Desktop'].values(),
    #         'MobileWeb': data['MobileWeb'].values()
    #     }
    #     df = pd.DataFrame(chart_data)
    #     fig = px.pie(df, values='MobileWeb', names='header',
    #              height=300, width=200)
    #     fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    #     st.plotly_chart(fig, use_container_width=True)
    # with col3:
    #     chart_data={
    #         'header': data['Desktop'].keys(),
    #         'Total': data['Total'].values(),
    #         'Desktop': data['Desktop'].values(),
    #         'MobileWeb': data['MobileWeb'].values()
    #     }
    #     st.subheader("Mobile")
    #     df = pd.DataFrame(chart_data)
    #     fig = px.pie(df, values='MobileWeb', names='header',
    #              height=300, width=200, color_discrete_map={
    #                 "Organic Search": '#636EFA',
    #                 "Social":  '#EF553B',
    #                 "Email":  '#00CC96',
    #                 "Display Ads": '#AB63FA',
    #                 "Direct": '#FFA15A',
    #                 "Referrals":  '#19D3F3',
    #                 "Paid Search": '#FF6692'                    
    #              })
    #     fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    #     logging.info(fig)
    #     st.plotly_chart(fig, use_container_width=True)