from connector.base import Connector
from connector.skinbaron.models.get_newest_sales import NewestSales
from .models.get_best_deals import BestDeals
from .models.get_price_list import PriceList


class SkinbaronConnector:
    __docs__ = "https://skinbaron.de/misc/apidoc/"

    def __init__(self, api_key: str, proxy: str | None = None):
        self.connector = Connector(
            base_url="https://api.skinbaron.de",
            proxy=proxy,
        )
        self.api_key = api_key

    async def get_best_deals(self, appid: int = 730, size: int = 100) -> BestDeals:
        assert size <= 100, "Size must be less than or equal to 100"
        text = await self.connector.post(
            "/BestDeals",
            headers={
                "X-Requested-With": "XMLHttpRequest",
            },
            json={
                "appId": appid,
                "size": size,
                "apikey": self.api_key,
            },
        )
        return BestDeals.model_validate_json(text)

    async def get_price_list(self, appid: int = 730) -> PriceList:
        text = await self.connector.post(
            "/GetPriceList",
            headers={
                "X-Requested-With": "XMLHttpRequest",
            },
            json={
                "appId": appid,
                "apikey": self.api_key,
            },
        )
        return PriceList.model_validate_json(text)

    async def get_newest_sales(
        self,
        market_hash_name: str,
        stat_trak: bool = False,
        souvenir: bool = False,
    ) -> NewestSales:
        text = await self.connector.post(
            "/NewestSales30Days",
            headers={
                "X-Requested-With": "XMLHttpRequest",
            },
            json={
                "apikey": self.api_key,
                "itemName": market_hash_name,
                "statTrak": stat_trak,
                "souvenir": souvenir,
            },
        )
        return NewestSales.model_validate_json(text)
