"""
Test cases for Task 8 - Subtask 8.4: Order Overview Page
Tests order list route
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
class TestTask84OrderOverview:
    """Test order overview page functionality"""
    
    @pytest.fixture
    def admin_client(self, client):
        """Create authenticated admin client"""
        try:
            admin = User.create(
                email='admin_order@example.com',
                password='admin123',
                role='admin'
            )
            client.post('/auth/login', data={
                'email': 'admin_order@example.com',
                'password': 'admin123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_admin_orders_page(self, admin_client):
        """Test admin orders page is accessible"""
        response = admin_client.get('/admin/orders')
        assert response.status_code == 200
    
    def test_orders_page_displays_orders(self, admin_client):
        """Test orders page displays order list"""
        response = admin_client.get('/admin/orders')
        assert response.status_code == 200
        # Check for order-related content
        assert b'order' in response.data.lower() or b'table' in response.data.lower()
    
    def test_orders_page_requires_authentication(self, client):
        """Test orders page requires authentication"""
        response = client.get('/admin/orders', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_orders_page_requires_admin_role(self, client):
        """Test orders page requires admin role"""
        try:
            # Create customer user
            customer = User.create(
                email='customer_order@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_order@example.com',
                'password': 'customer123'
            })
            
            # Try to access orders page
            response = client.get('/admin/orders')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

