from abc import ABC, abstractmethod

class BaseDatabase(ABC):
    @abstractmethod
    def append_df(self, table_name : str, df_pd):
        """Append the data inside database. If the table doesnt exist, it will be created."""
        pass

    @abstractmethod
    def get_last_block(self, currency : str):
        """Returns the last block from currency saved on database"""
        pass