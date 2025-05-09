import pytest

from connector.gamerpaygg.connector import GamerPayGgConnector

@pytest.mark.asyncio
async def test_gamerpaygg_integration():
    connector = GamerPayGgConnector()
    resp = await connector.get_prices()
    model = resp.model()
    assert hasattr(model, "root")
    assert model.root is None or isinstance(model.root, list) 