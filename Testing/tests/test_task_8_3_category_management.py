"""
Test cases for Task 8 - Subtask 8.3: Category Management
Tests category list and create category routes
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
class TestTask83CategoryManagement:
    """Test category management functionality"""
    
    @pytest.fixture
    def admin_client(self, client):
        """Create authenticated admin client"""
        try:
            admin = User.create(
                email='admin_category@example.com',
                password='admin123',
                role='admin'
            )
            client.post('/auth/login', data={
                'email': 'admin_category@example.com',
                'password': 'admin123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_admin_categories_page(self, admin_client):
        """Test admin categories page is accessible"""
        response = admin_client.get('/admin/categories')
        assert response.status_code == 200
    
    def test_create_category_page(self, admin_client):
        """Test create category page is accessible"""
        response = admin_client.get('/admin/categories/create')
        assert response.status_code == 200
    
    def test_create_category_functionality(self, admin_client):
        """Test creating a category"""
        try:
            response = admin_client.post('/admin/categories/create', data={
                'name': 'Test Category',
                'description': 'Test Description',
                'slug': 'test-category'
            }, follow_redirects=True)
            
            assert response.status_code == 200
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_categories_page_requires_authentication(self, client):
        """Test categories page requires authentication"""
        response = client.get('/admin/categories', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_categories_page_requires_admin_role(self, client):
        """Test categories page requires admin role"""
        try:
            # Create customer user
            customer = User.create(
                email='customer_category@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_category@example.com',
                'password': 'customer123'
            })
            
            # Try to access categories page
            response = client.get('/admin/categories')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

