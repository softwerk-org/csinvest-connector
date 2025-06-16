import pytest
import os

from connector.dmarket.connector import DMarketConnector


@pytest.mark.asyncio
async def test_get_last_sales_integration():
    pub = os.getenv("DMARKET_PUBLIC_KEY")
    priv = os.getenv("DMARKET_PRIVATE_KEY")
    if not pub or not priv:
        pytest.skip(
            "DMARKET_PUBLIC_KEY and DMARKET_PRIVATE_KEY required for integration tests"
        )
    async with DMarketConnector(public_key=pub, private_key=priv) as connector:
        model = await connector.get_last_sales(market_hash_name="Kilowatt Case")
    assert hasattr(model, "sales")


@pytest.mark.asyncio
async def test_get_market_items_integration():
    pub = os.getenv("DMARKET_PUBLIC_KEY")
    priv = os.getenv("DMARKET_PRIVATE_KEY")
    if not pub or not priv:
        pytest.skip(
            "DMARKET_PUBLIC_KEY and DMARKET_PRIVATE_KEY required for integration tests"
        )
    async with DMarketConnector(public_key=pub, private_key=priv) as connector:
        model = await connector.get_market_items("Kilowatt Case")
    assert model.total is not None


@pytest.mark.asyncio
async def test_get_aggregated_prices_integration():
    pub = os.getenv("DMARKET_PUBLIC_KEY")
    priv = os.getenv("DMARKET_PRIVATE_KEY")
    if not pub or not priv:
        pytest.skip(
            "DMARKET_PUBLIC_KEY and DMARKET_PRIVATE_KEY required for integration tests"
        )
    async with DMarketConnector(public_key=pub, private_key=priv) as connector:
        model = await connector.get_aggregated_prices(["Kilowatt Case"])
    assert model.aggregated_titles is not None


@pytest.mark.asyncio
async def test_get_avg_sales_graph_integration():
    async with DMarketConnector() as connector:
        model = await connector.get_avg_sales_graph(
            title="★ Driver Gloves | Crimson Weave (Minimal Wear)", period="1Y"
        )
    assert hasattr(model, "totalSales")
    assert hasattr(model, "date")
    assert hasattr(model, "avgPrice")
    assert len(model.totalSales) > 0
    assert len(model.date) > 0
    assert len(model.avgPrice) > 0
