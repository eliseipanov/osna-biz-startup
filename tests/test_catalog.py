import pytest
from unittest.mock import AsyncMock, patch
from bot.handlers.catalog import catalog_handler
from aiogram.types import Message
from core.models import AvailabilityStatus

@pytest.mark.asyncio
async def test_catalog_handler_shows_only_in_stock_products():
    """Test that catalog handler only shows products with IN_STOCK availability."""
    # Mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    # Mock products - one IN_STOCK, one OUT_OF_STOCK
    mock_product_in_stock = AsyncMock()
    mock_product_in_stock.name = "Test Product In Stock"
    mock_product_in_stock.price = 10.0
    mock_product_in_stock.unit = "kg"

    mock_product_out = AsyncMock()
    mock_product_out.name = "Test Product Out"
    mock_product_out.price = 15.0
    mock_product_out.unit = "kg"

    # Mock session and query
    mock_session = AsyncMock()
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = [mock_product_in_stock]  # Only IN_STOCK product
    mock_session.scalars.return_value = mock_scalars

    with patch('bot.handlers.catalog.async_session') as mock_async_session:
        mock_async_session.return_value.__aenter__.return_value = mock_session

        await catalog_handler(mock_message)

        # Verify the query was called with correct filter
        mock_session.scalars.assert_called_once()
        call_args = mock_session.scalars.call_args[0][0]
        # The query should filter by availability_status == IN_STOCK
        assert str(call_args).find('availability_status') != -1
        assert str(call_args).find('IN_STOCK') != -1

        # Verify message was sent with product info
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Test Product In Stock" in call_args
        assert "10,0 €/kg" in call_args

@pytest.mark.asyncio
async def test_catalog_handler_handles_database_error():
    """Test that catalog handler gracefully handles database errors."""
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    with patch('bot.handlers.catalog.async_session') as mock_async_session:
        mock_async_session.return_value.__aenter__.side_effect = Exception("Database connection failed")

        await catalog_handler(mock_message)

        # Verify error message was sent
        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Сталася помилка при завантаженні каталогу" in call_args

@pytest.mark.asyncio
async def test_catalog_handler_empty_catalog():
    """Test catalog handler when no products are available."""
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()

    mock_session = AsyncMock()
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = []  # No products
    mock_session.scalars.return_value = mock_scalars

    with patch('bot.handlers.catalog.async_session') as mock_async_session:
        mock_async_session.return_value.__aenter__.return_value = mock_session

        await catalog_handler(mock_message)

        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args[0][0]
        assert "Каталог порожній" in call_args