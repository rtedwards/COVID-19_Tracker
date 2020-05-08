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
from coronavirus.db_utils.db_utils import DataBase
from coronavirus.preprocessor.preprocessor import (consolidate_country_regions,
                                                   get_top_n_countries)

def get_totals():
    """Displays total deaths, confirmed, and recovered"""
    db = DataBase('COVID-19.db')
    confirmed_df = db.read_table_to_dataframe('jh_global_confirmed', 'confirmed')
    deaths_df = db.read_table_to_dataframe('jh_global_deaths', 'deaths')
    recovered_df = db.read_table_to_dataframe('jh_global_recovered', 'recovered')

    confirmed_df = consolidate_country_regions(confirmed_df)
    deaths_df = consolidate_country_regions(deaths_df)
    recovered_df = consolidate_country_regions(recovered_df)

    confirmed_df = get_most_recent_numbers(confirmed_df)
    deaths_df = get_most_recent_numbers(deaths_df)
    recovered_df = get_most_recent_numbers(recovered_df)

    confirmed_total = confirmed_df['confirmed'].sum()
    deaths_total = deaths_df['deaths'].sum()
    recovered_total = recovered_df['recovered'].sum()

    return  confirmed_total, deaths_total, recovered_total

def get_most_recent_numbers(df):
    """Returns most recent data"""
    return df.loc[df['date'] == df['date'].max()]

def string_of_spaces(n):
    """
    Creates a string of html spaces

    :param n {int}: number of spaces
    """
    return "&nbsp;" * n