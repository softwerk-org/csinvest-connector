from .base import BaseConnector


class CsDealsConnector(BaseConnector):
    base = "https://cs.deals/API"
    __docs__ = "https://cs.deals/es/API-documentation"

    def __init__(self, proxy_url: str | None = None):
        super().__init__(proxy_url=proxy_url)

    async def get_lowest_prices(self, app_id: str = "730"):
        response = await self._request(
            "GET",
            "/IPricing/GetLowestPrices/v1",
            params={"appid": app_id},
            handler=lambda r: r.json(),
        )
        return response
