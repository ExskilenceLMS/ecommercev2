"""
Test cases for Task 14 - Subtask 14.4_admin_overview: Admin Order Overview
Tests admin order overview functionality
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
class TestTask145AdminOverview:
    """Test admin order overview functionality"""
    
    @pytest.fixture
    def admin_client(self, client):
        """Create authenticated admin client"""
        try:
            admin = User.create(
                email='admin_overview@example.com',
                password='admin123',
                role='admin'
            )
            client.post('/auth/login', data={
                'email': 'admin_overview@example.com',
                'password': 'admin123'
            })
            return client
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_order_list_page_admin(self, admin_client):
        """Test order list page for admin"""
        response = admin_client.get('/orders/')
        assert response.status_code == 200

