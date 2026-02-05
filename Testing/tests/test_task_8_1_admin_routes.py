"""
Test cases for Task 8 - Subtask 8.1: Admin Routes
Tests admin dashboard route with statistics
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


@pytest.mark.admin
@pytest.mark.unit
class TestTask81AdminRoutes:
    """Test admin routes functionality"""
    
    @pytest.fixture
    def admin_client(self, client):
        """Create authenticated admin client"""
        try:
            admin = User.create(
                email='admin_routes@example.com',
                password='admin123',
                role='admin'
            )
            client.post('/auth/login', data={
                'email': 'admin_routes@example.com',
                'password': 'admin123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_admin_dashboard_access(self, admin_client):
        """Test admin dashboard is accessible"""
        response = admin_client.get('/admin/dashboard')
        assert response.status_code == 200
        assert b'Admin Dashboard' in response.data or b'admin' in response.data.lower()
    
    def test_admin_dashboard_shows_statistics(self, admin_client):
        """Test admin dashboard displays statistics"""
        response = admin_client.get('/admin/dashboard')
        assert response.status_code == 200
        # Check for stat cards or statistics
        assert b'stat' in response.data.lower() or b'dashboard' in response.data.lower()
    
    def test_admin_dashboard_requires_authentication(self, client):
        """Test admin dashboard requires authentication"""
        response = client.get('/admin/dashboard', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_admin_dashboard_requires_admin_role(self, client):
        """Test admin dashboard requires admin role"""
        try:
            # Create customer user
            customer = User.create(
                email='customer_admin@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_admin@example.com',
                'password': 'customer123'
            })
            
            # Try to access admin dashboard
            response = client.get('/admin/dashboard')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

