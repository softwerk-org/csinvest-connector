import pytest

from connector.skinport.connector import SkinportConnector


@pytest.mark.asyncio
async def test_skinport_integration():
    connector = SkinportConnector()
    model = await connector.get_items()
    assert isinstance(model, list)


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_one():
    connector = SkinportConnector()
    model = await connector.get_sales_history(["Snakebite Case"])
    assert isinstance(model, list)
    assert model[0] is not None


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_multiple():
    connector = SkinportConnector()
    model = await connector.get_sales_history(["Snakebite Case", "Revolution Case"])
    assert isinstance(model, list)
    assert model[0] is not None


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_all():
    connector = SkinportConnector()
    model = await connector.get_sales_history()
    assert isinstance(model, list)
    assert model[0] is not None
