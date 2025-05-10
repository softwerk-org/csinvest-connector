import pytest

from connector.marketcsgo.connector import MarketCsgoConnector

@pytest.mark.asyncio
async def test_marketcsgo_integration():
    connector = MarketCsgoConnector()
    model = await connector.get_prices()
    assert hasattr(model, "items")
    assert model.items is None or isinstance(model.items, list) 