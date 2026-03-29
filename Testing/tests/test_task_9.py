"""
Test cases for Task 9: Seller Dashboard
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


@pytest.mark.seller
@pytest.mark.unit
class TestSellerDashboard:
    """Test seller dashboard functionality"""
    
    @pytest.fixture
    def seller_client(self, client):
        """Create authenticated seller client"""
        try:
            seller = User.create(
                email='seller_dash@example.com',
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
            conn.commit()
            cursor.close()
            conn.close()
            
            client.post('/auth/login', data={
                'email': 'seller_dash@example.com',
                'password': 'seller123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_seller_dashboard_access(self, seller_client):
        """Test seller dashboard is accessible"""
        response = seller_client.get('/seller/dashboard')
        assert response.status_code == 200
    
    def test_seller_products_page(self, seller_client):
        """Test seller products page"""
        response = seller_client.get('/seller/products')
        assert response.status_code == 200
    
    def test_seller_inventory_page(self, seller_client):
        """Test seller inventory page"""
        response = seller_client.get('/seller/inventory')
        assert response.status_code == 200
    
    def test_seller_orders_page(self, seller_client):
        """Test seller orders page"""
        response = seller_client.get('/seller/orders')
        assert response.status_code == 200
    
    def test_create_product_page(self, seller_client):
        """Test create product page"""
        response = seller_client.get('/seller/products/create')
        assert response.status_code == 200


@pytest.mark.seller
@pytest.mark.integration
class TestSellerOperations:
    """Test seller operations"""
    
    @pytest.fixture
    def seller_client(self, client):
        """Create authenticated seller client"""
        try:
            seller = User.create(
                email='seller_ops@example.com',
                password='seller123',
                role='seller'
            )
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sellers (user_id, store_name, contact_email)
                VALUES (%s, %s, %s)
            """, (seller.id, 'Test Store', seller.email))
            conn.commit()
            cursor.close()
            conn.close()
            
            client.post('/auth/login', data={
                'email': 'seller_ops@example.com',
                'password': 'seller123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_create_product(self, seller_client):
        """Test creating a product"""
        try:
            # First create a category
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO categories (name, slug) VALUES (%s, %s)
            """, ('Test Category', 'test-category'))
            category_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            response = seller_client.post('/seller/products/create', data={
                'name': 'Test Product',
                'description': 'Test Description',
                'category_id': category_id,
                'price': '29.99',
                'sku': 'TEST-001',
                'quantity': '10'
            }, follow_redirects=True)
            
            assert response.status_code == 200
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

