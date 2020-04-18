import sqlite3
from sqlite3 import Error
from pathlib import Path

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DATA_DIR = Path.cwd() / 'data'
DEFAULT_PATH = DATA_DIR / 'database.sqlite3'

def pull_data():
    """
    Pull data from John Hopkins github and store in DB (currently a csv)
    """

    # Should set these url paths as environment variables
    CONFIRMED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    RECOVERED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    confirmed_df = pd.read_csv(CONFIRMED)
    deaths_df = pd.read_csv(DEATHS)
    recovered_df = pd.read_csv(RECOVERED)

    save_data(confirmed_df, DATA_DIR, "confirmed_jh.csv")
    save_data(deaths_df, DATA_DIR, "deaths_jh.csv")
    save_data(recovered_df, DATA_DIR, "recovered_jh.csv")


def save_data(df, data_dir, filename):
    """
    Saves the data (to csv) in the data directory (creates directory if doesn't exit)
        - Need to change to actual DB
    :param data_dir: data directory
    :param filename: name of saved file
    """
    if not Path(data_dir).is_dir():
        data_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_dir / filename)


def db_connect(db_path=DEFAULT_PATH):
    data_dir = db_path.parent
    connection = None

    print(data_dir)
    try:
        if not Path(data_dir).is_dir():
            data_dir.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(db_path)
        print("Connection to SQLite DB successful")

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def main():
    pull_data()
    db_connect()

if __name__ == '__main__':
    main()