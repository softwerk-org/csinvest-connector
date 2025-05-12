import pytest

from connector.gamerpaygg.connector import GamerPayGgConnector


@pytest.mark.asyncio
async def test_gamerpaygg_integration_prices():
    connector = GamerPayGgConnector()
    model = await connector.get_prices()
    assert model.root is not None


@pytest.mark.asyncio
async def test_gamerpaygg_integration_sales():
    connector = GamerPayGgConnector()
    model = await connector.get_sales()
    assert model.root is not None
