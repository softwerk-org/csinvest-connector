import pytest
import os
from httpx import HTTPStatusError

from connector.steam import SteamConnector


@pytest.mark.asyncio
async def test_get_market_listings_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.community.get_market_listings(start=0, count=10)
    assert model.success is not None


@pytest.mark.asyncio
async def test_get_pricehistory_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        try:
            model = await connector.community.get_pricehistory(
                market_hash_name="Kilowatt Case"
            )
        except HTTPStatusError as e:
            if e.response.status_code == 500:
                pytest.skip(
                    "Internal server error from Steam, skipping integration test"
                )
            raise
        assert model.prices is not None


@pytest.mark.asyncio
async def test_get_inventory_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.community.get_inventory(steamid=steamid)
        assert model.assets is not None


@pytest.mark.asyncio
async def test_get_profile_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.community.get_profile(steamid=steamid)
        assert model.profile.steam_id64 is not None
