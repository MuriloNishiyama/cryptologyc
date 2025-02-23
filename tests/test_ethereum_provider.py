# tests/test_ethereum_provider.py
import unittest
from unittest.mock import MagicMock, patch
from src.providers.ethereum_provider import EthereumProvider
from src.logger import logger
class TestEthereumProvider(unittest.TestCase):
    @patch("src.providers.ethereum_provider.Web3")
    def test_get_last_block(self, mock_web3):
        mock_instance = MagicMock()
        mock_instance.eth.get_block_number.return_value = 12345678
        mock_web3.HTTPProvider.return_value = "provider_instance"
        mock_web3.return_value = mock_instance

        api_key = "dummy_api_key"
        provider = EthereumProvider(api_key)
        last_block = provider.get_last_block()

        self.assertEqual(last_block, 12345678)
        mock_instance.eth.get_block_number.assert_called_once()

if __name__ == '__main__':
    unittest.main()
