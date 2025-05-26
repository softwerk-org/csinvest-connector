import os
import pytest

from connector.whitemarket.connector import WhiteMarketConnector
from connector.whitemarket.models.get_prices import Prices
from connector.whitemarket.models.get_history import SalesHistoryResponse, HistoryEntry


@pytest.mark.asyncio
async def test_get_listings_integration():
    async with WhiteMarketConnector() as connector:
        result = await connector.get_prices()
    assert isinstance(result, Prices)
    assert result.root, "Expected non-empty price list"
    first = result.root[0]
    assert hasattr(first, "market_hash_name")
    assert hasattr(first, "price")
    assert hasattr(first, "market_product_link")


@pytest.mark.asyncio
async def test_get_sales_history_integration():
    async with WhiteMarketConnector() as connector:
        resp = await connector.get_sales_history("AK-47 | Redline (Field-Tested)")
    assert isinstance(resp, SalesHistoryResponse)
    history = resp.data.market_stats_product
    assert isinstance(history, list)
    assert history, "Expected at least one history record"
    entry = history[0]
    assert isinstance(entry, HistoryEntry)
    assert hasattr(entry, "priceAvg")
    assert hasattr(entry, "volume")
    assert hasattr(entry, "date")
