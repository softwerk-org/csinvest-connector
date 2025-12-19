import json
from connector.base import Connector
from connector.skins.models.get_market_items import MarketItems


class SkinsConnector(Connector):

    def __init__(
        self,
        base_url: str = "https://api.skins.com",
        proxy_url: str | None = None,
        session_kwargs: dict = {},
    ):
        super().__init__(base_url, proxy_url, session_kwargs)

    async def get_market_items(
        self,
        page: int,
        limit: int,
        sort_by: str = "price",
        sort_order: str = "desc",
    ) -> dict:
        response = await self._get(
            "/public/market/items",
            params={
                "sortBy": sort_by,
                "sortOrder": sort_order,
                "page": page,
                "limit": limit,
            },
        )
        return json.loads(response)
