import sqlite3
import pandas as pd
from sqlite3 import Error
from pathlib import Path
from coronavirus.preprocessor.preprocessor import (
    convert_jh_global_time_series_to_long)


# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
class DataBase():
    def __init__(self, db_name):
        self.db_name = db_name
        self.data_dir = Path.cwd() / 'data'
        self.db_path = self.data_dir / self.db_name
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        """Connects to SQLite DB"""
        connection = None
        try:
            if not Path(self.data_dir).is_dir():
                self.data_dir.mkdir(parents=True, exist_ok=True)

            print(f"Connecting to {self.db_path}")
            connection = sqlite3.connect(self.db_path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def pull_mobility_data(self):
        """
        Pulls mobility data from Google and Apple.  Needs to be updated daily
        Google:
            - CSV: https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv
        Apple: https://www.apple.com/covid19/mobility
            - CSV: https://covid19-static.cdn-apple.com/covid19-mobility-data/2006HotfixDev7/v1/en-us/applemobilitytrends-2020-04-16.csv
        """
        # pull_google_mobility_data()
        # pull_apple_mobility_data()
        pass

    def pull_world_bank_data(self):
        """Pulls population data from World Bank
            - api.worldbank.org/v2/en/indicator/EN.POP.DNST?downloadformat=csv
        """

    def pull_data(self, url, name, csv=False):
        """
        Pull data from John Hopkins github and store in DB (currently a csv)
            - Converts time series to long format before saving
        """
        df = pd.read_csv(url)
        df = convert_jh_global_time_series_to_long(df, name.split('_')[2])

        self.save_to_db(df, name)

        if csv:
            self.save_to_csv(df, name + ".csv")

    def save_to_db(self, df, table_name):
        """
        Saves the data to a table in the DB
        :param df: pandas dataframe
        :param table_name: name of table to save data

        ** Need to check / drop duplicates **
        """
        df.to_sql(table_name, self.connection, if_exists='append', index=False)
        print(f"> Inserted {table_name} into {self.db_name}")

    def save_to_csv(self, df, file_name):
        """
        Saves the data (to csv) in the data directory
        (creates directory if doesn't exit)
            - Need to change to actual DB
        :param df: pandas dataframe
        :param table_name: name of saved file
        """
        if not Path(self.data_dir).is_dir():
            self.data_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.data_dir / file_name)

    def execute_query(self, query):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query executed successfully")
        except self.OperationalError as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def read_table_to_dataframe(self, table_name, response):
        df = pd.read_sql_query("SELECT * FROM " + table_name, self.connection)
        df = df.drop(columns=['latitude', 'longitude'])
        df = df.reindex(columns=['province/state', 'country/region',
                                 response, 'date'])
        df = df.sort_values(by=['date'], ascending=False)
        df['date'] = pd.to_datetime(df['date']).dt.normalize()

        # TODO: add response rate
        # TODO: add population density
        # TODO: add reponse / population density
        return df.drop_duplicates()

    def list_tables(self):

        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.cursor.execute("SELECT * FROM sqlite_master")
        tables = self.cursor.fetchall()
        tables = [x[2] for x in tables]
        print(f"> Tables in {self.db_name}: {tables}")

        return tables

    def load_jh_world_df(self):
        """Loads and joins confirmed, deaths, and recovered tables from DB"""

        confirmed_df = self.read_table_to_dataframe('jh_global_confirmed')
        deaths_df = self.read_table_to_dataframe('jh_global_deaths')
        recovered_df = self.read_table_to_dataframe('jh_global_recovered')
        print(confirmed_df.shape)
        print(deaths_df.shape)
        print(recovered_df.shape)

        merged_df = pd.merge(confirmed_df, deaths_df,
                             on=['province/state', 'country/region', 'date'],
                             how='left')
        # merged_df = pd.merge(merged_df, recovered_df,
        #                 on=['province/state', 'country/region', 'date'],
        #                 how='left')
        return merged_df


def main():
    # Should set these url paths as environment variables
    CONFIRMED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    RECOVERED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    # db = DataBase('database.sqlite3')
    db = DataBase('COVID-19.db')
    db.pull_data(url=CONFIRMED, name='jh_global_confirmed', csv=True)
    db.pull_data(url=DEATHS, name='jh_global_deaths', csv=True)
    db.pull_data(url=RECOVERED, name='jh_global_recovered', csv=True)

    # Summary Statistics
    tables = db.list_tables()
    for table in tables:
        db.cursor.execute("SELECT count(*) FROM " + table)
        length = db.cursor.fetchall()

        print(f"{table}.length(): {length[0][0]}")

    df = db.read_table_to_dataframe('jh_global_deaths')
    print(df.tail(20))


if __name__ == '__main__':
    main()
