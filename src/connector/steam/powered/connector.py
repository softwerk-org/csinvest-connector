from connector.base import Connector
from .models.get_player_summaries import PlayerSummaries
from .models.get_asset_class_info import AssetClassInfo
from .models.get_number_of_current_players import NumberOfCurrentPlayers


class SteamPoweredConnector(Connector):
    """Connector for the Steam WebAPI (api.steampowered.com).

    Documentation: https://steamapi.xpaw.me
    """

    def __init__(self, proxy_url: str | None = None, api_key: str | None = None):
        super().__init__(
            base_url="https://api.steampowered.com",
            proxy_url=proxy_url,
        )
        self.api_key = api_key

    async def get_player_summaries(
        self,
        steamids: list[str] | str,
    ) -> PlayerSummaries:
        """Get player summaries for the given steamids."""
        if isinstance(steamids, list):
            steamids = ",".join(steamids)

        text = await self._get(
            "/ISteamUser/GetPlayerSummaries/v0002/",
            params={
                "key": self.api_key,
                "steamids": steamids,
                "format": "json",
            },
        )
        return PlayerSummaries.model_validate_json(text)

    async def get_asset_class_info(
        self, classids: list[str] | tuple[str, ...] | str, appid: int = 730
    ) -> AssetClassInfo:
        """Get asset class info for the given classids."""

        if isinstance(classids, tuple):
            classids = list(classids)
        elif isinstance(classids, str):
            classids = [classids]

        text = await self._get(
            "/ISteamEconomy/GetAssetClassInfo/v0001/",
            params={
                "key": self.api_key,
                "appid": appid,
                "class_count": len(classids),
                **{f"classid{ix}": classid for ix, classid in enumerate(classids)},
            },
        )
        return AssetClassInfo.model_validate_json(text)

    async def get_number_of_current_players(
        self,
        appid: int = 730,
    ) -> NumberOfCurrentPlayers:
        """Get the current number of players for the given *appid*."""

        text = await self._get(
            "/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
            params={
                "appid": appid,
                "format": "json",
            },
        )
        return NumberOfCurrentPlayers.model_validate_json(text)
