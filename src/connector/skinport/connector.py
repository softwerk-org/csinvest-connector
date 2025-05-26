import httpx
from connector.tools.flaresolverr import Flaresolverr
from .models.get_items import Items, Item
from .models.get_sales_history import SalesHistory, SalesItem
from .models.get_item import ItemResponse
from .utils import slugify


class SkinportConnector:
    """
    Unified connector for Skinport that provides both official API methods (get_items, get_sales_history)
    and unofficial web methods (get_item).
    """

    API_BASE_URL = "https://api.skinport.com"
    WEB_BASE_URL = "https://skinport.com"

    def __init__(
        self,
        proxy_url: str | None = None,
        flaresolverr_url: str | None = None,
    ):
        self.client = httpx.AsyncClient(proxy=proxy_url)
        self.flaresolverr = Flaresolverr(flaresolverr_url) if flaresolverr_url else None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def close(self):
        await self.client.aclose()

    async def get_items(
        self,
        appid: int = 730,
        currency: str = "USD",
        tradable: int = 0,
    ) -> list[Item]:
        """
        Retrieve marketplace item listings via the official Skinport API.
        """
        response = await self.client.get(
            f"{self.API_BASE_URL}/v1/items",
            params={"app_id": appid, "currency": currency, "tradable": tradable},
            headers={"Accept-Encoding": "br"},
            timeout=30,
        )
        response.raise_for_status()
        items = Items.model_validate_json(response.text)
        return items.root

    async def get_sales_history(
        self,
        market_hash_names: list[str] | None = None,
        appid: int = 730,
        currency: str = "USD",
    ) -> list[SalesItem]:
        """
        Retrieve aggregated sales history via the official Skinport API.
        """
        params: dict[str, str | int] = {"app_id": appid, "currency": currency}
        if market_hash_names is not None:
            params["market_hash_name"] = ",".join(market_hash_names)
        response = await self.client.get(
            f"{self.API_BASE_URL}/v1/sales/history",
            params=params,
            headers={"Accept-Encoding": "br"},
            timeout=30,
        )
        response.raise_for_status()
        stats = SalesHistory.model_validate_json(response.text)
        return stats.root

    async def get_item(
        self,
        market_hash_name: str,
        appid: int = 730,
    ) -> ItemResponse:
        """
        Retrieve public item details via the unofficial Skinport web API.
        """
        if not self.flaresolverr:
            raise ValueError("flaresolverr_url is required for web API requests")

        cookies, user_agent = self.flaresolverr.solve("https://skinport.com/en/market")
        response = await self.client.get(
            f"{self.WEB_BASE_URL}/api/item",
            params={"appid": appid, "url": slugify(market_hash_name)},
            headers={
                "User-Agent": user_agent,
                "Referer": "https://skinport.com/en/market",
            },
            cookies=cookies,
        )
        response.raise_for_status()
        return ItemResponse.model_validate_json(response.text)
