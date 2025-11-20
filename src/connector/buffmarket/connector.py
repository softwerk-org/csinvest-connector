from connector.base import Connector
from connector.buffmarket.auth import BuffMarketAuth
from connector.buffmarket.models.get_market_goods import MarketGoods
from connector.steam.community.auth import SteamAuth


class BuffMarketConnector(Connector):
    def __init__(
        self,
        steam_username: str,
        steam_password: str,
        steam_api_key: str,
        proxy_url: str | None = None,
        session_kwargs: dict = {},
    ):
        super().__init__(
            "https://api.buff.market/api/",
            proxy_url,
            session_kwargs,
        )
        steam_auth = SteamAuth(
            username=steam_username,
            password=steam_password,
            api_key=steam_api_key,
        )
        self.buff_auth = BuffMarketAuth(steam_auth)

    async def get_market_goods(
        self,
        page_num: int,
        page_size: int,
        tab: str = "selling",
        game: str = "csgo",
    ):

        buff_cookies = await self.buff_auth.get_cookies()
        response = await self._get(
            "market/goods",
            params={
                "game": game,
                "tab": tab,
                "page_num": page_num,
                "page_size": page_size,
            },
            headers={
                "X-CSRFToken": buff_cookies["csrf_token"],
            },
            cookies=buff_cookies,
        )
        return MarketGoods.model_validate_json(response)
