import pytest
import os
from httpx import HTTPStatusError

from connector.steam.community.connector import SteamCommunityConnector

@pytest.mark.asyncio
async def test_get_market_listings_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    connector = SteamCommunityConnector(username=username, password=password, api_key=api_key)
    resp = await connector.get_market_listings(start=0, count=10)
    model = resp.model()
    assert model.success is not None

@pytest.mark.asyncio
async def test_get_pricehistory_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    connector = SteamCommunityConnector(username=username, password=password, api_key=api_key)
    try:
        resp = await connector.get_pricehistory(market_hash_name="Kilowatt Case")
    except HTTPStatusError as e:
        if e.response.status_code == 500:
            pytest.skip("Internal server error from Steam, skipping integration test")
        raise
    model = resp.model()
    assert model.prices is not None

@pytest.mark.asyncio
async def test_get_inventory_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    connector = SteamCommunityConnector(username=username, password=password, api_key=api_key)
    resp = await connector.get_inventory(steamid=steamid)
    model = resp.model()
    assert model.assets is not None

@pytest.mark.asyncio
async def test_get_profile_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    connector = SteamCommunityConnector(username=username, password=password, api_key=api_key)
    resp = await connector.get_profile(steamid=steamid)
    model = resp.model()
    assert model.profile.steam_id64 is not None 