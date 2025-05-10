from typing import Literal

from connector.base import ConnectorBase
from .models.get_prices import GetPrices

class MarketCsgoConnector:
    __docs__ = "https://market.csgo.com/docs-v2"

    def __init__(self, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://market.csgo.com/api/v2", proxy_url=proxy_url)

    async def get_prices(
        self, currency: Literal["RUB", "EUR", "USD"] = "USD"
    ) -> GetPrices:
        """Get market prices."""
        text = await self.connector.request(
            "GET",
            f"/prices/{currency}.json",
        )
        return GetPrices.model_validate_json(text)