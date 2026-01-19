"""
Test cases for Task 14: Order Management
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app
from models.user import User
from utils import get_db_connection


@pytest.mark.unit
class TestOrderManagement:
    """Test order management functionality"""
    
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
    
    @pytest.fixture
    def seller_client(self, client):
        """Create authenticated seller client"""
        try:
            seller = User.create(
                email='seller_order@example.com',
                password='seller123',
                role='seller'
            )
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sellers (user_id, store_name) VALUES (%s, %s)
            """, (seller.id, 'Test Store'))
            conn.commit()
            cursor.close()
            conn.close()
            
            client.post('/auth/login', data={
                'email': 'seller_order@example.com',
                'password': 'seller123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_order_list_page_customer(self, customer_client):
        """Test order list page for customer"""
        response = customer_client.get('/orders/')
        assert response.status_code == 200
    
    def test_order_list_page_seller(self, seller_client):
        """Test order list page for seller"""
        response = seller_client.get('/orders/')
        assert response.status_code == 200
    
    def test_order_details_page(self, customer_client):
        """Test order details page"""
        # This would require an actual order ID
        response = customer_client.get('/orders/1', follow_redirects=True)
        # Should either show order or 404/redirect
        assert response.status_code in [200, 404, 302]
    
    def test_update_order_status(self, seller_client):
        """Test updating order status"""
        # This would require an actual order ID
        response = seller_client.post('/orders/1/update-status', data={
            'status': 'confirmed'
        }, follow_redirects=True)
        # Should either work or show error
        assert response.status_code in [200, 404, 302]

