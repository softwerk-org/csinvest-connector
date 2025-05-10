from connector.base import ConnectorBase
from .models.get_prices import GetPrices

class GamerPayGgConnector:
    __docs__ = "https://api.gamerpay.gg/docs"

    def __init__(self, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://api.gamerpay.gg", proxy_url=proxy_url)

    async def get_prices(self) -> GetPrices:
        text = await self.connector.request(
            "GET",
            "/prices",
        )
        return GetPrices.model_validate_json(text)