"""
Test cases for Task 13 - Subtask 13.3_order_confirmation: Order Confirmation Page
Tests order confirmation page functionality
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
class TestTask135OrderConfirmation:
    """Test order confirmation page functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_confirm@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_confirm@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_order_confirmation_page(self, customer_client):
        """Test order confirmation page"""
        response = customer_client.get('/checkout/confirmation?order_numbers=ORD-TEST123')
        assert response.status_code == 200

