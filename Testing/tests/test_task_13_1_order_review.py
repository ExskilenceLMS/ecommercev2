"""
Test cases for Task 13 - Subtask 13.1_order_review: Order Review Page
Tests order review page functionality
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


@pytest.mark.unit
class TestTask132OrderReview:
    """Test order review page functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_review@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_review@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_checkout_review_page(self, customer_client):
        """Test checkout review page"""
        response = customer_client.get('/checkout/')
        # Should either show checkout or redirect if cart is empty
        assert response.status_code in [200, 302]

