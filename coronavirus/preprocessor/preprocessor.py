import pandas as pd


def convert_jh_global_time_series_to_long(df, name):
    """Converts JH global time series data from wide to long format"""
    df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                 var_name='date',
                 value_name=name)

    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y").dt.normalize()

    # Rename columns
    df.columns = ['province/state', 'country/region',
                  'latitude', 'longitude', 'date', name]
    return df


def merge_dataframes(df1, df2, df3=None):
    """Merges JH global time series dataframes"""
    merged_df = pd.merge(df1, df1,
                         on=['Province/State', 'Country/Region',
                             'Lat', 'Long', 'date'],
                         how='inner')

    if df3:
        merged_df = pd.merge(merged_df, df3,
                             on=['Province/State', 'Country/Region',
                                 'Lat', 'Long', 'date'],
                             how='inner')

    return merged_df


def consolidate_country_regions(df):
    """Selects the rows with overall country stats and drops region column"""
    rtn_df = (df.loc[df['province/state'].isnull()]
              .drop(columns=['province/state']))
    return rtn_df


def get_top_n_countries(df, n, response):
    """
    Returns a list of the top countries by response
        :param df: pandas dataframe
        :param n {int}: number of countries to select
        :param response {string}: deaths, confirmed, or recovered
    """
    top_df = df.loc[df['date'] == df['date'].max()]
    top_df = top_df.sort_values(by=[response], ascending=False)

    return list(top_df['country/region'].iloc[0:n])

def clean_country_names(df):
    """
    Given a dataframe with only 1 column 'country/region'
    cleans country names
    """
    cleaned_df = df.replace({'country/region':
                                {'US': 'United States',
                                'Taiwan*': 'Taiwan',
                                'Korea, South': 'South Korea'}
                            })
    return cleaned_df

# Calculate Incidence, Prevalence, Morbidity, Mortality
# https://www.health.ny.gov/diseases/chronic/basicstat.htm


# Join Political Leanings
# https://www.cpds-data.org/

# Freedom Index
# https://rsf.org/en/ranking_table
# https://www.cato.org/sites/cato.org/files/human-freedom-index-files/human-freedom-index-2019.pdf
#   - https://www.reddit.com/r/IntellectualDarkWeb/comments/b07on4/political_compass_of_countries_data_from_the/

# Air Pollutions
# https://projects.iq.harvard.edu/files/covid-pm/files/pm_and_covid_mortality.pdf
# https://ourworldindata.org/air-pollution
# https://ourworldindata.org/outdoor-air-pollution
# https://ourworldindata.org/indoor-air-pollution
#  - https://github.com/owid/covid-19-data/tree/master/public/data
