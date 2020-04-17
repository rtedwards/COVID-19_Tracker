import pandas as pd 
from pathlib import Path

def pull_data():
    """
    Pull data from John Hopkins github and store in DB (currently a csv)
    """
    DATA_DIR = Path.cwd() / 'data'

    # Should set these url paths as environment variables
    CONFIRMED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    RECOVERED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    confirmed_df = pd.read_csv(CONFIRMED)
    deaths_df = pd.read_csv(DEATHS)
    recovered_df = pd.read_csv(RECOVERED)

    # Need to change to actual DB
    confirmed_df.to_csv(DATA_DIR / "confirmed_jh.csv")
    deaths_df.to_csv(DATA_DIR / "deaths_jh.csv")
    recovered_df.to_csv(DATA_DIR / "recovered_jh.csv")

def main():
    pull_data()

if __name__ == "__main__":
    main()