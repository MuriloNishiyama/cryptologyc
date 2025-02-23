import os
import tempfile
import duckdb
import unittest
from src.db.duckdb_database import DuckDBDatabase

class TestGetLastBlock(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)
        self.database = DuckDBDatabase(self.temp_db_path)
        with duckdb.connect(self.temp_db_path) as connection:
            connection.execute("""
                CREATE TABLE transactions (
                    blockNumber INTEGER,
                    currency VARCHAR
                )
            """)
            connection.execute("""
                INSERT INTO transactions VALUES (100, 'eth'), (200, 'eth'), (150, 'btc')
            """)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_get_last_block_existing_currency(self):
        lastBlockETH = self.database.get_last_block('eth')
        lastBlockBTC = self.database.get_last_block('btc')
        self.assertEqual(lastBlockETH, 200)
        self.assertEqual(lastBlockBTC, 150)

    def test_get_last_block_nonexistent_currency(self):
        lastBlockLTC = self.database.get_last_block('ltc')
        self.assertIsNone(lastBlockLTC)

    def test_get_last_block_no_transactions_table(self):
        with duckdb.connect(self.temp_db_path) as connection:
            connection.execute("DROP TABLE transactions")
        lastBlockETH = self.database.get_last_block('eth')
        self.assertIsNone(lastBlockETH)

if __name__ == '__main__':
    unittest.main()
