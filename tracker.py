import pandas as pd
import geopandas as gpd
import joblib
import folium
import os
import streamlit as st
from utilities import list_all_tags, is_tag, find_tag

DATA_DIR = '/Users/Berto/Projects/COVID-19_Tracker/COVID-19/csse_covid_19_data/csse_covid_19_time_series'
CONFIRMED = os.path.join(DATA_DIR, "time_series_19-covid-Confirmed.csv")
DEATHS = os.path.join(DATA_DIR, "time_series_19-covid-Deaths.csv")
RECOVERED = os.path.join(DATA_DIR, "time_series_19-covid-Recovered.csv")

confirmed_df = pd.read_csv(CONFIRMED)
deaths_df = pd.read_csv(DEATHS)
recovered_df = pd.read_csv(RECOVERED)