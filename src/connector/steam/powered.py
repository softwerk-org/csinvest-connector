from typing import Any

from connector.base import BaseConnector


class SteamPoweredConnector(BaseConnector):
    base = "https://api.steampowered.com"
    __docs__ = "https://steamapi.xpaw.me"

    def __init__(self, proxy_url: str | None = None, api_key: str | None = None):
        super().__init__(proxy_url=proxy_url)
        self.api_key = api_key

    async def get_player_summaries(
        self, steamids: list[str] | str, format: str = "json"
    ) -> dict[str, Any]:
        """Get player summaries for the given steamids."""
        if isinstance(steamids, list):
            steamids = ",".join(steamids)

        response = await self._request(
            "GET",
            "/ISteamUser/GetPlayerSummaries/v0002/",
            params={
                "key": self.api_key,
                "steamids": steamids,
                "format": format,
            },
            handler=lambda r: r.json(),
        )
        return response

    async def get_asset_class_info(
        self, classids: list[str] | str, appid: int = 730
    ) -> dict[str, Any]:
        """Get asset class info for the given classids."""

        if not isinstance(classids, list):
            classids = [classids]

        response = await self._request(
            "GET",
            "/ISteamEconomy/GetAssetClassInfo/v0001/",
            params={
                "key": self.api_key,
                "appid": appid,
                "class_count": len(classids),
                **{f"classid{ix}": classid for ix, classid in enumerate(classids)},
            },
            handler=lambda r: r.json(),
        )
        return response
