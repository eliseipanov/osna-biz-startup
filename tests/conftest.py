import pytest
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set up environment variables for testing
os.environ.setdefault('SECRET_KEY', 'test_secret_key_for_testing_only_not_secure')

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    from admin.app import app as flask_app
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test_secret_key'
    flask_app.config['WTF_CSRF_ENABLED'] = True
    return flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()