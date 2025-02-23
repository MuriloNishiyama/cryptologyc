from web3 import Web3
from .blockchain_provider import BlockchainProvider

class EthereumProvider(BlockchainProvider):
    def __init__(self, api_key: str):
        self.web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{api_key}'))
        self.last_parsed_block = 0

    def get_last_block(self):
        self.last_parsed_block = self.web3.eth.get_block_number()
        return self.last_parsed_block