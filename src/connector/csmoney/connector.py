from connector.base import Connector
from connector.csmoney.models.get_min_prices import MarketPriceItem, MinPrices
from connector.csmoney.models.get_price_trader_log import PriceTraderLogResponse


class CSMoneyConnector(Connector):
    """Connector for CS.Money public endpoints.

    No official documentation URL is available.
    """

    WIKI_BASE_URL = "https://wiki.cs.money"
    MARKET_BASE_URL = "https://cs.money"

    def __init__(
        self,
        proxy_url: str | None = None,
    ):
        super().__init__(proxy_url=proxy_url)

    async def get_min_prices(self) -> dict[str, MarketPriceItem]:
        """Get minimum prices for all markets (updates every 10 minutes)."""
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Priority": "u=0, i",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
            "Origin": "https://cs.money",
            "Referer": "https://cs.money/",
        }

        text = await self._get(
            f"{self.MARKET_BASE_URL}/api/min_price/market/all",
            headers=headers,
        )
        return MinPrices.validate_json(text)

    async def get_price_trader_log(self, name_ids: list[int]) -> PriceTraderLogResponse:
        """Get price trader log data for given name IDs."""
        query = """
        query price_trader_log($name_ids: [Int!]!) {
          price_trader_log(input: {name_ids: $name_ids}) {
            name_id
            values {
              price_trader_new
              time
            }
          }
        }
        """

        body = {
            "operationName": "price_trader_log",
            "query": query,
            "variables": {
                "name_ids": name_ids,
            },
        }

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://wiki.cs.money",
            "Referer": "https://wiki.cs.money/",
        }

        text = await self._post(
            f"{self.WIKI_BASE_URL}/api/graphql",
            json=body,
            headers=headers,
        )
        return PriceTraderLogResponse.model_validate_json(text)
