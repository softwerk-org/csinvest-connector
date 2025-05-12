import pytest
from connector.csdeals.connector import CsDealsConnector


@pytest.mark.asyncio
async def test_get_lowest_prices_integration():
    # Integration test against real API
    connector = CsDealsConnector()
    model = await connector.get_lowest_prices()
    # Ensure Pydantic model is parsed successfully
    assert model.success is not None


@pytest.mark.asyncio
async def test_get_sales_history_integration():
    connector = CsDealsConnector()
    model = await connector.get_sales_history(
        name="Revolution Case", appid=730, phase=None
    )
    # Ensure Pydantic model is parsed successfully
    assert model.success is not None


@pytest.mark.asyncio
async def test_get_sales_history_multi_integration_single_item():
    connector = CsDealsConnector()
    model = await connector.get_sales_history_multi(
        items=[{"name": "Revolution Case", "appid": 730, "phase": None}]
    )
    # Ensure Pydantic model is parsed successfully
    assert model.success is not None


@pytest.mark.asyncio
async def test_get_sales_history_multi_integration_multiple_items():
    connector = CsDealsConnector()
    model = await connector.get_sales_history_multi(
        items=[
            {"name": "Revolution Case", "appid": 730},
            {"name": "Recoil Case", "appid": 730},
            {"name": "SSG 08 | Blue Spruce (Field-Tested)", "appid": 730},
        ]
    )
    # Ensure Pydantic model is parsed successfully
    assert model.success is not None
