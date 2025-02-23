from abc import ABC, abstractmethod

class BlockchainProvider(ABC):
    @abstractmethod
    def get_last_block(self):
        """Returns the last block number"""
        pass