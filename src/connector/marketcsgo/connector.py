from typing import Literal
import os

from connector.base import Connector
from .models.get_prices import Prices
from .models.get_list_items_info import ListItemsInfo


class MarketCsgoConnector:
    __docs__ = "https://market.csgo.com/en/api"

    def __init__(self, api_key: str | None = None, proxy: str | None = None):
        self.connector = Connector(
            base_url="https://market.csgo.com/api",
            proxy=proxy,
        )
        self.api_key = api_key

    async def get_prices(
        self, currency: Literal["RUB", "EUR", "USD"] = "USD"
    ) -> Prices:
        """Get market prices."""
        text = await self.connector.get(
            f"/v2/prices/{currency}.json",
        )
        return Prices.model_validate_json(text)

    async def get_list_items_info(self, market_hash_names: list[str]) -> ListItemsInfo:
        """Get list items info."""
        params = {"list_hash_name[]": market_hash_names}
        text = await self.connector.get(
            "/v2/get-list-items-info",
            params=params,
        )
        return ListItemsInfo.model_validate_json(text)
