from connector.base import BaseConnector

class SkinBaronConnector(BaseConnector):
    base = "https://api.skinbaron.de"
    __docs__ = "https://skinbaron.de/misc/apidoc/"
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    

    async def get_best_deals(self, appid: int = 730, size: int = 100) -> list[dict]:
        assert size <= 100, "Size must be less than or equal to 100"

        response = await self._request(
            "POST",
            "/BestDeals",
            headers={
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
            body={
                "appId": appid,
                "size": size,
                "apikey": self.api_key,
            },
            handler=lambda r: r.json(),
        )
        return response

    async def get_price_list(self, appid: int = 730) -> list[dict]:
        response = await self._request(
            "POST",
            "/GetPriceList",
            headers={
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
            body={
                "appId": appid,
                "apikey": self.api_key,
            },
            handler=lambda r: r.json(),
        )
        return response
