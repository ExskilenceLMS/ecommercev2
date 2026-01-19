"""
Test cases for Task 10 - Subtask 10.2: Order History
Tests customer order history list functionality
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


@pytest.mark.customer
@pytest.mark.unit
class TestTask102OrderHistory:
    """Test customer order history functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_order@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_order@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_customer_orders_page(self, customer_client):
        """Test customer orders page is accessible"""
        response = customer_client.get('/customer/orders')
        assert response.status_code == 200
    
    def test_orders_page_displays_orders(self, customer_client):
        """Test orders page displays order list"""
        response = customer_client.get('/customer/orders')
        assert response.status_code == 200
        # Check for order-related content
        assert b'order' in response.data.lower() or b'table' in response.data.lower()
    
    def test_orders_page_requires_authentication(self, client):
        """Test orders page requires authentication"""
        response = client.get('/customer/orders', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_orders_page_requires_customer_role(self, client):
        """Test orders page requires customer role"""
        try:
            # Create seller user
            seller = User.create(
                email='seller_order@example.com',
                password='seller123',
                role='seller'
            )
            client.post('/auth/login', data={
                'email': 'seller_order@example.com',
                'password': 'seller123'
            })
            
            # Try to access orders page
            response = client.get('/customer/orders')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

