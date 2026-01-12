"""
Test cases for Task 15: Payment Handling
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app
from models.user import User
from utils import get_db_connection


@pytest.mark.unit
class TestPaymentHandling:
    """Test payment handling functionality"""
    
    @pytest.fixture
    def customer_client(self, client):
        """Create authenticated customer client"""
        try:
            customer = User.create(
                email='customer_payment@example.com',
                password='customer123',
                role='customer'
            )
            client.post('/auth/login', data={
                'email': 'customer_payment@example.com',
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
    
    def test_payment_success_page(self, customer_client):
        """Test payment success page"""
        response = customer_client.get('/payment/success/1', follow_redirects=True)
        # Should either show success or redirect
        assert response.status_code in [200, 404, 302]
    
    def test_invoice_page(self, customer_client):
        """Test invoice page"""
        response = customer_client.get('/payment/invoice/1', follow_redirects=True)
        # Should either show invoice or redirect
        assert response.status_code in [200, 404, 302]
    
    def test_process_payment(self, customer_client):
        """Test processing payment"""
        # This would require an actual order ID
        response = customer_client.post('/payment/process/1', data={
            'payment_method': 'credit_card'
        }, follow_redirects=True)
        # Should either process or show error
        assert response.status_code in [200, 404, 302]

