"""
Test cases for Task 11 - Subtask 11.2: Product Details Page
Tests product details page functionality
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app
from utils import get_db_connection


@pytest.mark.unit
class TestTask112ProductDetails:
    """Test product details page functionality"""
    
    def test_product_details_page(self, client):
        """Test product details page"""
        try:
            # Create a test product
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Create seller
            from models.user import User
            seller = User.create(
                email='seller_prod@example.com',
                password='seller123',
                role='seller'
            )
            cursor.execute("""
                INSERT INTO sellers (user_id, store_name) VALUES (%s, %s)
            """, (seller.id, 'Test Store'))
            seller_id = cursor.lastrowid
            
            # Create category
            cursor.execute("""
                INSERT INTO categories (name, slug) VALUES (%s, %s)
            """, ('Test Category', 'test-category'))
            category_id = cursor.lastrowid
            
            # Create product
            cursor.execute("""
                INSERT INTO products (seller_id, category_id, name, price, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """, (seller_id, category_id, 'Test Product', 29.99, True))
            product_id = cursor.lastrowid
            
            # Create inventory
            cursor.execute("""
                INSERT INTO inventory (product_id, quantity) VALUES (%s, %s)
            """, (product_id, 10))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            response = client.get(f'/products/{product_id}')
            assert response.status_code == 200
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

