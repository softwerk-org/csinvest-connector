from connector.base import Connector
from connector.csmoney.models.get_min_prices import MarketPriceItem, MinPrices


class CSMoneyConnector(Connector):
    """Connector for CS.Money public endpoints.

    No official documentation URL is available.
    """

    def __init__(self, proxy: str | None = None):
        super().__init__(base_url="https://cs.money", proxy=proxy)

    async def get_min_prices(self) -> dict[str, MarketPriceItem]:
        """Get minimum prices for all markets (updates every 10 minutes)."""
        text = await self._get("/api/min_price/market/all")
        min_prices = MinPrices.model_validate_json(text)
        return min_prices.root
