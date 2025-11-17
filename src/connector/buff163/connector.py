from connector.base import Connector
from connector.buff163.models.get_market_goods import MarketGoods


class Buff163Connector(Connector):
    def __init__(
        self,
        proxy_url: str | None = None,
        session_kwargs: dict = {},
    ):
        super().__init__(
            "https://buff.163.com/api/",
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
                "page_num": page_num,
                "page_size": page_size,
                "tab": tab,
                "game": game,
            },
        )
        return MarketGoods.model_validate_json(response)
