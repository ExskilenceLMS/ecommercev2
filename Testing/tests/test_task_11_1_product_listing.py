"""
Test cases for Task 11 - Subtask 11.1: Product Listing Page
Tests basic product listing functionality
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app


@pytest.mark.unit
class TestTask111ProductListing:
    """Test product listing page functionality"""
    
    def test_product_list_page_loads(self, client):
        """Test product list page loads"""
        response = client.get('/products/')
        assert response.status_code == 200
        assert b'Products' in response.data or b'product' in response.data.lower()
    
    def test_product_list_displays_products(self, client):
        """Test product list displays products"""
        response = client.get('/products/')
        assert response.status_code == 200
        # Check for product-related content
        assert b'product' in response.data.lower() or b'table' in response.data.lower()

