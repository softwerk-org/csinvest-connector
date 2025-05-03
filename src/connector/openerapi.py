from .base import BaseConnector


class OpenExchangeRatesConnector(BaseConnector):
    base = "https://open.er-api.com/v6"
    __docs__ = "https://open.er-api.com/documentation"

    def __init__(self, proxy_url: str | None = None):
        super().__init__(proxy_url=proxy_url)

    async def get_latest_rates(self, base_code: str = "USD"):
        response = await self._request(
            "GET",
            f"/latest/{base_code}",
            handler=lambda r: r.json(),
        )
        return response
