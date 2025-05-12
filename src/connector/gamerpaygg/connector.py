from connector.base import Connector
from connector.gamerpaygg.models.get_sales import Sales
from connector.gamerpaygg.models.get_prices import Prices


class GamerPayGgConnector:
    __docs__ = "https://api.gamerpay.gg/docs"

    def __init__(self, proxy: str | None = None):
        self.connector = Connector(
            base_url="https://api.gamerpay.gg",
            proxy=proxy,
        )

    async def get_prices(self) -> Prices:
        text = await self.connector.get(
            "/prices",
        )
        return Prices.model_validate_json(text)

    async def get_sales(self) -> Sales:
        text = await self.connector.get(
            "/v1/platform/sales",
        )
        return Sales.model_validate_json(text)
