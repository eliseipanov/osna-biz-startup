import pytest
import os
from unittest.mock import patch, MagicMock
from admin.app import app

def test_app_debug_mode_disabled():
    """Test that Flask app runs without debug mode."""
    # The app.run call at the end has debug=False
    # We can't easily test the run call, but we can check the config
    assert app.config['DEBUG'] == False or 'DEBUG' not in app.config

def test_secret_key_from_env():
    """Test that SECRET_KEY is loaded from environment variable."""
    with patch.dict(os.environ, {'SECRET_KEY': 'test_secure_key_12345'}):
        # Reinitialize app to pick up env var
        from admin.app import app as test_app
        assert test_app.config['SECRET_KEY'] == 'test_secure_key_12345'

def test_max_content_length_set():
    """Test that file upload size limit is set to 5MB."""
    assert app.config['MAX_CONTENT_LENGTH'] == 5 * 1024 * 1024  # 5MB

def test_csrf_enabled():
    """Test that CSRF protection is enabled."""
    assert app.config.get('WTF_CSRF_ENABLED', True) == True

def test_login_rate_limiting_configured():
    """Test that rate limiting is configured on login route."""
    from admin.app import limiter
    assert limiter is not None

    # Check that login route has limiter decorator
    rules = limiter._rules
    login_limited = any('login' in str(rule) for rule in rules)
    assert login_limited

def test_file_upload_allowed_extensions():
    """Test that file upload fields have allowed extensions."""
    from admin.app import ProductView, CategoryView, FarmView

    # Check ProductView file upload
    product_form_extra = ProductView.form_extra_fields
    assert 'image_path' in product_form_extra
    image_field = product_form_extra['image_path']
    assert hasattr(image_field, 'allowed_extensions')
    assert 'jpg' in image_field.allowed_extensions
    assert 'png' in image_field.allowed_extensions
    assert 'gif' in image_field.allowed_extensions

    # Check CategoryView file upload
    category_form_extra = CategoryView.form_extra_fields
    assert 'image_path' in category_form_extra
    cat_image_field = category_form_extra['image_path']
    assert hasattr(cat_image_field, 'allowed_extensions')
    assert 'jpg' in cat_image_field.allowed_extensions

    # Check FarmView file upload
    farm_form_extra = FarmView.form_extra_fields
    assert 'image_path' in farm_form_extra
    farm_image_field = farm_form_extra['image_path']
    assert hasattr(farm_image_field, 'allowed_extensions')
    assert 'jpg' in farm_image_field.allowed_extensions

def test_admin_views_secure():
    """Test that admin views require authentication."""
    from admin.app import ProductView, UserView
    from flask_admin import Admin

    # Check that views inherit from SecureModelView
    assert issubclass(ProductView, app.view_functions.get('admin.index').view_class.__bases__[0].__bases__[0]) or 'SecureModelView' in str(ProductView.__bases__)

def test_login_route_exists():
    """Test that login route is properly configured."""
    with app.test_client() as client:
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data

def test_admin_logout_route_exists():
    """Test that logout route exists."""
    with app.test_client() as client:
        response = client.get('/admin/logout')
        # Should redirect to login since not authenticated
        assert response.status_code == 302