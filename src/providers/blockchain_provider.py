from abc import ABC, abstractmethod

class BlockchainProvider(ABC):
    @property
    @abstractmethod
    def currency(self) -> str:
        """The currency code"""
        pass

    @abstractmethod
    def get_last_block(self):
        """Returns the last block number"""
        pass

    @abstractmethod
    def parse_block(self, block):
        """Returns the block information"""
        pass

    @abstractmethod
    def wei_to_currency(self, value):
        """Transforms wei to specific currency"""
        pass