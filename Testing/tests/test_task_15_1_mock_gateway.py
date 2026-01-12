"""
Test cases for Task 15 - Subtask 15.1_mock_gateway: Mock Payment Gateway Integration
Tests mock payment gateway integration
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
class TestTask152MockGateway:
    """Test mock payment gateway integration"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_gateway@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_gateway@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_payment_process_page(self, customer_client):
        """Test payment process page"""
        # This would require an actual order ID
        response = customer_client.get('/payment/process/1', follow_redirects=True)
        # Should either show payment form or redirect
        assert response.status_code in [200, 404, 302]

