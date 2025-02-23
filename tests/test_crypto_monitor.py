# tests/test_crypto_monitor.py
import unittest
from src.crypto_monitor import CryptoMonitor

class DummyProvider:
    def get_last_block(self):
        return 999

class TestCryptoMonitor(unittest.TestCase):
    def setUp(self):
        self.providers = {"dummy": DummyProvider()}
        self.monitor = CryptoMonitor(self.providers)

    def test_get_last_block_valid_currency(self):
        self.assertEqual(self.monitor.get_last_block("dummy"), 999)

    def test_get_last_block_invalid_currency(self):
        with self.assertRaises(ValueError):
            self.monitor.get_last_block("invalida")

if __name__ == '__main__':
    unittest.main()
