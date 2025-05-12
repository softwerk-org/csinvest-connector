import pytest
from connector.csfloat.connector import CSFloatConnector


@pytest.mark.asyncio
async def test_get_float_prices_integration():
    connector = CSFloatConnector()
    model = await connector.get_listings()
    assert model[0] is not None
