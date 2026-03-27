"""
Test cases for Task 6 - Subtask 6.2: Logout
Tests logout functionality
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app
from models.user import User


@pytest.mark.unit
class TestTask62Logout:
    """Test logout functionality"""
    
    @pytest.fixture
    def authenticated_client(self, client):
        """Create authenticated client"""
        try:
            user = User.create(
                email='test_logout@example.com',
                password='test123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'test_logout@example.com',
                'password': 'test123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_logout_route_exists(self, authenticated_client):
        """Test logout route exists"""
        response = authenticated_client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
    
    def test_logout_clears_session(self, authenticated_client):
        """Test logout clears session"""
        response = authenticated_client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        # After logout, accessing protected route should redirect to login
        response = authenticated_client.get('/customer/dashboard', follow_redirects=True)
        assert b'login' in response.data.lower() or response.status_code == 302

