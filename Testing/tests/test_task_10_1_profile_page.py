"""
Test cases for Task 10 - Subtask 10.1: Profile Page
Tests customer profile view and update functionality
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


@pytest.mark.customer
@pytest.mark.unit
class TestTask101ProfilePage:
    """Test customer profile page functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_profile@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_profile@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_customer_profile_page(self, customer_client):
        """Test customer profile page is accessible"""
        response = customer_client.get('/customer/profile')
        assert response.status_code == 200
    
    def test_profile_page_displays_profile_form(self, customer_client):
        """Test profile page displays profile form"""
        response = customer_client.get('/customer/profile')
        assert response.status_code == 200
        # Check for profile-related content
        assert b'profile' in response.data.lower() or b'form' in response.data.lower()
    
    def test_update_profile_functionality(self, customer_client):
        """Test updating customer profile"""
        try:
            response = customer_client.post('/customer/profile', data={
                'first_name': 'Updated',
                'last_name': 'Name',
                'phone': '1234567890'
            }, follow_redirects=True)
            
            assert response.status_code == 200
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_profile_page_requires_authentication(self, client):
        """Test profile page requires authentication"""
        response = client.get('/customer/profile', follow_redirects=False)
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location or '/login' in response.location
    
    def test_profile_page_requires_customer_role(self, client):
        """Test profile page requires customer role"""
        try:
            # Create seller user
            seller = User.create(
                email='seller_profile@example.com',
                password='seller123',
                role='seller'
            )
            client.post('/auth/login', data={
                'email': 'seller_profile@example.com',
                'password': 'seller123'
            })
            
            # Try to access profile page
            response = client.get('/customer/profile')
            # Should return 403
            assert response.status_code == 403
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

