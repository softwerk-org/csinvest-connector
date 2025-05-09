from connector.base import ConnectorBase
from connector.response import ConnectorResponse
from .models.get_best_deals import GetBestDeals
from .models.get_price_list import GetPriceList
import json

class SkinbaronConnector:
    __docs__ = "https://skinbaron.de/misc/apidoc/"
    
    def __init__(self, api_key: str, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://api.skinbaron.de", proxy_url=proxy_url)
        self.api_key = api_key
    

    async def get_best_deals(self, appid: int = 730, size: int = 100) -> ConnectorResponse[GetBestDeals]:
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
        data = json.loads(text)
        if isinstance(data, list):
            text = json.dumps({"bestDeals": data})
        return ConnectorResponse[GetBestDeals](text)

    async def get_price_list(self, appid: int = 730) -> ConnectorResponse[GetPriceList]:
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
        data = json.loads(text)
        if isinstance(data, list):
            text = json.dumps({"map": data})
        return ConnectorResponse[GetPriceList](text)