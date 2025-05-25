import pytest

from connector.skinport.official.connector import SkinportOfficialConnector


@pytest.mark.asyncio
async def test_skinport_integration():
    async with SkinportOfficialConnector() as connector:
        model = await connector.get_items()
    assert isinstance(model, list)


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_one():
    async with SkinportOfficialConnector() as connector:
        model = await connector.get_sales_history_agg(["Snakebite Case"])
    assert model[0] is not None


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_multiple():
    async with SkinportOfficialConnector() as connector:
        model = await connector.get_sales_history_agg(
            ["Snakebite Case", "Revolution Case"]
        )
    assert isinstance(model, list)
    assert model[0] is not None


@pytest.mark.asyncio
async def test_skinport_integration_sales_history_all():
    async with SkinportOfficialConnector() as connector:
        model = await connector.get_sales_history_agg()
    assert isinstance(model, list)
    assert model[0] is not None
