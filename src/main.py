import os
from providers.ethereum_provider import EthereumProvider
from crypto_monitor import CryptoMonitor

def main():
    infura_api_key = os.environ.get("INFURA_API_KEY")
    if not infura_api_key:
        raise EnvironmentError("INFURA_API_KEY must be set.")

    providers = {
        "eth": EthereumProvider(infura_api_key)
    }

    monitor = CryptoMonitor(providers)
    last_block = monitor.get_last_block("eth")
    print("Last Ethereum block:", last_block)

if __name__ == '__main__':
    main()
