import pytest
from connector.csdeals.connector import CsDealsConnector

@pytest.mark.asyncio
async def test_get_lowest_prices_integration():
    # Integration test against real API
    connector = CsDealsConnector()
    resp = await connector.get_lowest_prices()
    model = resp.model()
    # Ensure Pydantic model is parsed successfully
    assert model.success is not None 