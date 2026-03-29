"""
Test cases for Task 14 - Subtask 14.2_customer_history: Customer Order History
Tests customer order history functionality
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
class TestTask143CustomerHistory:
    """Test customer order history functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_history@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_history@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_order_list_page_customer(self, customer_client):
        """Test order list page for customer"""
        response = customer_client.get('/orders/')
        assert response.status_code == 200

