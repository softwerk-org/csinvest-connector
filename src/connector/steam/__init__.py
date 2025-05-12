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


__all__ = ["SteamConnector"]
