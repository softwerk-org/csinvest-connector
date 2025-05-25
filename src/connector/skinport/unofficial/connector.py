from connector.base import Connector
from connector.tools.flaresolverr import Flaresolverr
from .models.get_item import ItemResponse
from ..utils import slugify


class SkinportUnofficialConnector(Connector):
    """Connector for the Skinport Unofficial Web API."""

    def __init__(
        self,
        proxy_url: str | None = None,
        flaresolverr_url: str | None = None,
    ):
        super().__init__(base_url="https://skinport.com/api", proxy_url=proxy_url)
        if flaresolverr_url:
            self.flaresolverr = Flaresolverr(flaresolverr_url)

    async def get_item(
        self,
        market_hash_name: str,
        appid: int = 730,
    ) -> ItemResponse:
        """
        Fetch public item details via the web interface.
        This endpoints provides the full item sales history.
        """
        assert self.flaresolverr, "flaresolverr_url is required"
        cookies, user_agent = self.flaresolverr.solve("https://skinport.com/en/market")
        headers = {
            "User-Agent": user_agent,
            "Referer": "https://skinport.com/en/market",
        }
        text = await self._get(
            "/item",
            params={
                "appid": appid,
                "url": slugify(market_hash_name),
            },
            headers=headers,
            cookies=cookies,
        )
        return ItemResponse.model_validate_json(text)
