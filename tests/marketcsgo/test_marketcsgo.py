import pytest

from connector.marketcsgo.connector import MarketCsgoConnector

@pytest.mark.asyncio
async def test_marketcsgo_integration():
    connector = MarketCsgoConnector()
    resp = await connector.get_prices()
    model = resp.model()
    assert hasattr(model, "items")
    assert model.items is None or isinstance(model.items, list) 