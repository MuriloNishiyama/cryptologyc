import os
import tempfile
import duckdb
import pandas as pd
import unittest
from src.db.duckdb_database import DuckDBDatabase

class TestDuckDBDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)
        self.database = DuckDBDatabase(self.temp_db_path)
        self.sample_dataframe = pd.DataFrame({'number': [1, 2], 'letter': ['a', 'b']})
        self.table_name = "test_table"

    def test_append_df_creates_table(self):
        self.database.append_df(self.table_name, self.sample_dataframe)
        connection = duckdb.connect(self.temp_db_path)
        result_dataframe = connection.sql(f"SELECT * FROM {self.table_name}").df()
        connection.close()
        self.assertEqual(len(result_dataframe), len(self.sample_dataframe))
        self.assertListEqual(list(result_dataframe.columns), list(self.sample_dataframe.columns))

    def test_append_df_inserts_additional_rows(self):
        self.database.append_df(self.table_name, self.sample_dataframe)
        self.database.append_df(self.table_name, self.sample_dataframe)
        connection = duckdb.connect(self.temp_db_path)
        result_dataframe = connection.sql(f"SELECT * FROM {self.table_name}").df()
        connection.close()
        self.assertEqual(len(result_dataframe), 2 * len(self.sample_dataframe))

if __name__ == '__main__':
    unittest.main()
