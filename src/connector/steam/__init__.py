from connector.steam.community import SteamCommunityConnector
from connector.steam.powered import SteamPoweredConnector


class SteamConnector:
    def __init__(
        self,
        username: str,
        password: str,
        api_key: str,
        proxy: str | None = None,
    ):
        self.powered = SteamPoweredConnector(api_key=api_key)
        self.community = SteamCommunityConnector(
            username=username,
            password=password,
            api_key=api_key,
            proxy=proxy,
        )

    async def __aenter__(self):
        await self.powered.__aenter__()
        await self.community.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.community.__aexit__(exc_type, exc_value, traceback)
        await self.powered.__aexit__(exc_type, exc_value, traceback)


__all__ = ["SteamConnector"]
