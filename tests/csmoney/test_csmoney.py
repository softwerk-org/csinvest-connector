import pytest
from connector.csmoney.connector import CSMoneyConnector


@pytest.mark.asyncio
async def test_get_min_prices_integration():
    async with CSMoneyConnector() as connector:
        model = await connector.get_min_prices()
    assert model is not None
