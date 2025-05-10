import pytest

from connector.openerapi.connector import OpenExchangeRatesConnector

@pytest.mark.asyncio
async def test_openerapi_integration():
    connector = OpenExchangeRatesConnector()
    model = await connector.get_latest_rates()
    assert model.base_code is not None 