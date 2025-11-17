from connector.base import Connector
from connector.buffmarket.models.get_market_goods import MarketGoods


class BuffMarketConnector(Connector):
    def __init__(self, proxy_url: str | None = None, session_kwargs: dict = {}):
        super().__init__(
            "https://api.buff.market/api/",
            proxy_url,
            session_kwargs,
        )

    async def get_market_goods(
        self,
        page_num: int,
        page_size: int,
        tab: str = "selling",
        game: str = "csgo",
    ):
        response = await self._get(
            "market/goods",
            params={
                "game": game,
                "tab": tab,
                "page_num": page_num,
                "page_size": page_size,
            },
        )
        return MarketGoods.model_validate_json(response)
