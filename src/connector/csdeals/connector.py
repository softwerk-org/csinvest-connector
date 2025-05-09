from connector.base import ConnectorBase
from connector.response import ConnectorResponse
from .models.get_lowest_prices import GetLowestPrices


class CsDealsConnector:
    __docs__ = "https://cs.deals/es/API-documentation"

    def __init__(self, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://cs.deals/API", proxy_url=proxy_url)

    async def get_lowest_prices(self, app_id: str = "730") -> ConnectorResponse[GetLowestPrices]:
        text = await self.connector.request(
            "GET",
            "/IPricing/GetLowestPrices/v1",
            params={"appid": app_id},
        )
        return ConnectorResponse[GetLowestPrices](text) 