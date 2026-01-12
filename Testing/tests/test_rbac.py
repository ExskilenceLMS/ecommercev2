"""
Test cases for Task 3: Authorization Design - RBAC
Tests the Role-Based Access Control system
"""

import pytest
import sys
from pathlib import Path
from flask import Flask, session
from werkzeug.exceptions import Forbidden
from unittest.mock import patch, MagicMock

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

# Import the module/functions you want to test
from rbac import (
    RBAC, 
    role_required, 
    admin_required, 
    seller_required, 
    customer_required, 
    permission_required
)

# --- Fixtures ---

@pytest.fixture
def app():
    """Create a Flask app context for tests."""
    from flask_login import LoginManager
    
    # Use the actual app from Development
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    
    # Push an app context
    ctx = flask_app.app_context()
    ctx.push()
    yield flask_app
    ctx.pop()

class MockUser:
    """Mock object for Flask-Login current_user"""
    def __init__(self, is_authenticated=True, role=None):
        self.is_authenticated = is_authenticated
        self.role = role

# --- RBAC Class Unit Tests ---

@pytest.mark.unit
def test_rbac_has_role():
    assert RBAC.has_role('admin', 'admin') is True
    assert RBAC.has_role('seller', 'admin') is False
    assert RBAC.has_role(None, 'admin') is False

@pytest.mark.unit
def test_rbac_has_permission():
    # Test Admin Permissions
    assert RBAC.has_permission('admin', 'manage_sellers') is True
    assert RBAC.has_permission('admin', 'place_orders') is False # Admin doesn't have customer permissions in this dict
    
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
    perms = RBAC.get_user_permissions('seller')
    assert 'manage_inventory' in perms
    assert 'view_store_orders' in perms
    assert 'manage_sellers' not in perms
    
    assert RBAC.get_user_permissions('unknown') == []
    assert RBAC.get_user_permissions(None) == []

# --- Decorator Tests ---

@pytest.mark.unit
@patch('rbac.current_user')
def test_role_required_success(mock_user, app):
    """Test role_required allows access if roles match exactly."""
    mock_user.is_authenticated = True
    mock_user.role = 'seller'
    
    @role_required('seller')
    def protected_view():
        return "Success"
        
    with app.test_request_context():
        assert protected_view() == "Success"

@pytest.mark.unit
@patch('rbac.current_user')
def test_role_required_fail_wrong_role(mock_user, app):
    """Test role_required raises 403 if role does not match."""
    mock_user.is_authenticated = True
    mock_user.role = 'customer' # Wrong role
    
    @role_required('seller')
    def protected_view():
        return "Success"
        
    with app.test_request_context():
        with pytest.raises(Forbidden):
            protected_view()

@pytest.mark.unit
@patch('rbac.current_user')
def test_admin_required_success(mock_user, app):
    mock_user.is_authenticated = True
    mock_user.role = 'admin'
    
    @admin_required
    def admin_view():
        return "Admin Area"
    
    with app.test_request_context():
        assert admin_view() == "Admin Area"

@pytest.mark.unit
@patch('rbac.current_user')
def test_admin_required_fail_wrong_role(mock_user, app):
    """Test that a seller cannot access admin area."""
    mock_user.is_authenticated = True
    mock_user.role = 'seller'
    
    @admin_required
    def admin_view():
        return "Admin Area"
    
    with app.test_request_context():
        with pytest.raises(Forbidden):
            admin_view()

@pytest.mark.unit
@patch('rbac.current_user')
def test_seller_required_hierarchy(mock_user, app):
    """
    Test seller_required logic:
    if user_role not in ['admin', 'seller'] -> 403
    This means Admin SHOULD be able to access Seller routes.
    """
    @seller_required
    def seller_view():
        return "Seller Area"

    with app.test_request_context():
        # Case 1: Seller accesses Seller View -> Pass
        mock_user.role = 'seller'
        mock_user.is_authenticated = True
        assert seller_view() == "Seller Area"

        # Case 2: Admin accesses Seller View -> Pass (Hierarchy check)
        mock_user.role = 'admin'
        assert seller_view() == "Seller Area"

        # Case 3: Customer accesses Seller View -> Fail
        mock_user.role = 'customer'
        with pytest.raises(Forbidden):
            seller_view()

@pytest.mark.unit
@patch('rbac.current_user')
def test_customer_required_hierarchy(mock_user, app):
    """
    Test customer_required logic:
    if user_role not in ['admin', 'customer'] -> 403
    """
    @customer_required
    def customer_view():
        return "Customer Area"

    with app.test_request_context():
        # Case 1: Customer -> Pass
        mock_user.role = 'customer'
        mock_user.is_authenticated = True
        assert customer_view() == "Customer Area"
        
        # Case 2: Seller -> Fail
        mock_user.role = 'seller'
        with pytest.raises(Forbidden):
            customer_view()

@pytest.mark.unit
@patch('rbac.current_user')
def test_permission_required(mock_user, app):
    """Test permission_required decorator"""
    mock_user.is_authenticated = True
    mock_user.role = 'seller'
    
    @permission_required('manage_inventory')
    def inventory_view():
        return "Inventory"

    @permission_required('manage_sellers')
    def admin_view():
        return "Sellers"

    with app.test_request_context():
        # Seller has 'manage_inventory' -> Pass
        assert inventory_view() == "Inventory"
        
        # Seller does NOT have 'manage_sellers' -> Fail
        with pytest.raises(Forbidden):
            admin_view()

# --- Unauthenticated Redirect Tests ---

@pytest.mark.unit
@patch('rbac.current_user')
def test_unauthenticated_redirect(mock_user, app):
    """Test that unauthenticated users are redirected to login for all decorators"""
    mock_user.is_authenticated = False
    
    # Create dummy wrapped functions
    wrapped_funcs = [
        role_required('admin')(lambda: 'ok'),
        admin_required(lambda: 'ok'),
        seller_required(lambda: 'ok'),
        customer_required(lambda: 'ok'),
        permission_required('any_perm')(lambda: 'ok')
    ]
    
    with app.test_request_context():
        for func in wrapped_funcs:
            response = func()
            # Assert 302 Redirect
            assert response.status_code == 302, f"Expected 302 redirect, got {response.status_code}"
            # Assert redirect to login page
            # url_for('auth.login') will resolve to '/auth/login' or '/login'
            location = response.headers.get('Location', '')
            assert '/login' in location or '/auth/login' in location, \
                f"Expected redirect to login, got: {location}"