from connector.base import Connector
from connector.csmoney.models.get_min_prices import MarketPriceItem, MinPrices
from connector.tools.flaresolverr import Flaresolverr


class CSMoneyConnector(Connector):
    """Connector for CS.Money public endpoints.

    No official documentation URL is available.
    """

    def __init__(
        self,
        proxy_url: str | None = None,
        flaresolverr_url: str | None = None,
    ):
        super().__init__(
            base_url="https://cs.money/api",
            proxy_url=proxy_url,
        )
        if flaresolverr_url:
            self.flaresolverr = Flaresolverr(
                flaresolverr_url,
                cache_response=True,
                cache_ttl_min=10,
            )
        else:
            self.flaresolverr = None

    async def get_min_prices(self) -> dict[str, MarketPriceItem]:
        """Get minimum prices for all markets (updates every 10 minutes)."""
        assert self.flaresolverr is not None
        response = self.flaresolverr.get(
            "https://cs.money/api/min_price/market/all",
            return_only_cookies=True,
            timeout_s=60,
        )
        cookies = {
            cookie["name"]: cookie["value"] for cookie in response.solution.cookies
        }
        user_agent = response.solution.userAgent
        text = await self._get(
            "/min_price/market/all",
            cookies=cookies,
            headers={"User-Agent": user_agent},
            timeout=30,
        )

        min_prices = MinPrices.model_validate_json(text)
        return min_prices.root
