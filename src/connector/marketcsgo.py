from typing import Any, Literal

from .base import BaseConnector


class MarketCsgoConnector(BaseConnector):
    base = "https://market.csgo.com/api/v2"
    __docs__ = "https://market.csgo.com/docs-v2"

    def __init__(self, proxy_url: str | None = None):
        super().__init__(proxy_url=proxy_url)

    async def get_prices(
        self, currency: Literal["RUB", "EUR", "USD"] = "USD"
    ) -> dict[str, Any]:
        """Get market prices."""
        response = await self._request(
            "GET",
            f"/prices/{currency}.json",
            proxied=True,
            handler=lambda r: r.json(),
        )
        return response
