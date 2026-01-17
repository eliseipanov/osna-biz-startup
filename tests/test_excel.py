import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
from core.utils.excel_manager import import_products_from_excel_sync

def test_excel_import_validates_name_required():
    """Test that Excel import validates name is required."""
    # Create test Excel data with empty name
    data = {
        'name': [''],
        'price': [10.0],
        'unit': ['kg'],
        'sku': ['TEST001']
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)

        mock_session = MagicMock()
        mock_session.begin_nested.return_value.__enter__.return_value = mock_session
        mock_session.commit = MagicMock()

        with pytest.raises(Exception) as exc_info:
            import_products_from_excel_sync(mock_session, tmp.name)

        assert "Name cannot be empty" in str(exc_info.value)

        os.unlink(tmp.name)

def test_excel_import_validates_price_not_negative():
    """Test that Excel import validates price is not negative."""
    data = {
        'name': ['Test Product'],
        'price': [-5.0],
        'unit': ['kg'],
        'sku': ['TEST001']
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)

        mock_session = MagicMock()
        mock_session.begin_nested.return_value.__enter__.return_value = mock_session
        mock_session.commit = MagicMock()

        with pytest.raises(Exception) as exc_info:
            import_products_from_excel_sync(mock_session, tmp.name)

        assert "Price cannot be negative" in str(exc_info.value)

        os.unlink(tmp.name)

def test_excel_import_validates_unit_required():
    """Test that Excel import validates unit is required."""
    data = {
        'name': ['Test Product'],
        'price': [10.0],
        'unit': [''],
        'sku': ['TEST001']
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)

        mock_session = MagicMock()
        mock_session.begin_nested.return_value.__enter__.return_value = mock_session
        mock_session.commit = MagicMock()

        with pytest.raises(Exception) as exc_info:
            import_products_from_excel_sync(mock_session, tmp.name)

        assert "Unit cannot be empty" in str(exc_info.value)

        os.unlink(tmp.name)

def test_excel_import_validates_sku_length():
    """Test that Excel import validates SKU length <= 50 characters."""
    long_sku = 'A' * 51  # 51 characters
    data = {
        'name': ['Test Product'],
        'price': [10.0],
        'unit': ['kg'],
        'sku': [long_sku]
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)

        mock_session = MagicMock()
        mock_session.begin_nested.return_value.__enter__.return_value = mock_session
        mock_session.commit = MagicMock()

        with pytest.raises(Exception) as exc_info:
            import_products_from_excel_sync(mock_session, tmp.name)

        assert "SKU cannot be longer than 50 characters" in str(exc_info.value)

        os.unlink(tmp.name)

def test_excel_import_valid_data_success():
    """Test that Excel import succeeds with valid data."""
    data = {
        'name': ['Test Product'],
        'price': [10.0],
        'unit': ['kg'],
        'sku': ['TEST001']
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)

        mock_session = MagicMock()
        mock_session.begin_nested.return_value.__enter__.return_value = mock_session
        mock_session.commit = MagicMock()
        mock_session.execute.return_value.scalar_one_or_none.return_value = None  # No existing product
        mock_session.add = MagicMock()

        result = import_products_from_excel_sync(mock_session, tmp.name)

        assert "Import successful" in result
        assert "1 rows processed" in result

        os.unlink(tmp.name)

def test_excel_import_handles_missing_file():
    """Test that Excel import handles missing file gracefully."""
    mock_session = MagicMock()

    with pytest.raises(FileNotFoundError):
        import_products_from_excel_sync(mock_session, 'nonexistent_file.xlsx')