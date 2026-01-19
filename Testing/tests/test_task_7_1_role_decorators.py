"""
Test cases for Task 7 - Subtask 7.1: Role Decorators
Tests role decorator definitions and functionality
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from decorators import admin_required, seller_required, customer_required, role_required
from flask_login import current_user


@pytest.mark.unit
class TestTask71RoleDecorators:
    """Test role decorator definitions"""
    
    def test_admin_required_decorator_exists(self):
        """Test that admin_required decorator exists"""
        assert admin_required is not None
        assert callable(admin_required)
    
    def test_seller_required_decorator_exists(self):
        """Test that seller_required decorator exists"""
        assert seller_required is not None
        assert callable(seller_required)
    
    def test_customer_required_decorator_exists(self):
        """Test that customer_required decorator exists"""
        assert customer_required is not None
        assert callable(customer_required)
    
    def test_role_required_decorator_exists(self):
        """Test that role_required decorator exists"""
        assert role_required is not None
        assert callable(role_required)
    
    def test_decorators_are_callable(self):
        """Test that decorators can be called"""
        # Test that decorators can wrap functions
        @admin_required
        def test_func():
            return "test"
        
        assert callable(test_func)
        assert hasattr(test_func, '__wrapped__')
    
    def test_decorators_preserve_function_name(self):
        """Test that decorators preserve function names"""
        @admin_required
        def test_function():
            pass
        
        assert test_function.__name__ == 'test_function'

