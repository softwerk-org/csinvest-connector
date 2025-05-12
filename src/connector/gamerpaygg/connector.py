from connector.base import Connector
from connector.gamerpaygg.models.get_sales import Sale, Sales
from connector.gamerpaygg.models.get_prices import Prices


class GamerPayGgConnector:
    __docs__ = "https://api.gamerpay.gg/docs"

    def __init__(self, proxy: str | None = None):
        self.connector = Connector(
            base_url="https://api.gamerpay.gg",
            proxy=proxy,
        )

    async def get_prices(self) -> list[Prices]:
        text = await self.connector.get(
            "/prices",
        )
        prices = Prices.model_validate_json(text)
        return prices.root

    async def get_sales(self) -> dict[str, list[Sale]]:
        text = await self.connector.get(
            "/prices",
        )
        sales = Sales.model_validate_json(text)
        return sales.root
