import os
import pytest
from connector.csfloat.connector import CSFloatConnector


@pytest.mark.asyncio
async def test_get_float_prices_integration():
    key = os.getenv("CSFLOAT_API_KEY")
    if not key:
        pytest.skip("CSFLOAT_API_KEY required for integration tests")
    connector = CSFloatConnector(api_key=key)
    model = await connector.get_listings()
    assert model[0] is not None
