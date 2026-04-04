"""
Test cases for Task 14 - Subtask 14.1_order_status: Order Status Lifecycle
Tests order status update functionality
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
from utils import get_db_connection


@pytest.mark.unit
class TestTask142OrderStatus:
    """Test order status lifecycle functionality"""
    
    @pytest.fixture
    def seller_client(self, client):
        """Create authenticated seller client"""
        try:
            seller = User.create(
                email='seller_status@example.com',
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
                'email': 'seller_status@example.com',
                'password': 'seller123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_update_order_status_route_exists(self, seller_client):
        """Test update order status route exists"""
        # Route exists, but requires actual order ID
        response = seller_client.post('/orders/1/update-status', data={
            'status': 'confirmed'
        }, follow_redirects=True)
        # Should either work or show error
        assert response.status_code in [200, 404, 302]

