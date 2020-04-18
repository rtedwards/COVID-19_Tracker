import unittest
import coronavirus.db_utils.db_utils as dbu 
from pathlib import Path

class TestDBUtils(unittest.TestCase):
    def setUp(self):
        """
        Creates paths and stores them in the test case as self objects.
        """
        self.data_dir = Path.cwd() / 'tests/db_tests/data'
        self.db_path = self.data_dir / 'database.sqlite3'
        self.connection = dbu.db_connect(db_path=self.db_path)
        
        # self.pol_df = tu.build_test_pol_dataframe()
        # self.observation_df = tu.build_test_observation_dataframe()

    def tearDown(self):
        """Removes database file and data directory"""
        self.db_path.unlink()
        self.data_dir.rmdir()

    def test_db_connect(self): 
        """
        Connects to the SQLite DB and tests:
            - the data directory is created
            - the sqlite db file is created
            - the sqlite.Connection is returned
        """
        self.assertTrue(self.data_dir.is_dir())
        self.assertTrue(self.db_path.is_file())
        self.assertTrue(type(self.connection == 'sqlite3.Connection'))
        

if __name__ == '__main__':
    unittest.main()
