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
from coronavirus.preprocessor.preprocessor import (consolidate_country_regions,
                                                   get_top_n_countries)


def load_country_rates_page():
    # Get the data
    db = DataBase('COVID-19.db')
    data_type = st.sidebar.selectbox(label='Select data', options=['DEATHS', 'CONFIRMED', 'RECOVERED'], index=0)
    if data_type == 'CONFIRMED': 
        response = 'confirmed'
        df = db.read_table_to_dataframe('jh_global_confirmed', response)
        # df = db.load_jh_world_df()
    elif data_type == 'DEATHS': 
        response = 'deaths'
        df = db.read_table_to_dataframe('jh_global_deaths', response)
        # df = db.load_jh_world_df()
    else: 
        response = 'recovered'
        df = db.read_table_to_dataframe('jh_global_recovered', response)
        # df = db.load_jh_world_df()

    # Select Country row by dropping all rows where province/state != None
    st.header("Countries over Time")
    df = consolidate_country_regions(df)

    n = st.sidebar.number_input(label='Top number of countries to plot',
                                min_value=1,
                                value=5)

    top_countries = get_top_n_countries(df, n, response)
    selected_countries = st.sidebar.multiselect(
        'Select countries',
        list(df['country/region'].sort_values().unique()),
        default = top_countries)
    
    log_scale = st.sidebar.checkbox("Log Scale", value=False)
    x_num_cases = st.sidebar.checkbox("Days Since 10,000 Cases")
    # TODO: scale df to date of x number of cases

    countries_df = df[df['country/region'].isin(selected_countries)]
    month_ticks = np.unique(countries_df['date'].values.astype('datetime64[M]')).astype('datetime64',copy=False)
    
    if log_scale:
        countries_df = countries_df.loc[countries_df[response] != 0]
        line_plot = alt.Chart(countries_df).mark_line().encode(
                        alt.Y(response + ':Q', scale=alt.Scale(type='log')),
                        x='date' + ':T',
                        # y=response + ':Q',
                        color='country/region' + ':N'
                    )
    else:
        line_plot = alt.Chart(countries_df).mark_line().encode(
                        x='date' + ':T',
                        y=response + ':Q',
                        color='country/region' + ':N'
                    )

    st.altair_chart(line_plot, use_container_width=True)
    st.write(countries_df)
