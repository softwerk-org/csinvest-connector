import pytest

from connector.skinport.connector import SkinportConnector


@pytest.mark.asyncio
async def test_skinport_integration():
    connector = SkinportConnector()
    model = await connector.get_items()
    assert model.root is None or isinstance(model.root, list)


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_one():
    connector = SkinportConnector()
    model = await connector.get_sales_history(["Snakebite Case"])
    assert model.success is True
    assert model.response is not None


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_multiple():
    connector = SkinportConnector()
    model = await connector.get_sales_history(["Snakebite Case", "Revolution Case"])
    assert model.success is True
    assert model.response is not None


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_all():
    connector = SkinportConnector()
    model = await connector.get_sales_history()
    assert model.success is True
    assert model.response is not None
