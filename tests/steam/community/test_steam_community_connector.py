import pytest
import os
from httpx import HTTPStatusError

from connector.steam import SteamConnector


@pytest.mark.asyncio
async def test_get_market_page_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.community.get_market_page(start=0, count=10)
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
        model = await connector.community.get_market_listings(
            market_hash_name="Kilowatt Case"
        )
        assert model.success is not None


@pytest.mark.asyncio
async def test_get_partner_inventory_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.community.get_partner_inventory(steamid=steamid)
        assert model.success is not None


@pytest.mark.asyncio
async def test_get_partner_inventory_integration_many_items():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198209388244")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.community.get_partner_inventory(steamid=steamid)
        assert model.success is not None


@pytest.mark.asyncio
async def test_get_priceoverview_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198209388244")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username,
        password=password,
        api_key=api_key,
    ) as connector:
        model = await connector.community.get_priceoverview(
            market_hash_name="Shadow Case"
        )
        assert model.success


@pytest.mark.asyncio
async def test_get_priceoverview_integration_invalid():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username,
        password=password,
        api_key=api_key,
    ) as connector:
        model = await connector.community.get_priceoverview(
            market_hash_name="Invalid Item"
        )
        assert model.success
