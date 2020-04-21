import pandas as pd
import geopandas as gpd
import joblib
import json
import folium
import urllib
import os

def convert_jh_global_time_series_to_long(df, name): 
    """Converts JH global time series data from wide to long format"""
    df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                 var_name='date', 
                 value_name=name)

    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y").dt.normalize()

    # Rename columns
    df.columns = ['province/state', 'country/region', 'latitude', 'longitude', 'date', name]
    return df


def merge_dataframes(df1, df2, df3=None):
    """Merges JH global time series dataframes"""
    merged_df = pd.merge(df1, df1, 
                    on=['Province/State', 'Country/Region', 'Lat', 'Long', 'date'],
                    how='inner')
    
    if df3:
        merged_df = pd.merge(merged_df, df3, 
                    on=['Province/State', 'Country/Region', 'Lat', 'Long', 'date'],
                    how='inner')

    return merged_df


# Calculate Incidence, Prevalence, Morbidity, Mortality
# https://www.health.ny.gov/diseases/chronic/basicstat.htm


# Join Political Leanings
# https://www.cpds-data.org/

# Freedom Index
# https://rsf.org/en/ranking_table
# https://www.cato.org/sites/cato.org/files/human-freedom-index-files/human-freedom-index-2019.pdf
#   - https://www.reddit.com/r/IntellectualDarkWeb/comments/b07on4/political_compass_of_countries_data_from_the/