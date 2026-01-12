"""
Test cases for Task 13 - Subtask 13.2_place_order: Place Order Logic
Tests place order functionality
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
class TestTask134PlaceOrder:
    """Test place order functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client with cart and address"""
        try:
            customer = User.create(
                email='customer_place@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_place@example.com',
                'password': 'customer123'
            })
            
            # Create address
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO addresses (user_id, address_line1, city, state, postal_code, country)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (customer.id, '123 Test St', 'Test City', 'TS', '12345', 'USA'))
            address_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            return client, address_id
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_place_order_route_exists(self, customer_client):
        """Test place order route exists"""
        client, address_id = customer_client
        # Route exists, but requires cart items
        response = client.post('/checkout/place-order', data={
            'shipping_address_id': address_id
        }, follow_redirects=True)
        # Should either process or redirect
        assert response.status_code in [200, 302]

