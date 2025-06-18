from connector.base import Connector
from .auth import SteamAuth
from .models.get_market_page import MarketPage
from .models.get_pricehistory import Pricehistory
from .models.get_inventory import Inventory
from .models.get_partner_inventory import PartnerInventory
from .models.get_profile import Profile
from .models.get_market_listings import MarketListings
import xmltodict


class SteamCommunityConnector(Connector):
    """Connector for Steam Community API.

    Documentation: https://github.com/Revadike/InternalSteamWebAPI/wiki
    """

    def __init__(
        self,
        username: str,
        password: str,
        api_key: str,
        proxy_url: str | None = None,
    ):
        super().__init__(base_url="https://steamcommunity.com", proxy_url=proxy_url)
        self.auth = SteamAuth(
            username=username,
            password=password,
            api_key=api_key,
        )

    async def get_market_page(
        self,
        start: int,
        count: int = 100,
        appid: int = 730,
        language: str = "DE",
        norender: str = "1",
        search_descriptions: str = "0",
        sort_dir: str = "asc",
        currency: int = 0,
    ) -> MarketPage:
        """Get market page."""
        text = await self._get(
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
        )
        return MarketPage.model_validate_json(text)

    async def get_pricehistory(
        self,
        market_hash_name: str,
        country: str = "DE",
        currency: int = 0,
        appid: int = 730,
    ) -> Pricehistory:
        """Get price history for an item."""
        text = await self._get(
            "/market/pricehistory/",
            params={
                "country": country,
                "currency": currency,
                "appid": appid,
                "market_hash_name": market_hash_name,
            },
            cookies=await self.auth.cookies(),
        )
        return Pricehistory.model_validate_json(text)

    async def get_inventory(
        self,
        steamid: str,
        appid: int = 730,
        contextid: int = 2,
        language: str = "english",
        count: int = 2500,
        start_assetid: str | None = None,
    ) -> Inventory:
        """Get inventory of a user identified by steamid."""
        assert count <= 2500, "Count must be less than or equal to 2500"
        params = {
            "l": language,
            "count": count,
        }
        if start_assetid:
            params["start_assetid"] = start_assetid

        text = await self._get(
            f"inventory/{steamid}/{appid}/{contextid}",
            params=params,
            headers={
                "Referer": f"https://steamcommunity.com/profiles/{steamid}",
            },
            cookies=await self.auth.cookies(),
        )
        return Inventory.model_validate_json(text)

    async def get_partner_inventory(
        self,
        steamid: str,
        appid: int = 730,
        contextid: int = 2,
        language: str = "english",
    ) -> PartnerInventory:
        """
        Get all tradeable items of a user identified by steamid.
        This method utilizes a enpoint for trading items with other users. It only returns tradeable items.
        """
        params = {
            "l": language,
            "partner": steamid,
            "appid": appid,
            "contextid": contextid,
            "sessionid": (await self.auth.cookies()).get("sessionid"),
        }
        text = await self._get(
            "/tradeoffer/new/partnerinventory/",
            params=params,
            cookies=await self.auth.cookies(),
            headers={
                "Referer": f"https://steamcommunity.com/tradeoffer/new/?partner={steamid}",
            },
        )
        return PartnerInventory.model_validate_json(text)

    async def get_market_listings(
        self,
        market_hash_name: str,
        appid: int = 730,
        start: int = 0,
        count: int = 1,
        currency: int = 1,
        language: str = "english",
    ) -> MarketListings:
        """Get a unique listings for an item."""
        text = await self._get(
            f"/market/listings/{appid}/{market_hash_name}/render",
            params={
                "start": start,
                "count": count,
                "currency": currency,
                "language": language,
            },
        )
        return MarketListings.model_validate_json(text)

    async def get_profile(self, steamid: str) -> Profile:
        """Get profile information for a user."""
        text = await self._get(
            f"/profiles/{steamid}/",
            params={"xml": 1},
        )

        return Profile.model_validate(xmltodict.parse(text))
