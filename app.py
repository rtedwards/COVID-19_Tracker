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
from coronavirus.pages.world_map import load_world_map_page
from coronavirus.pages.country_line_plots import load_country_line_plots_page


# pd.set_option('display.max_colwidth', -1)

chart_type = st.sidebar.selectbox(label='Plot type', options=["Line Plots","World Map"])

if chart_type == "Line Plots":
    load_country_line_plots_page()

if chart_type == "World Map": 
    load_world_map_page()

# Sources
# TODO: display_sources() utility function
st.markdown(
    "Sources:  \n\
    [Johns Hopkins](https://github.com/CSSEGISandData/COVID-19)  \n\
    [Google](https://www.google.com/covid19/mobility/)  \n\
    [World Bank](api.worldbank.org/v2/en/indicator/EN.POP.DNST?downloadformat=csv)  \n\
    ")
st.markdown(
    "Github: [github.com/rtedwards](https://github.com/rtedwards/coronavirus-tracker)"
)