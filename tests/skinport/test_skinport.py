import pytest

from connector.skinport.connector import SkinportConnector

@pytest.mark.asyncio
async def test_skinport_integration():
    connector = SkinportConnector()
    resp = await connector.get_items()
    model = resp.model()
    assert model.root is None or isinstance(model.root, list) 