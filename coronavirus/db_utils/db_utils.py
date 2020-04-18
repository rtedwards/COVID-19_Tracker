import sqlite3
from sqlite3 import Error
from pathlib import Path

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DATA_DIR = Path.cwd() / 'data'
DEFAULT_PATH = DATA_DIR / 'database.sqlite3'

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
    db_connect()

if __name__ == '__main__':
    main()