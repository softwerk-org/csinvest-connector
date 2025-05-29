from typing import cast
from bs4 import BeautifulSoup
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
            self.flaresolverr = Flaresolverr(flaresolverr_url)
        else:
            self.flaresolverr = None

    async def get_min_prices(self) -> dict[str, MarketPriceItem]:
        """Get minimum prices for all markets (updates every 10 minutes)."""
        assert self.flaresolverr is not None
        response = self.flaresolverr.get(
            "https://cs.money/api/min_price/market/all",
            timeout_s=60,
        )
        soup = BeautifulSoup(cast(str, response.solution.response), "html.parser")

        pre = soup.find("pre")
        if pre is None:
            raise ValueError("No <pre> tag found in response")

        json_text = pre.get_text(strip=True)
        return MinPrices.validate_json(json_text)
