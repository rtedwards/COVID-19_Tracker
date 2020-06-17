import streamlit as st
import urllib
import json
import pandas as pd
import numpy as np
from pathlib import Path
from coronavirus.db_utils.db_utils import DataBase
from coronavirus.preprocessor.preprocessor import consolidate_country_regions


def get_totals():
    """Displays total deaths, confirmed, and recovered"""
    db = DataBase('COVID-19.db')
    confirmed_df = db.read_table_to_dataframe('jh_global_confirmed',
                                              'confirmed')
    deaths_df = db.read_table_to_dataframe('jh_global_deaths',
                                           'deaths')
    recovered_df = db.read_table_to_dataframe('jh_global_recovered',
                                              'recovered')

    confirmed_df = consolidate_country_regions(confirmed_df)
    deaths_df = consolidate_country_regions(deaths_df)
    recovered_df = consolidate_country_regions(recovered_df)

    confirmed_df = get_most_recent_numbers(confirmed_df)
    deaths_df = get_most_recent_numbers(deaths_df)
    recovered_df = get_most_recent_numbers(recovered_df)

    confirmed_total = confirmed_df['confirmed'].sum()
    deaths_total = deaths_df['deaths'].sum()
    recovered_total = recovered_df['recovered'].sum()

    return confirmed_total, deaths_total, recovered_total


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
    rate_df[name] = (rate_df.groupby(['country/region'])[response]
                     .transform(calculate_rate))

    rate_df = rate_df.reindex(columns=['country/region', response,
                                       name, 'date'])
    return rate_df.sort_values(by='date', ascending=False)


def _max_width_():
    """Workaround in html to not having a 'Wide Mode()' setting"""
    max_width_str = f"max-width: 2000px;"
    st.markdown(f"""
                <style>
                .reportview-container .main .block-container{{ 
                    {max_width_str} }}
                </style>    
                """,
                unsafe_allow_html=True,
                )


def add_ISO2_country_codes(df):
    """Adds ISO2 country codes to dataframe"""
    link = "http://country.io/names.json"
    f = urllib.request.urlopen(link)

    country_json = f.read().decode("utf-8")
    country_ISO2 = json.loads(country_json)
    country_ISO2_df = pd.DataFrame(country_ISO2.items(), columns=['ISO2 Code', 'country/region'])

    return pd.merge(df, country_ISO2_df, on='country/region', how='inner')
    # df.head()


def add_ISO3_country_codes(df):
    """Adds ISO3 country codes to dataframe"""
    link = "http://country.io/iso3.json"
    f = urllib.request.urlopen(link)

    country_json = f.read().decode("utf-8")
    country_ISO3 = json.loads(country_json)
    country_ISO3_df = pd.DataFrame(country_ISO3.items(), columns=['ISO2 Code', 'ISO3 Code'])

    return pd.merge(df, country_ISO3_df, on='ISO2 Code', how='inner')
    # df.head()


def add_population_density(df):
    """Joins population density from 2018"""
    db = DataBase('COVID-19.db')
    population_df = db.load_population_density_df()

    merged_df = df.merge(population_df[['Country Code', '2018']],
                         how='left',
                         left_on=['ISO3 Code'],
                         right_on=['Country Code'])
    merged_df['pop_density_per_sq_km'] = merged_df['2018']
    merged_df = merged_df.drop(columns=['Country Code', '2018'])

    return merged_df


def add_country_population(df):
    """Joins population density from 2018"""
    db = DataBase('COVID-19.db')
    population_df = db.load_population_df()

    merged_df = df.merge(population_df[['Country Code', '2018']],
                         how='left',
                         left_on=['ISO3 Code'],
                         right_on=['Country Code'])
    merged_df['population'] = merged_df['2018']
    merged_df = merged_df.drop(columns=['Country Code', '2018'])

    return merged_df


def add_google_mobility_data(df):
    """Join Google mobility data"""
    # db = DataBase('COVID-19.db')
    # google_df = db.pull_google_mobility_data()
    # link = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
    link = Path.cwd() / 'data/Global_Mobility_Report.csv'
    google_df = pd.read_csv(link)
    google_df['date'] = pd.to_datetime(google_df['date'])
    merged_df = df.merge(google_df,
                         how='left',
                         left_on=['ISO2 Code', 'date'],
                         right_on=['country_region_code', 'date'])
    return merged_df

# TODO: Rolling average


def rolling_mean(df, num_days):
    """
    Window average on response.  Smooths variations due to problems with 
    reporting. 

    df: a pandas series for the response
    return: 
    """
    n = num_days - 1
    response = df.to_numpy()
    avg_response = response.copy()
    for i in range(1, len(response)):
        if i <= num_days:
            print(f'i = {i}')
            print(f'n = {n}')
            print(f'num_days = {num_days}')
            print(f'num_days-n = {num_days - n}')
            avg_response[i] = round(response[0:num_days-n].mean())
            print(f'avg = {avg_response[i]}')
            print()
            n -= 1
        else:
            print(f'i = {i}')
            print(f'i-num_days = {i-num_days}')
            print(f'response[i-n:i] = response[i-num_days:i]')
            avg_response[i] = round(response[i-num_days:i].mean())
            print(f'avg = {avg_response[i]}')
            print()

    return pd.Series(avg_response)
