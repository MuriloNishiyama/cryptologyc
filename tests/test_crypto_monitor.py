import unittest
import pandas as pd
from src.crypto_monitor import CryptoMonitor

class DummyProvider:
    def __init__(self, currency="dummy"):
        self.currency = currency
        self.last_parsed_block = 0

    def get_last_block(self):
        return 5

    def parse_block(self, block):
        return {"transactions": [{"value": 100, "id": block}]}

    def wei_to_currency(self, value):
        return value / 1e18

class DummyDatabase:
    def __init__(self):
        self.tables = {}
    def append_df(self, table_name, df_pd):
        self.tables[table_name] = df_pd

class TestCryptoMonitor(unittest.TestCase):
    def setUp(self):
        self.dummy_provider = DummyProvider()
        self.dummy_database = DummyDatabase()
        self.monitor = CryptoMonitor(providers={"dummy": self.dummy_provider}, database=self.dummy_database)

    def test_get_last_block(self):
        last_block = self.monitor.get_last_block(self.dummy_provider)
        self.assertEqual(last_block, 5)

    def test_parse_block(self):
        block_data = self.monitor.parse_block(self.dummy_provider, 3)
        self.assertIn("transactions", block_data)
        self.assertEqual(block_data["transactions"][0]["id"], 3)

    def test_reset_transactions(self):
        self.monitor.transactions[self.dummy_provider] = [{"value": 100}]
        self.monitor.reset_transactions()
        self.assertEqual(self.monitor.transactions[self.dummy_provider], [])

    def test_get_transactions_dataframe(self):
        self.monitor.transactions[self.dummy_provider] = [{"value": 100, "id": 1}]
        df = self.monitor.get_transactions_dataframe()
        self.assertIn("currency", df.columns)
        self.assertIn("wei_value", df.columns)
        self.assertIn("value", df.columns)
        self.assertEqual(len(df), 1)

    def test_save_data_to_database(self):
        self.monitor.transactions[self.dummy_provider] = [{"value": 100, "id": 1}]
        self.monitor.save_data_to_database()
        self.assertIn("transactions", self.dummy_database.tables)
        df_saved = self.dummy_database.tables["transactions"]
        self.assertEqual(len(df_saved), 1)
        self.assertEqual(self.monitor.transactions[self.dummy_provider], [])

if __name__ == '__main__':
    unittest.main()
