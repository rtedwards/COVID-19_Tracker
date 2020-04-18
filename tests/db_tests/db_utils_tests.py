import unittest
import coronavirus.db_utils.db_utils as dbu 
from pathlib import Path

class TestDBUtils(unittest.TestCase):
    def setUp(self):
        """
        Creates paths and stores them in the test case as self objects.
        """
        self.data_dir = Path.cwd() / 'tests/db_tests'
        self.db_path = self.data_dir / 'database.sqlite3'
        
        # self.pol_df = tu.build_test_pol_dataframe()
        # self.observation_df = tu.build_test_observation_dataframe()

    def tearDown(self):
        pass

    def test_db_connect(self): 
        """
        Connects to the SQLite DB and tests:
            - the data directory is created
            - the sqlite db file is created
            - the sqlite.Connection is returned
        """
        connection = dbu.db_connect(db_path=self.db_path)

        self.assertTrue(self.data_dir.is_dir())
        self.assertTrue(self.db_path.is_file())
        self.assertTrue(type(connection == 'sqlite3.Connection'))
        

if __name__ == '__main__':
    unittest.main()
