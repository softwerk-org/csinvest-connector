from connector.base import Connector
from connector.csmoney.models.get_min_prices import MarketPriceItem, MinPrices


class CSMoneyConnector:
    __docs__ = ""

    def __init__(self, proxy: str | None = None):
        self.connector = Connector(base_url="https://cs.money", proxy=proxy)

    async def get_min_prices(self) -> dict[str, MarketPriceItem]:
        """Get minimum prices for all markets (updates every 10 minutes)."""
        text = await self.connector.get("/api/min_price/market/all")
        min_prices = MinPrices.model_validate_json(text)
        return min_prices.root
