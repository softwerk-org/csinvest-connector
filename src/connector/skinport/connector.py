from connector.base import ConnectorBase
from .models.get_items import GetItems


class SkinportConnector:
    __docs__ = "https://docs.skinport.com/"

    def __init__(self, proxy_url: str | None = None):
        self.connector = ConnectorBase(base_url="https://api.skinport.com/v1", proxy_url=proxy_url)

    async def get_items(
        self,
        appid: int = 730,
        currency: str = "USD",
        tradable: int = 0,
    ) -> GetItems:
        text = await self.connector.request(
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
        )
        return GetItems.model_validate_json(text)