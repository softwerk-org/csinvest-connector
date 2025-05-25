import os
import pytest

from connector.gamerpaygg.connector import GamerPayGgConnector


@pytest.mark.asyncio
async def test_gamerpaygg_integration_prices():
    async with GamerPayGgConnector() as connector:
        model = await connector.get_prices()
    assert isinstance(model, list)


@pytest.mark.asyncio
async def test_gamerpaygg_integration_sales():
    key = os.getenv("GAMERPAYGG_API_KEY")
    if not key:
        pytest.skip("GAMERPAYGG_API_KEY required for integration tests")
    async with GamerPayGgConnector(api_key=key) as connector:
        model = await connector.get_sales()
    assert isinstance(model, dict)
