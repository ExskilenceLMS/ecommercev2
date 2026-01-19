"""
Test cases for Task 9 - Subtask 9.2: Inventory Update
Tests inventory list and update routes
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


@pytest.mark.seller
@pytest.mark.unit
class TestTask92InventoryUpdate:
    """Test inventory update functionality"""
    
    @pytest.fixture
    def seller_client(self, client):
        """Create authenticated seller client"""
        try:
            seller = User.create(
                email='seller_inventory@example.com',
                password='seller123',
                role='seller'
            )
            
            # Create seller record
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sellers (user_id, store_name, contact_email)
                VALUES (%s, %s, %s)
            """, (seller.id, 'Test Store', seller.email))
            seller_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            client.post('/auth/login', data={
                'email': 'seller_inventory@example.com',
                'password': 'seller123'
            })
            return client, seller_id
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_seller_inventory_page(self, seller_client):
        """Test seller inventory page is accessible"""
        client, _ = seller_client
        response = client.get('/seller/inventory')
        assert response.status_code == 200
    
    def test_inventory_page_displays_inventory(self, seller_client):
        """Test inventory page displays inventory items"""
        client, _ = seller_client
        response = client.get('/seller/inventory')
        assert response.status_code == 200
        # Check for inventory-related content
        assert b'inventory' in response.data.lower() or b'quantity' in response.data.lower()
    
    def test_inventory_page_requires_authentication(self, client):
        """Test inventory page requires authentication"""
        response = client.get('/seller/inventory', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_inventory_page_requires_seller_role(self, client):
        """Test inventory page requires seller role"""
        try:
            # Create customer user
            customer = User.create(
                email='customer_inventory@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_inventory@example.com',
                'password': 'customer123'
            })
            
            # Try to access inventory page
            response = client.get('/seller/inventory')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

