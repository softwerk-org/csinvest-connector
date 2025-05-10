from connector.base import ConnectorBase
from .models.get_lowest_prices import GetLowestPrices


class CsDealsConnector:
    __docs__ = "https://cs.deals/es/API-documentation"

    def __init__(self, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://cs.deals/API", proxy_url=proxy_url)

    async def get_lowest_prices(self, app_id: int = 730) -> GetLowestPrices:
        """Get the lowest prices for all items."""
        text = await self.connector.request(
            "GET",
            "/IPricing/GetLowestPrices/v1",
            params={"appid": app_id},
        )
        return GetLowestPrices.model_validate_json(text)