from connector.base import Connector
from connector.skinbaron.models.get_newest_sales import NewestSales
from .models.get_best_deals import BestDeals
from .models.get_price_list import PriceList


class SkinbaronConnector(Connector):
    """Connector for the SkinBaron API.

    Documentation: https://skinbaron.de/misc/apidoc/
    """

    def __init__(self, api_key: str | None = None, proxy_url: str | None = None):
        super().__init__(
            base_url="https://api.skinbaron.de",
            proxy_url=proxy_url,
        )
        self.api_key = api_key

    async def get_best_deals(self, appid: int = 730, size: int = 100) -> BestDeals:
        assert size <= 100, "Size must be less than or equal to 100"
        text = await self._post(
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
        text = await self._post(
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
        doppler_phase: str | None = None,
    ) -> NewestSales:
        payload = {
            "apikey": self.api_key,
            "itemName": market_hash_name,
            "statTrak": stat_trak,
            "souvenir": souvenir,
        }
        if doppler_phase:
            payload["dopplerPhase"] = doppler_phase

        text = await self._post(
            "/GetNewestSales30Days",
            headers={
                "X-Requested-With": "XMLHttpRequest",
            },
            json=payload,
        )
        return NewestSales.model_validate_json(text)
