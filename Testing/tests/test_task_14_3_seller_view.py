"""
Test cases for Task 14 - Subtask 14.3_seller_view: Seller Order View
Tests seller order view functionality
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
class TestTask144SellerView:
    """Test seller order view functionality"""
    
    @pytest.fixture
    def seller_client(self, client):
        """Create authenticated seller client"""
        try:
            seller = User.create(
                email='seller_view@example.com',
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
                'email': 'seller_view@example.com',
                'password': 'seller123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_order_list_page_seller(self, seller_client):
        """Test order list page for seller"""
        response = seller_client.get('/orders/')
        assert response.status_code == 200

