import pytest
import os

from connector.steam.powered.connector import SteamPoweredConnector


@pytest.mark.asyncio
async def test_get_player_summaries_integration():
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not api_key:
        pytest.skip("STEAM_WEBAPI_KEY required for integration tests")
    connector = SteamPoweredConnector(api_key=api_key)
    model = await connector.get_player_summaries(steamid)
    assert model.response.players is not None


@pytest.mark.asyncio
async def test_get_asset_class_info_integration():
    api_key = os.getenv("STEAM_WEBAPI_KEY")
    steamid = os.getenv("STEAM_TEST_ID", "76561198202508143")
    if not api_key:
        pytest.skip("STEAM_WEBAPI_KEY required for integration tests")
    connector = SteamPoweredConnector(api_key=api_key)
    model = await connector.get_asset_class_info(steamid)
    assert model.result is not None
