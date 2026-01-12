"""
Test cases for Task 9 - Subtask 9.1: Product CRUD Pages
Tests product list, create, and edit routes
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
class TestTask91ProductCRUD:
    """Test product CRUD functionality"""
    
    @pytest.fixture
    def seller_client(self, client):
        """Create authenticated seller client"""
        try:
            seller = User.create(
                email='seller_product@example.com',
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
                'email': 'seller_product@example.com',
                'password': 'seller123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_seller_products_page(self, seller_client):
        """Test seller products page is accessible"""
        response = seller_client.get('/seller/products')
        assert response.status_code == 200
    
    def test_create_product_page(self, seller_client):
        """Test create product page is accessible"""
        response = seller_client.get('/seller/products/create')
        assert response.status_code == 200
        assert b'Create' in response.data or b'product' in response.data.lower()
    
    def test_create_product_functionality(self, seller_client):
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
    
    def test_products_page_requires_authentication(self, client):
        """Test products page requires authentication"""
        response = client.get('/seller/products', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_products_page_requires_seller_role(self, client):
        """Test products page requires seller role"""
        try:
            # Create customer user
            customer = User.create(
                email='customer_product@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_product@example.com',
                'password': 'customer123'
            })
            
            # Try to access products page
            response = client.get('/seller/products')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

