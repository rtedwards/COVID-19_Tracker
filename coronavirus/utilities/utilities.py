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

# TODO: get date of x number of cases reached
def get_date_of_x_cases_reached(df, x):
    """
    Determines the date hit n number of cases were reached

    :param df: pandas df
    :param x {int}: number of cases
    """
    pass

# TODO: create column of days since x number of cases reached
def add_column_date_of_x_cases_reached(df, x):
    """
    create column of days since x number of cases reached
    :param df: pandas df
    :param x {int}: number of cases
    """
    pass

# TODO: create column of cases each day
def add_column_cases_per_day(df, response, name):
    """
    Create column of number of cases since previous day
    :param df: pandas df sorted by date in ascending
    :param reponse {str}: the response column to calculate rate
    :param name {str}: new column name
    """
    # Sort by ascending so the inevitable NaN of first row is the first day 
    # not the current day
    rate_df = df.sort_values(by='date', ascending=True)

    # TODO: make groupby 'country/region' 'state/province' agnostic
    # TODO: probably wrap this in a class
    def calculate_rate(x):
        return x - x.shift(1)

    # Select response, groupby country, calculate rate, transform back to df
    rate_df[name] = rate_df.groupby(['country/region'])[response].transform(calculate_rate)
    # rate_df[name] = rate_df['country/region'].map(rate_df.groupby(['country/region'])[response].calculate_rate())

    rate_df = rate_df.reindex(columns=['country/region', response, 
                                        name, 'date'])
    return rate_df.sort_values(by='date', ascending=False)
