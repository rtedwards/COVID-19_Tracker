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

URL = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
# URL = f'https://github.com/datasets/geo-countries/tree/master/data/countries.geojson'
COUNTRY_GEO = f'{URL}/world-countries.json'
STATE_GEO = f'{URL}/us-states.json'

pd.set_option('display.max_colwidth', -1)

## Pull Johns Hopklins Data
# Should set these url paths as environment variables
# CONFIRMED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
# DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
# RECOVERED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

# # db = DataBase('database.sqlite3')
# db = dbu.DataBase('COVID-19.db')
# db.pull_data(url=CONFIRMED, name='jh_global_confirmed', csv=True)
# db.pull_data(url=DEATHS, name='jh_global_deaths', csv=True)
# db.pull_data(url=RECOVERED, name='jh_global_recovered', csv=True)

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


chart_type = st.sidebar.selectbox(label='Plot type', options=["Lineplot","Map"])

if chart_type == "Lineplot":
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


## Choropleth Maps
if chart_type == "Map": 
    st.header("World Map")

    # Select Date
    df['date'] = pd.to_datetime(df['date']).apply(lambda x: x.date())
    # st.write(df['date'])
    # current_date = pd.to_datetime(df['date'].max()).date()
    current_date = df['date'].max()
    st.write(current_date)

    date = st.sidebar.date_input("Select Date:", value=current_date)

    st.write(date)
    df = df.loc[df['date'] == date]
    st.write(df)

    # Merge ISO2 Codes
    link = "http://country.io/names.json"
    f = urllib.request.urlopen(link)

    country_json = f.read().decode("utf-8")
    country_ISO2 = json.loads(country_json)
    country_ISO2_df = pd.DataFrame(country_ISO2.items(), columns=['ISO2 Code','country/region'])

    st.subheader("Loading ISO2 Codes")
    df = pd.merge(df, country_ISO2_df, on='country/region', how='inner')
    st.write(df)

    # Merge ISO3 Codes
    link = "http://country.io/iso3.json"
    f = urllib.request.urlopen(link)

    country_json = f.read().decode("utf-8")
    country_ISO3 = json.loads(country_json)
    country_ISO3_df = pd.DataFrame(country_ISO3.items(), columns=['ISO2 Code','ISO3 Code'])

    st.subheader("Loading ISO3 Codes")
    df = pd.merge(df, country_ISO3_df, on='ISO2 Code', how='inner')
    st.write(df)

    # Create map
    active_map = choropleth_map(df,
                                columns=['ISO3 Code', response],
                                geo_data=COUNTRY_GEO,
                                color='YlGn',
                                legend='Cases')
    st.write(type(active_map))
    st.write(active_map._repr_html_(), unsafe_allow_html=True)
    st.write(active_map, unsafe_allow_html=True)
    st.write(df)