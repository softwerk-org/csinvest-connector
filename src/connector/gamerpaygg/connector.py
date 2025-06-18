from connector.base import Connector
from connector.gamerpaygg.models.get_sales import Sale, Sales
from connector.gamerpaygg.models.get_prices import Prices, Price


class GamerPayGgConnector(Connector):
    """Connector for the GamerPay.gg API.

    Documentation: https://api.gamerpay.gg/docs
    """

    def __init__(self, api_key: str | None = None, proxy_url: str | None = None):
        super().__init__(
            base_url="https://api.gamerpay.gg",
            proxy_url=proxy_url,
        )
        self.api_key = api_key

    async def get_prices(self) -> list[Price]:
        text = await self._get(
            "/prices",
            headers={"Accept": "application/json, text/plain, */*"},
        )
        prices = Prices.model_validate_json(text)
        return prices.root

    async def get_sales(self) -> dict[str, list[Sale]]:
        text = await self._get(
            "/v1/platform/sales",
            headers={
                "Authorization": f"{self.api_key}",
                "Accept": "application/json, text/plain, */*",
            },
        )
        sales = Sales.model_validate_json(text)
        return sales.root
