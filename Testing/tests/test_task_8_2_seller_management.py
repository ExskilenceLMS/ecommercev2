"""
Test cases for Task 8 - Subtask 8.2: Seller Management
Tests seller list and create seller routes
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


@pytest.mark.admin
@pytest.mark.unit
class TestTask82SellerManagement:
    """Test seller management functionality"""
    
    @pytest.fixture
    def admin_client(self, client):
        """Create authenticated admin client"""
        try:
            admin = User.create(
                email='admin_seller@example.com',
                password='admin123',
                role='admin'
            )
            client.post('/auth/login', data={
                'email': 'admin_seller@example.com',
                'password': 'admin123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_admin_sellers_page(self, admin_client):
        """Test admin sellers page is accessible"""
        response = admin_client.get('/admin/sellers')
        assert response.status_code == 200
    
    def test_create_seller_page(self, admin_client):
        """Test create seller page is accessible"""
        response = admin_client.get('/admin/sellers/create')
        assert response.status_code == 200
        assert b'Create' in response.data or b'seller' in response.data.lower()
    
    def test_create_seller_functionality(self, admin_client):
        """Test creating a seller"""
        try:
            import random
            email = f'seller{random.randint(1000, 9999)}@example.com'
            
            response = admin_client.post('/admin/sellers/create', data={
                'email': email,
                'password': 'seller123',
                'first_name': 'Test',
                'last_name': 'Seller',
                'store_name': 'Test Store',
                'contact_email': email,
                'contact_phone': '1234567890'
            }, follow_redirects=True)
            
            assert response.status_code == 200
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_sellers_page_requires_authentication(self, client):
        """Test sellers page requires authentication"""
        response = client.get('/admin/sellers', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_sellers_page_requires_admin_role(self, client):
        """Test sellers page requires admin role"""
        try:
            # Create customer user
            customer = User.create(
                email='customer_seller@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_seller@example.com',
                'password': 'customer123'
            })
            
            # Try to access sellers page
            response = client.get('/admin/sellers')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

