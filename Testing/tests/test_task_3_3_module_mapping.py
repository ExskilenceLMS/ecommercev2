"""
Test cases for Task 3 - Subtask 3.3: RBAC intro - Map modules to roles
Tests the module to role mapping functionality
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

# Import module mapping (Subtask 3.3)
from module_mapping import (
    MODULE_ROLE_MAPPING,
    get_modules_for_role,
    get_role_for_module
)


# --- Module Mapping Tests (Subtask 3.3) ---

@pytest.mark.unit
def test_module_mapping_structure():
    """Test that MODULE_ROLE_MAPPING has expected structure"""
    assert 'admin' in MODULE_ROLE_MAPPING
    assert 'seller' in MODULE_ROLE_MAPPING
    assert 'customer' in MODULE_ROLE_MAPPING
    assert 'product' in MODULE_ROLE_MAPPING
    assert 'cart' in MODULE_ROLE_MAPPING
    assert 'checkout' in MODULE_ROLE_MAPPING
    assert 'order' in MODULE_ROLE_MAPPING
    assert 'payment' in MODULE_ROLE_MAPPING

@pytest.mark.unit
def test_module_mapping_admin():
    """Test admin module mapping"""
    admin_module = MODULE_ROLE_MAPPING['admin']
    assert admin_module['required_role'] == 'admin'
    assert 'blueprint' in admin_module
    assert 'routes' in admin_module
    assert 'permissions' in admin_module
    assert 'manage_sellers' in admin_module['permissions']

@pytest.mark.unit
def test_module_mapping_seller():
    """Test seller module mapping"""
    seller_module = MODULE_ROLE_MAPPING['seller']
    assert seller_module['required_role'] == 'seller'
    assert 'allowed_roles' in seller_module
    assert 'admin' in seller_module['allowed_roles']
    assert 'seller' in seller_module['allowed_roles']
    assert 'manage_products' in seller_module['permissions']

@pytest.mark.unit
def test_module_mapping_customer():
    """Test customer module mapping"""
    customer_module = MODULE_ROLE_MAPPING['customer']
    assert customer_module['required_role'] == 'customer'
    assert 'allowed_roles' in customer_module
    assert 'admin' in customer_module['allowed_roles']
    assert 'customer' in customer_module['allowed_roles']
    assert 'manage_cart' in customer_module['permissions']

@pytest.mark.unit
def test_get_modules_for_role_admin():
    """Test get_modules_for_role for admin (should have access to all)"""
    modules = get_modules_for_role('admin')
    assert 'admin' in modules
    assert 'seller' in modules
    assert 'customer' in modules
    assert 'product' in modules
    assert 'cart' in modules
    assert 'checkout' in modules
    assert 'order' in modules
    assert 'payment' in modules

@pytest.mark.unit
def test_get_modules_for_role_seller():
    """Test get_modules_for_role for seller"""
    modules = get_modules_for_role('seller')
    assert 'seller' in modules
    assert 'product' in modules  # Public module
    assert 'admin' not in modules  # Seller cannot access admin module
    assert 'customer' not in modules  # Seller cannot access customer module

@pytest.mark.unit
def test_get_modules_for_role_customer():
    """Test get_modules_for_role for customer"""
    modules = get_modules_for_role('customer')
    assert 'customer' in modules
    assert 'product' in modules  # Public module
    assert 'cart' in modules
    assert 'checkout' in modules
    assert 'payment' in modules
    assert 'admin' not in modules  # Customer cannot access admin module
    assert 'seller' not in modules  # Customer cannot access seller module

@pytest.mark.unit
def test_get_role_for_module():
    """Test get_role_for_module function"""
    admin_role_info = get_role_for_module('admin')
    assert admin_role_info['required_role'] == 'admin'
    
    seller_role_info = get_role_for_module('seller')
    assert seller_role_info['required_role'] == 'seller'
    assert 'admin' in seller_role_info['allowed_roles']
    
    product_role_info = get_role_for_module('product')
    assert product_role_info['required_role'] is None  # Public module

@pytest.mark.unit
def test_get_role_for_module_invalid():
    """Test get_role_for_module with invalid module"""
    result = get_role_for_module('invalid_module')
    assert result is None

