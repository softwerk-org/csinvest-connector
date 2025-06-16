from typing import Literal

from fake_useragent import UserAgent
from connector.base import Connector
from connector.marketcsgo.models.get_history import HistoryResponse
from connector.marketcsgo.models.get_prices import Prices
from connector.marketcsgo.models.get_list_items_info import ListItemsInfo


class MarketCsgoConnector(Connector):
    """Connector for the Market.CSGO API.

    Documentation: https://market.csgo.com/en/api
    """

    def __init__(
        self,
        api_key: str | None = None,
        proxy_url: str | None = None,
    ):
        super().__init__(
            base_url="https://market.csgo.com/api",
            proxy_url=proxy_url,
        )
        self.api_key = api_key
        self.proxy_url = proxy_url

    async def get_prices(
        self, currency: Literal["RUB", "EUR", "USD"] = "USD"
    ) -> Prices:
        """Get market prices."""
        text = await self._get(
            f"/v2/prices/{currency}.json",
        )
        return Prices.model_validate_json(text)

    async def get_list_items_info(self, market_hash_names: list[str]) -> ListItemsInfo:
        """Get list items info. ( includes a partial sales history )"""
        text = await self._get(
            "/v2/get-list-items-info",
            params={
                "key": self.api_key,
                "list_hash_name[]": market_hash_names,
            },
        )
        return ListItemsInfo.model_validate_json(text)

    async def get_history(
        self, market_hash_name: str, phase: str | None = None
    ) -> HistoryResponse:
        """Get the full sales history of an item."""
        query = """
        query history($market_hash_name: String!, $phase: String) {
            history(market_hash_name: $market_hash_name, phase: $phase) {
                price time count currency
            }
        }
        """

        ua = UserAgent()
        body = {
            "operationName": "history",
            "query": query,
            "variables": {
                "market_hash_name": market_hash_name,
                "phase": phase or "",
            },
        }
        headers = {
            "User-Agent": ua.chrome,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Referer": "https://market.csgo.com/",
            "Origin": "https://market.csgo.com",
        }
        text = await self._post(
            "/graphql",
            json=body,
            headers=headers,
            timeout=30,
        )
        return HistoryResponse.model_validate_json(text)
