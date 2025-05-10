from connector.base import ConnectorBase
from .models.get_player_summaries import GetPlayerSummaries
from .models.get_asset_class_info import GetAssetClassInfo


class SteamPoweredConnector:
    __docs__ = "https://steamapi.xpaw.me"

    def __init__(self, proxy_url: str | None = None, api_key: str | None = None):
        self.connector = ConnectorBase(base_url="https://api.steampowered.com", proxy_url=proxy_url)
        self.api_key = api_key

    async def get_player_summaries(
        self, steamids: list[str] | str, format: str = "json",
    ) -> GetPlayerSummaries:
        """Get player summaries for the given steamids."""
        if isinstance(steamids, list):
            steamids = ",".join(steamids)

        text = await self.connector.request(
            "GET",
            "/ISteamUser/GetPlayerSummaries/v0002/",
            params={
                "key": self.api_key,
                "steamids": steamids,
                "format": format,
            },
        )
        return GetPlayerSummaries.model_validate_json(text)

    async def get_asset_class_info(
        self, classids: list[str] | str, appid: int = 730
    ) -> GetAssetClassInfo:
        """Get asset class info for the given classids."""

        if not isinstance(classids, list):
            classids = [classids]

        text = await self.connector.request(
            "GET",
            "/ISteamEconomy/GetAssetClassInfo/v0001/",
            params={
                "key": self.api_key,
                "appid": appid,
                "class_count": len(classids),
                **{f"classid{ix}": classid for ix, classid in enumerate(classids)},
            },
        )
        return GetAssetClassInfo.model_validate_json(text)
