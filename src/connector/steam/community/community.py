from typing import Any

import xmltodict

from connector.base import BaseConnector
from connector.steam.auth import SteamAuthenticator

from connector.steam.community.models import PriceHistory


class SteamCommunityConnector(BaseConnector):
    base = "https://steamcommunity.com"
    __docs__ = "https://github.com/Revadike/InternalSteamWebAPI/wiki"

    def __init__(
        self,
        username: str,
        password: str,
        api_key: str,
        proxy_url: str | None = None,
    ):
        super().__init__(proxy_url=proxy_url)
        self.username = username
        self.password = password
        self.steam_auth = SteamAuthenticator(
            username=self.username, password=self.password, api_key=api_key
        )

    async def get_market_listings(
        self,
        start: int,
        count: int = 100,
        appid: int = 730,
        language: str = "DE",
        norender: str = "1",
        search_descriptions: str = "0",
        sort_dir: str = "asc",
        currency: int = 0,
    ) -> dict[str, Any]:
        """Get market listings."""
        response = await self._request(
            "GET",
            "/market/search/render/",
            params={
                "start": start,
                "count": count,
                "appid": appid,
                "l": language,
                "norender": norender,
                "search_descriptions": search_descriptions,
                "sort_dir": sort_dir,
                "currency": currency,
            },
            handler=lambda r: r.json(),
        )
        return response

    async def get_pricehistory(
        self,
        market_hash_name: str,
        country: str = "DE",
        currency: int = 0,
        appid: int = 730,
    ) -> dict[str, Any]:
        """Get price history for an item."""

        response = await self._request(
            "GET",
            "/market/pricehistory/",
            params={
                "country": country,
                "currency": currency,
                "appid": appid,
                "market_hash_name": market_hash_name,
            },
            cookies=await self.steam_auth.get_cookies(),
        )

        return PriceHistory(**response.json())

    async def get_inventory(
        self,
        steamid: str,
        appid: int = 730,
        contextid: int = 2,
        language: str = "english",
        count: int = 5000,
        start_assetid: str | None = None,
    ) -> dict[str, Any]:
        """Get inventory of a user identified by steamid."""
        params = {
            "l": language,
            "count": count,
        }
        if start_assetid:
            params["start_assetid"] = start_assetid

        response = await self._request(
            "GET",
            f"/inventory/{steamid}/{appid}/{contextid}",
            params=params,
            handler=lambda r: r.json(),
            cookies=await self.steam_auth.get_cookies(),
        )
        return response

    async def get_partner_inventory(
        self,
        steamid: str,
        appid: int = 730,
        contextid: int = 2,
        language: str = "english",
    ):
        """
        Get all tradeable items of a user identified by steamid.
        This method utilizes a enpoint for trading items with other users. It only returns tradeable items.
        """
        params = {
            "l": language,
            "partner": steamid,
            "appid": appid,
            "contextid": contextid,
            "sessionid": (await self.steam_auth.get_cookies()).get("sessionid"),
        }
        response = await self._request(
            "GET",
            "/tradeoffer/new/partnerinventory/",
            params=params,
            handler=lambda r: r.json(),
            cookies=await self.steam_auth.get_cookies(),
            headers={
                "Referer": f"https://steamcommunity.com/tradeoffer/new/?partner={steamid}",
            },
        )
        return response

    async def get_market_page(
        self,
        market_hash_name: str,
        appid: int = 730,
    ) -> str | None:
        """Get market page HTML for an item."""
        response = await self._request(
            "GET",
            f"/market/listings/{appid}/{market_hash_name}",
            handler=lambda r: r.text,
        )
        return response

    async def get_profile(self, steamid: str) -> dict[str, Any]:
        """Get the profile of an user"""
        response = await self._request(
            "GET",
            f"/profiles/{steamid}/",
            params={"xml": 1},
            handler=lambda r: xmltodict.parse(r.text),
        )
        return response
