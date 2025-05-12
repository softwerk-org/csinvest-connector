import os
import pytest

from connector.marketcsgo.connector import MarketCsgoConnector


@pytest.mark.asyncio
async def test_marketcsgo_integration():
    connector = MarketCsgoConnector()
    model = await connector.get_prices()
    assert model.items is not None


@pytest.mark.asyncio
async def test_marketcsgo_integration_list_items_info():
    key = os.getenv("MARKETCSGO_API_KEY")
    if not key:
        pytest.skip("MARKETCSGO_API_KEY required for integration tests")
    connector = MarketCsgoConnector(api_key=key)
    model = await connector.get_list_items_info(["AK-47 | Redline (Minimal Wear)"])
    assert model.success is True
    assert model.data is not None
