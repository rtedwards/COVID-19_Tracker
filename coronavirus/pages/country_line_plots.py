import pandas as pd
import geopandas as gpd
import joblib
import folium
import urllib
import json
import numpy as np
import os
import altair as alt
import streamlit as st
# from coronavirus.preprocessor.preprocessor import load_data
from coronavirus.mapper.mapper import choropleth_map
from coronavirus.db_utils.db_utils import DataBase


def load_country_line_plots_page():
    # Get the data
    db = DataBase('COVID-19.db')

    data_type = st.sidebar.selectbox(label='Select data', options=['DEATHS', 'CONFIRMED', 'RECOVERED'], index=0)
    if data_type == 'CONFIRMED': 
        df = db.read_table_to_dataframe('jh_global_confirmed')
        response = 'confirmed'
        df['date'] = pd.to_datetime(df['date']).dt.normalize()
    elif data_type == 'DEATHS': 
        df = db.read_table_to_dataframe('jh_global_deaths')
        response = 'deaths'
    else: 
        df = db.read_table_to_dataframe('jh_global_recovered')
        response = 'recovered'

    st.header("Countries over Time")
        # Choose Countries
    selected_countries = st.sidebar.multiselect(
        'Select countries',
        list(df['country/region'].sort_values().unique()),
        default = ['US', 'United Kingdom', 'Italy', 'Spain', 'France', 'Germany'] )
    
    # st.write('Plotting the following countries:', selected_countries)

    countries_df = df[df['country/region'].isin(selected_countries)]

    month_ticks = np.unique(countries_df['date'].values.astype('datetime64[M]')).astype('datetime64',copy=False)
    print(month_ticks)
    line_plot = alt.Chart(countries_df).mark_line().encode(
                    x='date:T',
                    y=response + ':Q',
                    color='country/region' + ':N'
                )
    st.altair_chart(line_plot, use_container_width=True)
    st.write(countries_df)
