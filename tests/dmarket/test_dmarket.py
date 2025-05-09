import pytest
import os

from connector.dmarket.connector import DMarketConnector

@pytest.mark.asyncio
async def test_get_last_sales_integration():
    pub = os.getenv("DMARKET_PUBLIC_KEY")
    priv = os.getenv("DMARKET_PRIVATE_KEY")
    if not pub or not priv:
        pytest.skip("DMARKET_PUBLIC_KEY and DMARKET_PRIVATE_KEY required for integration tests")
    connector = DMarketConnector(public_key=pub, private_key=priv)
    resp = await connector.get_last_sales("Kilowatt Case", "Offer")
    model = resp.model()
    assert hasattr(model, "sales")

@pytest.mark.asyncio
async def test_get_market_items_integration():
    pub = os.getenv("DMARKET_PUBLIC_KEY")
    priv = os.getenv("DMARKET_PRIVATE_KEY")
    if not pub or not priv:
        pytest.skip("DMARKET_PUBLIC_KEY and DMARKET_PRIVATE_KEY required for integration tests")
    connector = DMarketConnector(public_key=pub, private_key=priv)
    resp = await connector.get_market_items("Kilowatt Case")
    model = resp.model()
    assert model.total is not None

@pytest.mark.asyncio
async def test_get_aggregated_prices_integration():
    pub = os.getenv("DMARKET_PUBLIC_KEY")
    priv = os.getenv("DMARKET_PRIVATE_KEY")
    if not pub or not priv:
        pytest.skip("DMARKET_PUBLIC_KEY and DMARKET_PRIVATE_KEY required for integration tests")
    connector = DMarketConnector(public_key=pub, private_key=priv)
    resp = await connector.get_aggregated_prices(["Kilowatt Case"])
    model = resp.model()
    assert model.AggregatedTitles is not None
