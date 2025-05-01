from .base import BaseConnector


class SkinportConnector(BaseConnector):
    base = "https://api.skinport.com/v1"
    __docs__ = "https://docs.skinport.com/"

    def __init__(self, proxy_url: str | None = None):
        super().__init__(proxy_url=proxy_url)

    async def get_items(
        self,
        appid: int = 730,
        currency: str = "USD",
        tradable: int = 0,
    ):
        response = await self._request(
            "GET",
            "/items",
            headers={
                "Accept-Encoding": "br",
            },
            params={
                "app_id": appid,
                "currency": currency,
                "tradable": tradable,
            },
            proxied=False,
            handler=lambda r: r.json(),
        )
        return response
