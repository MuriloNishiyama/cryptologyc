import pandas as pd
from .logger import logger

class CryptoMonitor:
    def __init__(self, providers: dict, database):
        self.providers = providers
        self.database = database
        self.transactions = {provider : [] for provider in list(self.providers.values())}
        self.blocks = {provider : [] for provider in list(self.providers.values())}

    def reset_variables(self):
        logger.debug("Cleaning transaction property...")
        self.transactions = {provider : [] for provider in list(self.providers.values())}
        self.blocks = {provider : [] for provider in list(self.providers.values())}

    def get_last_block(self, provider):
        return provider.get_last_block()
    
    def parse_block(self, provider, block):
        return provider.parse_block(block)
    
    def __get_last_block_from_db(self, network):
        return self.database.get_last_block(network=network)

    def parse_all_blocks(self, try_to_recover_from_db : bool = True):
        for currency, provider in self.providers.items():
            logger.info(f"Capturing {currency} data...")
            if provider.last_parsed_block == 0:
                if try_to_recover_from_db:
                    initial_block = self.__get_last_block_from_db(network = provider.network)
                    logger.debug(initial_block)
                    if initial_block is None:
                        initial_block = self.get_last_block(provider)
                        last_block = initial_block
                    elif initial_block == provider.last_parsed_block:
                        logger.info(f"No operations since last iteration. Block = {provider.last_parsed_block}")
                        continue
                    else:
                        last_block = self.get_last_block(provider)
                else:
                    initial_block = self.get_last_block(provider)
                    last_block = initial_block
            else:
                initial_block = provider.last_parsed_block
                last_block = self.get_last_block(provider)
                if initial_block == last_block:
                    logger.info(f"No operations since last iteration. Block = {provider.last_parsed_block}")
                    continue
            for block_number in range(initial_block, last_block + 1):
                block_data = provider.parse_block(block=block_number)
                block_dict = dict(block_data)
                transactions = block_dict.get("transactions", [])
                new_transactions = []
                for tx in transactions:
                    tx_dict = dict(tx)
                    tx_dict["block_id"] = block_number
                    new_transactions.append(tx_dict)
                self.transactions[provider] += new_transactions
                block_metadata = dict(block_dict)
                block_metadata.pop("transactions", None)
                block_metadata["block_id"] = block_number
                self.blocks[provider].append(block_metadata)

    def get_transactions_dataframe(self):
        data = {provider : [] for provider in list(self.providers.values())}
        logger.info("Turning transactions data into dataframe...")
        for provider, transactions in self.transactions.items():
            for transaction in transactions:
                transaction_aux = dict(transaction)
                transaction_aux["wei_value"] = transaction_aux["value"] 
                transaction_aux["value"] = provider.wei_to_currency(value = transaction_aux["wei_value"])
                data[provider].append(transaction_aux)
        return {provider : pd.DataFrame(data[provider]) for provider in list(self.providers.values())}
    
    def get_block_dataframe(self):
        data = {provider : [] for provider in list(self.providers.values())}
        logger.info("Turning transactions data into dataframe...")
        for provider, blocks in self.blocks.items():
            for block in blocks:
                data[provider].append(dict(block))
        return {provider : pd.DataFrame(data[provider]) for provider in list(self.providers.values())}
    
    def save_data_to_database(self):
        logger.info("Saving all data into database...")
        dfs_transactions = self.get_transactions_dataframe()
        for provider, df_transactions in dfs_transactions.items():
            self.database.append_df(table_name = f"{provider.network}_transactions", df_pd = df_transactions)
            logger.debug(f"Saved {len(df_transactions.index)} transactions.")

        dfs_blocks = self.get_block_dataframe()
        for provider, df_blocks in dfs_blocks.items():
            self.database.append_df(table_name = f"{provider.network}_blocks", df_pd = df_blocks)
            logger.debug(f"Saved {len(df_blocks.index)} blocks.")

        self.reset_variables()
