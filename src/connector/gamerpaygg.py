from .base import BaseConnector


class GamerPayGgConnector(BaseConnector):
    base = "https://api.gamerpay.gg"
    __docs__ = "https://api.gamerpay.gg/docs"

    def __init__(self, proxy_url: str | None = None):
        super().__init__(proxy_url=proxy_url)

    async def get_prices(self):
        response = await self._request(
            "GET",
            "/prices",
            handler=lambda r: r.json(),
        )
        return response
