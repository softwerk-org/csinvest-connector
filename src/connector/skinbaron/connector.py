from connector.base import ConnectorBase
from .models.get_best_deals import GetBestDeals
from .models.get_price_list import GetPriceList

class SkinbaronConnector:
    __docs__ = "https://skinbaron.de/misc/apidoc/"
    
    def __init__(self, api_key: str, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://api.skinbaron.de", proxy_url=proxy_url)
        self.api_key = api_key
    

    async def get_best_deals(self, appid: int = 730, size: int = 100) -> GetBestDeals:
        assert size <= 100, "Size must be less than or equal to 100"
        text = await self.connector.request(
            "POST",
            "/BestDeals",
            headers={
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
            json={
                "appId": appid,
                "size": size,
                "apikey": self.api_key,
            }
        )
        return GetBestDeals.model_validate_json(text)

    async def get_price_list(self, appid: int = 730) -> GetPriceList:
        text = await self.connector.request(
            "POST",
            "/GetPriceList",
            headers={
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
            json={
                "appId": appid,
                "apikey": self.api_key,
            },
        )
        return GetPriceList.model_validate_json(text)