"""
Test cases for Task 3 - Subtask 3.1: Define roles & permissions
Tests the RBAC class with role hierarchy and permissions
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

# Import only the RBAC class (Subtask 3.1)
from rbac import RBAC


# --- RBAC Class Unit Tests (Subtask 3.1) ---

@pytest.mark.unit
def test_rbac_has_role():
    """Test RBAC.has_role method"""
    assert RBAC.has_role('admin', 'admin') is True
    assert RBAC.has_role('seller', 'admin') is False
    assert RBAC.has_role(None, 'admin') is False

@pytest.mark.unit
def test_rbac_has_permission():
    """Test RBAC.has_permission method"""
    # Test Admin Permissions
    assert RBAC.has_permission('admin', 'manage_sellers') is True
    assert RBAC.has_permission('admin', 'place_orders') is False  # Admin doesn't have customer permissions in this dict
    
    # Test Seller Permissions
    assert RBAC.has_permission('seller', 'manage_inventory') is True
    assert RBAC.has_permission('seller', 'manage_sellers') is False

    # Test Customer Permissions
    assert RBAC.has_permission('customer', 'manage_cart') is True
    
    # Edge Cases
    assert RBAC.has_permission(None, 'manage_cart') is False
    assert RBAC.has_permission('hacker', 'manage_cart') is False

@pytest.mark.unit
def test_rbac_get_user_permissions():
    """Test RBAC.get_user_permissions method"""
    perms = RBAC.get_user_permissions('seller')
    assert 'manage_inventory' in perms
    assert 'view_store_orders' in perms
    assert 'manage_sellers' not in perms
    
    assert RBAC.get_user_permissions('unknown') == []
    assert RBAC.get_user_permissions(None) == []

@pytest.mark.unit
def test_rbac_role_hierarchy():
    """Test RBAC.ROLE_HIERARCHY structure"""
    assert 'admin' in RBAC.ROLE_HIERARCHY
    assert 'seller' in RBAC.ROLE_HIERARCHY
    assert 'customer' in RBAC.ROLE_HIERARCHY
    assert len(RBAC.ROLE_HIERARCHY['admin']) == 3
    assert len(RBAC.ROLE_HIERARCHY['seller']) == 1
    assert len(RBAC.ROLE_HIERARCHY['customer']) == 1

@pytest.mark.unit
def test_rbac_permissions_structure():
    """Test RBAC.PERMISSIONS structure"""
    assert 'admin' in RBAC.PERMISSIONS
    assert 'seller' in RBAC.PERMISSIONS
    assert 'customer' in RBAC.PERMISSIONS
    assert len(RBAC.PERMISSIONS['admin']) > 0
    assert len(RBAC.PERMISSIONS['seller']) > 0
    assert len(RBAC.PERMISSIONS['customer']) > 0

