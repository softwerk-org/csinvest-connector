import os
import pytest
from connector.csmoney.connector import CSMoneyConnector


@pytest.mark.asyncio
async def test_get_min_prices_integration():
    flaresolverr_url = os.getenv("FLARESOLVERR_URL")
    if not flaresolverr_url:
        pytest.skip("FLARESOLVERR_URL is not set")
    async with CSMoneyConnector(
        flaresolverr_url=flaresolverr_url,
    ) as connector:
        model = await connector.get_min_prices()
    assert model is not None
