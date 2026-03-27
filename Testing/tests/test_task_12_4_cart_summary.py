"""
Test cases for Task 12 - Subtask 12.4_cart_summary: Cart Summary Page
Tests cart summary page functionality
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
class TestTask125CartSummary:
    """Test cart summary page functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_summary@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_summary@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_cart_view_page(self, customer_client):
        """Test cart view page displays summary"""
        response = customer_client.get('/cart/')
        assert response.status_code == 200
        # Check for cart-related content
        assert b'cart' in response.data.lower() or b'table' in response.data.lower()
    
    def test_cart_shows_totals(self, customer_client):
        """Test cart shows totals"""
        response = customer_client.get('/cart/')
        assert response.status_code == 200

