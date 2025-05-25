import os
import pytest
from connector.csfloat.connector import CSFloatConnector


@pytest.mark.asyncio
async def test_get_float_prices_integration():
    key = os.getenv("CSFLOAT_API_KEY")
    if not key:
        pytest.skip("CSFLOAT_API_KEY required for integration tests")
    async with CSFloatConnector(api_key=key) as connector:
        model = await connector.get_listings()
    assert model.data[0] is not None


@pytest.mark.asyncio
async def test_get_similar_listings_integration():
    key = os.getenv("CSFLOAT_API_KEY")
    if not key:
        pytest.skip("CSFLOAT_API_KEY required for integration tests")
    async with CSFloatConnector(api_key=key) as connector:
        similar = await connector.get_similar_listings("840883240658144975")
    assert isinstance(similar, list)
    assert similar and similar[0] is not None


@pytest.mark.asyncio
async def test_get_history_graph_integration():
    key = os.getenv("CSFLOAT_API_KEY")
    if not key:
        pytest.skip("CSFLOAT_API_KEY required for integration tests")
    async with CSFloatConnector(api_key=key) as connector:
        history = await connector.get_history_graph("AK-47 | Hydroponic (Factory New)")
    assert isinstance(history, list)
    assert history and hasattr(history[0], "count") and hasattr(history[0], "avg_price")
