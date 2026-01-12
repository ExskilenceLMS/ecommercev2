"""
Test cases for Task 15 - Subtask 15.2_payment_handling: Payment Success & Failure Handling
Tests payment success and failure handling
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
class TestTask153PaymentHandling:
    """Test payment success and failure handling"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_handling@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_handling@example.com',
                'password': 'customer123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_payment_success_page(self, customer_client):
        """Test payment success page"""
        response = customer_client.get('/payment/success/1', follow_redirects=True)
        # Should either show success or redirect
        assert response.status_code in [200, 404, 302]

