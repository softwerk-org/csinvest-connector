from connector.base import Connector
from connector.youpin898.models.get_market_goods import MarketGoods


class YouPin898Connector(Connector):
    def __init__(self, proxy_url: str | None = None, session_kwargs: dict = {}):
        super().__init__(
            "https://api.youpin898.com/api/",
            proxy_url,
            session_kwargs,
        )

    async def get_market_goods(
        self,
        page_size: int,
        page_index: int,
        list_sort_type: int = 1,
        sort_type: int = 0,
    ):
        response = await self._post(
            "homepage/pc/goods/market/querySaleTemplate",
            data={
                "listSortType": list_sort_type,
                "sortType": sort_type,
                "pageSize": page_size,
                "pageIndex": page_index,
            },
        )
        return MarketGoods.model_validate_json(response)
