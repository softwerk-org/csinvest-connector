from connector.base import Connector
from connector.csmoney.models.get_min_prices import MinPrices


class CSMoneyConnector:
    __docs__ = ""

    def __init__(self, proxy: str | None = None):
        self.connector = Connector(base_url="https://cs.money", proxy=proxy)

    async def get_min_prices(self) -> MinPrices:
        """Get minimum prices for all markets (updates every 10 minutes)."""
        text = await self.connector.get("/api/min_price/market/all")
        return MinPrices.model_validate_json(text)
