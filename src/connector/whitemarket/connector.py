from connector.base import Connector
from connector.whitemarket.models.get_prices import Price, Prices
from connector.whitemarket.models.get_history import SalesHistoryResponse


class WhiteMarketConnector(Connector):
    """Connector for the WhiteMarket API.

    Documentation: https://api.white.market/docs_partner
    """

    S3_BASE_URL = "https://s3.white.market"
    API_BASE_URL = "https://api.white.market"

    def __init__(self, proxy_url: str | None = None):
        super().__init__(proxy_url=proxy_url)

    async def get_prices(self, appid: int = 730) -> list[Price]:
        """Get all lowest prices for a given appid."""
        text = await self._get(f"{self.S3_BASE_URL}/export/v1/prices/{appid}.json")
        return Prices.validate_json(text)

    async def get_sales_history(
        self,
        market_hash_name: str,
        appid: str = "CSGO",
    ) -> SalesHistoryResponse:
        """Get the sales history list from the WhiteMarket GraphQL API."""

        query = f"""
        {{
          market_stats_product(
            appId: {appid},
            nameHash: "{market_hash_name}"
          ) {{
            priceAvg
            volume
            date
          }}
        }}
        """

        text = await self._post(
            f"{self.API_BASE_URL}/graphql/api",
            json={"query": query},
        )

        return SalesHistoryResponse.model_validate_json(text)
