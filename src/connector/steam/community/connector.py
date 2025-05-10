from connector.base import ConnectorBase
from .auth import SteamAuth
from .models.get_market_listings import GetMarketListings
from .models.get_pricehistory import GetPricehistory
from .models.get_inventory import GetInventory
from .models.get_partner_inventory import GetPartnerInventory
from .models.get_profile import GetProfile
import xmltodict

class SteamCommunityConnector:
    __docs__ = "https://github.com/Revadike/InternalSteamWebAPI/wiki"

    def __init__(
        self,
        username: str,
        password: str,
        api_key: str,
        proxy_url: str | None = None,
    ):
        self.connector = ConnectorBase(
            base_url="https://steamcommunity.com", proxy_url=proxy_url
        )
        self.auth = SteamAuth(
            username=username,
            password=password,
            api_key=api_key,
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
    ) -> GetMarketListings:
        """Get market listings."""
        text = await self.connector.request(
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
        )
        return GetMarketListings.model_validate_json(text)

    async def get_pricehistory(
        self,
        market_hash_name: str,
        country: str = "DE",
        currency: int = 0,
        appid: int = 730,
    ) -> GetPricehistory:
        """Get price history for an item."""
        text = await self.connector.request(
            "GET",
            "/market/pricehistory/",
            params={
                    "country": country,
                    "currency": currency,
                    "appid": appid,
                    "market_hash_name": market_hash_name,
                },
                cookies=await self.auth.cookies(),
        )
        return GetPricehistory.model_validate_json(text)

    async def get_inventory(
        self,
        steamid: str,
        appid: int = 730,
        contextid: int = 2,
        language: str = "english",
        count: int = 5000,
        start_assetid: str | None = None,
    ) -> GetInventory:
        """Get inventory of a user identified by steamid."""
        params = {
            "l": language,
            "count": count,
        }
        if start_assetid:
            params["start_assetid"] = start_assetid

        text = await self.connector.request(
            "GET",
            f"/inventory/{steamid}/{appid}/{contextid}",
            params=params,
            cookies=await self.auth.cookies(),
        )
        return GetInventory.model_validate_json(text)

    async def get_partner_inventory(
        self,
        steamid: str,
        appid: int = 730,
        contextid: int = 2,
        language: str = "english",
    ) -> GetPartnerInventory:
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
        text = await self.connector.request(
            "GET",
            "/tradeoffer/new/partnerinventory/",
            params=params,
            cookies=await self.auth.cookies(),
            headers={
                "Referer": f"https://steamcommunity.com/tradeoffer/new/?partner={steamid}",
            },
        )
        return GetPartnerInventory.model_validate_json(text)

    async def get_market_page(
        self,
        market_hash_name: str,
        appid: int = 730,
    ) -> str:
        """Get market page HTML for an item."""
        text = await self.connector.request(
            "GET",
            f"/market/listings/{appid}/{market_hash_name}",
        )
        return text

    async def get_profile(self, steamid: str) -> GetProfile:
        """Get profile information for a user."""
        text = await self.connector.request(
            "GET",
            f"/profiles/{steamid}/",
            params={"xml": 1},
        )

        return GetProfile.model_validate(xmltodict.parse(text))
