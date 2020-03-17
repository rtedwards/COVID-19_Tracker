import pandas as pd
import geopandas as gpd
import joblib
import folium
import numpy as np
import os
import streamlit as st
from utilities import list_all_tags, is_tag, find_tag
from preprocessor import load_data

pd.set_option('display.max_colwidth', -1)

df = load_data(type=time_series)

data_type = streamlit.selectbox(label='Select data', options=['CONFIRMED', 'DEATHS', 'RECOVERED'], index=0)
if data_type == 'CONFIRMED': 
    response = 'confirmed'
elif data_type == 'DEATHS': 
    response = 'deaths'
else: 
    response = 'recovered'

# Select Date
current_date = df['date'].max()
date = st.date_input("Select Date:", value=current_date)