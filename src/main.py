import os
from providers.ethereum_provider import EthereumProvider
from crypto_monitor import CryptoMonitor
from db.database_builder import DatabaseBuilder

def main():
    infura_api_key = os.environ.get("INFURA_API_KEY")
    if not infura_api_key:
        raise EnvironmentError("INFURA_API_KEY must be set.")

    providers = {
        "eth": EthereumProvider(infura_api_key)
    }
    database = DatabaseBuilder() \
                .database_type("duckdb") \
                .build()
    monitor = CryptoMonitor(providers = providers, database = database)
    

    monitor.parse_all_blocks()
    monitor.save_data_to_database()


if __name__ == '__main__':
    main()
