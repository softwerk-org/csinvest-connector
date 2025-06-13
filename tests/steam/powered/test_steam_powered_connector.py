import pprint
import httpx
import pytest
import os

from connector.steam import SteamConnector


@pytest.mark.asyncio
async def test_get_player_summaries_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username,
        password=password,
        api_key=api_key,
    ) as connector:
        try:
            model = await connector.powered.get_player_summaries(steamid)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                pytest.skip("Sorry this endpoint just sucks")
            raise e

    assert model.response.players is not None


@pytest.mark.asyncio
async def test_get_asset_class_info_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.powered.get_asset_class_info("506853905")
    assert model.result is not None


@pytest.mark.asyncio
async def test_multiple_asset_class_info_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.powered.get_asset_class_info(["506853905", "506853387"])
    assert model.result is not None
    assert len(model.result.items()) == 2


@pytest.mark.asyncio
async def test_multiple_tuple_asset_class_info_integration():
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    if not username or not password or not api_key:
        pytest.skip("Steam credentials required for integration tests")
    async with SteamConnector(
        username=username, password=password, api_key=api_key
    ) as connector:
        model = await connector.powered.get_asset_class_info(("506853905", "506853387"))
    assert model.result is not None
    assert len(model.result.items()) == 2
