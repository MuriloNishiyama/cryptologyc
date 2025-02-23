class CryptoMonitor:
    def __init__(self, providers: dict):
        self.providers = providers

    def get_last_block(self, currency: str):
        provider = self.providers.get(currency)
        if provider is None:
            raise ValueError(f"Currency '{currency}' not supported.")
        return provider.get_last_block()