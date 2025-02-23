import pandas as pd
from .logger import logger

class CryptoMonitor:
    def __init__(self, providers: dict, database):
        self.providers = providers
        self.database = database
        self.transactions = {provider : [] for provider in list(self.providers.values())}

    def reset_transactions(self):
        logger.debug("Cleaning transaction property...")
        self.transactions = {provider : [] for provider in list(self.providers.values())}

    def get_last_block(self, provider):
        return provider.get_last_block()
    
    def parse_block(self, provider, block):
        return provider.parse_block(block)
    
    def __get_last_block_from_db(self, currency):
        return self.database.get_last_block(currency=currency)

    def parse_all_blocks(self, try_to_recover_from_db : bool = True):
        for currency, provider in self.providers.items():
            logger.info(f"Capturing {currency} data...")
            if provider.last_parsed_block == 0:
                if try_to_recover_from_db:
                    initial_block = self.__get_last_block_from_db(currency = currency)
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
            for i in range(initial_block, last_block + 1,1):
                self.transactions[provider] += self.parse_block(provider=provider, block = i).get("transactions")

    def get_transactions_dataframe(self):
        data = []
        logger.info("Turning data into dataframe...")
        for provider, transactions in self.transactions.items():
            for transaction in transactions:
                transaction_aux = dict(transaction)
                transaction_aux["currency"] = provider.currency
                transaction_aux["wei_value"] = transaction_aux["value"] 
                transaction_aux["value"] = provider.wei_to_currency(value = transaction_aux["wei_value"])
                data.append(transaction_aux)
        return pd.DataFrame(data)
    
    def save_data_to_database(self):
        logger.info("Saving all data into database...")
        df_transactions = self.get_transactions_dataframe()
        self.database.append_df(table_name = "transactions", df_pd = df_transactions)
        logger.debug(f"Saved {len(df_transactions.index)} transactions.")
        self.reset_transactions()