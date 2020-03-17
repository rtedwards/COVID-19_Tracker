import pandas as pd
import geopandas as gpd
import joblib
import json
import folium
import urllib
import os

def load_data(type=time_series): 

    if type == time_series:
        TIME_DATA_DIR = '/Users/Berto/Projects/COVID-19_Tracker/COVID-19/csse_covid_19_data/csse_covid_19_time_series'
        
        CONFIRMED = os.path.join(TIME_DATA_DIR, "time_series_19-covid-Confirmed.csv")
        DEATHS = os.path.join(TIME_DATA_DIR, "time_series_19-covid-Deaths.csv")
        RECOVERED = os.path.join(TIME_DATA_DIR, "time_series_19-covid-Recovered.csv")

        confirmed_df = pd.read_csv(CONFIRMED)
        deaths_df = pd.read_csv(DEATHS)
        recovered_df = pd.read_csv(RECOVERED)

        # Convert from Wide to Long format
        confirmed_df = confirmed_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                         var_name='date', 
                                         value_name='confirmed')
        deaths_df = deaths_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                   var_name='date', 
                                   value_name='deaths')
        recovered_df = recovered_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                         var_name='date', 
                                         value_name='recovered')
        # Merge data frames
        df = pd.merge(confirmed_df, deaths_df, 
                      on=['Province/State', 'Country/Region', 'Lat', 'Long', 'date'],
                      how='inner')
        df = pd.merge(df, recovered_df, 
                      on=['Province/State', 'Country/Region', 'Lat', 'Long', 'date'],
                      how='inner')

        # Convert to datetime
        df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y")

        return df

    elif type == daily:
        DAILY_DATA_DIR = '/Users/Berto/Projects/COVID-19_Tracker/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports'

        date_list = os.listdir(DAILY_DATA_DIR)
        date_list.remove('.gitignore')
        date_list.remove('README.md')
        date_list.sort()

    else:
        print("TypeError")



