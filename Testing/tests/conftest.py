"""
Shared pytest fixtures for all tests
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app, get_db_connection
from utils import set_db_connection_func

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['MYSQL_DB'] = 'ecommerce_test_db'
    
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def test_db():
    """Create test database connection"""
    # In tests, you might want to use a test database
    # For now, we'll use the same connection function
    return get_db_connection

@pytest.fixture
def auth_headers(client):
    """Helper to get auth headers after login"""
    def _login(email, password):
        response = client.post('/auth/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)
        return response
    return _login

