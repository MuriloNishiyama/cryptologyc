import unittest
from src.crypto_monitor import CryptoMonitor
import pandas as pd

class DummyProvider:
    def __init__(self, network="dummy", last_parsed_block=0, last_block_value=5):
        self.network = network
        self.last_parsed_block = last_parsed_block
        self.last_block_value = last_block_value

    def get_last_block(self):
        return self.last_block_value

    def parse_block(self, block):
        return {"transactions": [{"id": block}]}

    def wei_to_network(self, value):
        return value

class DummyDatabase:
    def __init__(self, last_block_db=None):
        self.last_block_db = last_block_db

    def get_last_block(self, network):
        return self.last_block_db

    def append_df(self, table_name, df_pd):
        pass

class TestParseAllBlocks(unittest.TestCase):
    def setUp(self):
        self.db_none = DummyDatabase(last_block_db=None)
        self.db_zero = DummyDatabase(last_block_db=0)
        self.provider_default = DummyProvider(network="dummy", last_parsed_block=0, last_block_value=5)

    def test_parse_all_blocks_db_none(self):
        monitor = CryptoMonitor(providers={"dummy": self.provider_default}, database=self.db_none)
        monitor.parse_all_blocks(try_to_recover_from_db=True)
        transactions = monitor.transactions[self.provider_default]
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["id"], 5)

    def test_parse_all_blocks_db_zero(self):
        monitor = CryptoMonitor(providers={"dummy": self.provider_default}, database=self.db_zero)
        monitor.parse_all_blocks(try_to_recover_from_db=True)
        transactions = monitor.transactions[self.provider_default]
        self.assertEqual(len(transactions), 0)

    def test_parse_all_blocks_no_recover(self):
        monitor = CryptoMonitor(providers={"dummy": self.provider_default}, database=self.db_zero)
        monitor.parse_all_blocks(try_to_recover_from_db=False)
        transactions = monitor.transactions[self.provider_default]
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["id"], 5)

    def test_parse_all_blocks_provider_non_zero(self):
        provider_non_zero = DummyProvider(network="dummy", last_parsed_block=3, last_block_value=5)
        monitor = CryptoMonitor(providers={"dummy": provider_non_zero}, database=self.db_none)
        monitor.parse_all_blocks(try_to_recover_from_db=True)
        transactions = monitor.transactions[provider_non_zero]
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0]["id"], 3)
        self.assertEqual(transactions[-1]["id"], 5)

if __name__ == '__main__':
    unittest.main()
