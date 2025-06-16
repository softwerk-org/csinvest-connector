import os
import pytest
from connector.csmoney.connector import CSMoneyConnector


@pytest.mark.asyncio
async def test_get_min_prices_integration():
    async with CSMoneyConnector() as connector:
        model = await connector.get_min_prices()
    assert model is not None


@pytest.mark.asyncio
async def test_get_price_trader_log_integration():
    async with CSMoneyConnector() as connector:
        model = await connector.get_price_trader_log([5002, 12611])
    assert model.data is not None
    assert hasattr(model.data, "price_trader_log")
    assert len(model.data.price_trader_log) > 0
    for item in model.data.price_trader_log:
        assert hasattr(item, "name_id")
        assert hasattr(item, "values")
        if item.values:
            assert hasattr(item.values[0], "price_trader_new")
            assert hasattr(item.values[0], "time")
