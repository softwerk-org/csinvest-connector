from typing import Literal

from connector.base import Connector
from connector.marketcsgo.models.get_history import HistoryResponse
from connector.marketcsgo.models.get_prices import Prices
from connector.marketcsgo.models.get_list_items_info import listItemsInfo
from connector.tools.flaresolverr import Flaresolverr


class MarketCsgoConnector(Connector):
    """Connector for the Market.CSGO API.

    Documentation: https://market.csgo.com/en/api
    """

    def __init__(
        self,
        api_key: str | None = None,
        proxy_url: str | None = None,
        flaresolverr_url: str | None = None,
    ):
        super().__init__(
            base_url="https://market.csgo.com/api",
            proxy_url=proxy_url,
        )
        self.api_key = api_key
        self.flaresolverr_url = flaresolverr_url
        self.proxy_url = proxy_url
        self.flaresolverr = Flaresolverr()

    async def get_prices(
        self, currency: Literal["RUB", "EUR", "USD"] = "USD"
    ) -> Prices:
        """Get market prices."""
        text = await self._get(
            f"/v2/prices/{currency}.json",
        )
        return Prices.model_validate_json(text)

    async def get_list_items_info(self, market_hash_names: list[str]) -> listItemsInfo:
        """Get list items info. ( includes a partial sales history )"""
        text = await self._get(
            "/v2/get-list-items-info",
            params={
                "key": self.api_key,
                "list_hash_name[]": market_hash_names,
            },
        )
        return listItemsInfo.model_validate_json(text)

    async def get_history(
        self, market_hash_name: str, phase: str | None = None
    ) -> HistoryResponse:
        """Get the full sales history of an item."""
        assert self.flaresolverr_url is not None, "flaresolverr is required"
        query = """
        query history($market_hash_name: String!, $phase: String) {
            history(market_hash_name: $market_hash_name, phase: $phase) {
                price time count currency
            }
        }
        """
        cookies, user_agent = self.flaresolverr.solve(
            str(self.client.base_url) + "/graphql",
            self.flaresolverr_url,
            self.proxy_url,
        )
        body = {
            "operationName": "history",
            "query": query,
            "variables": {
                "market_hash_name": market_hash_name,
                "phase": phase or "",
            },
        }
        headers = {
            "User-Agent": user_agent,
            "Referer": "https://market.csgo.com/",
            "Origin": "https://market.csgo.com",
        }
        text = await self._post(
            "/graphql",
            json=body,
            cookies=cookies,
            headers=headers,
        )
        return HistoryResponse.model_validate_json(text)
