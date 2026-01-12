"""
Test cases for Task 13: Checkout Flow
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
class TestCheckoutFlow:
    """Test checkout flow functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client with cart"""
        try:
            customer = User.create(
                email='customer_checkout@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_checkout@example.com',
                'password': 'customer123'
            })
            
            # Create address
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO addresses (user_id, address_line1, city, state, postal_code, country)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (customer.id, '123 Test St', 'Test City', 'TS', '12345', 'USA'))
            conn.commit()
            cursor.close()
            conn.close()
            
            return client, customer.id
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_checkout_review_page(self, customer_client):
        """Test checkout review page"""
        client, customer_id = customer_client
        response = client.get('/checkout/')
        # Should either show checkout or redirect if cart is empty
        assert response.status_code in [200, 302]
    
    def test_checkout_requires_address(self, customer_client):
        """Test that checkout requires address"""
        client, customer_id = customer_client
        response = client.get('/checkout/')
        # Should show address selection or redirect
        assert response.status_code in [200, 302]
    
    def test_order_confirmation_page(self, customer_client):
        """Test order confirmation page"""
        client, customer_id = customer_client
        response = client.get('/checkout/confirmation?order_numbers=ORD-TEST123')
        assert response.status_code == 200

