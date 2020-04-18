import sqlite3
import pandas as pd
from sqlite3 import Error
from pathlib import Path

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
class DataBase():
    def __init__(self, db_name):
        self.db_name = db_name
        self.data_dir = Path.cwd() / 'data'
        self.db_path = self.data_dir / self.db_name
        self.connection = self.connect()


    def connect(self):
        """Connects to SQLite DB"""
        connection = None
        try:
            if not Path(self.data_dir).is_dir():
                self.data_dir.mkdir(parents=True, exist_ok=True)

            connection = sqlite3.connect(self.db_path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection


    def pull_data(self, url, name, csv=False):
        """
        Pull data from John Hopkins github and store in DB (currently a csv)
        """
        df = pd.read_csv(url)
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
        Saves the data (to csv) in the data directory (creates directory if doesn't exit)
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
        except OperationalError as e:
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


    def read_table_to_dataframe(self, table_name):
        return pd.read_sql_query("SELECT * FROM " + table_name, self.connection)


    def list_tables(self):
        cursor = self.connection.cursor()
        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        cursor.execute("SELECT * FROM sqlite_master")
        tables = cursor.fetchall()
        tables = [x[2] for x in tables]
        print(f"> Tables in {self.db_name}: {tables}")


def main():
    # Should set these url paths as environment variables
    CONFIRMED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    RECOVERED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    # db = DataBase('database.sqlite3')
    db = DataBase('COVID-19.db')
    db.pull_data(url=CONFIRMED, name='jh_confirmed', csv=True)
    db.pull_data(url=DEATHS, name='jh_deaths', csv=True)
    db.pull_data(url=RECOVERED, name='jh_recovered', csv=True)

    db.list_tables()
    df = db.read_table_to_dataframe('jh_deaths')
    print(df.head())


if __name__ == '__main__':
    main()