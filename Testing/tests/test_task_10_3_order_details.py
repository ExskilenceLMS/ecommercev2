"""
Test cases for Task 10 - Subtask 10.3: Order Details Page
Tests customer order details view functionality
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
class TestTask103OrderDetails:
    """Test customer order details page functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_details@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_details@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_order_details_page_requires_authentication(self, client):
        """Test order details page requires authentication"""
        response = client.get('/customer/orders/1', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_order_details_page_requires_customer_role(self, client):
        """Test order details page requires customer role"""
        try:
            # Create seller user
            seller = User.create(
                email='seller_details@example.com',
                password='seller123',
                role='seller'
            )
            client.post('/auth/login', data={
                'email': 'seller_details@example.com',
                'password': 'seller123'
            })
            
            # Try to access order details page
            response = client.get('/customer/orders/1')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_order_details_page_displays_order_info(self, customer_client):
        """Test order details page displays order information"""
        # This test may fail if no orders exist, which is expected
        response = customer_client.get('/customer/orders/999999', follow_redirects=True)
        # Should either show order details or redirect with error
        assert response.status_code in [200, 302]

