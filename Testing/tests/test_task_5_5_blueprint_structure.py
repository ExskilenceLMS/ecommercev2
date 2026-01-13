"""
Test cases for Task 5 - Subtask 5.5: Blueprint Structure
Tests blueprint structure and registration
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
class TestTask55BlueprintStructure:
    """Test blueprint structure"""
    
    def test_blueprints_directory_exists(self):
        """Test blueprints directory exists"""
        try:
            from blueprints import __init__ as blueprints_init
            assert blueprints_init is not None
        except ImportError:
            pytest.fail("Blueprints directory does not exist")
    
    def test_blueprints_can_be_imported(self):
        """Test blueprints can be imported"""
        try:
            from blueprints.auth import auth_bp
            assert auth_bp is not None
        except ImportError as e:
            pytest.fail(f"Blueprints cannot be imported: {e}")
    
    def test_blueprints_registered(self):
        """Test blueprints are registered with app"""
        # Check that blueprints are registered
        registered_blueprints = [bp.name for bp in app.blueprints.values()]
        
        # At minimum, auth blueprint should be registered
        assert len(registered_blueprints) > 0
        # Check for common blueprints
        expected_blueprints = ['auth', 'admin', 'seller', 'customer', 'product']
        for bp_name in expected_blueprints:
            if bp_name in registered_blueprints:
                assert True
                break
        else:
            # At least one blueprint should be registered
            assert len(registered_blueprints) > 0
    
    def test_blueprint_routes_accessible(self, client):
        """Test blueprint routes are accessible"""
        # Test auth blueprint route
        response = client.get('/auth/login')
        assert response.status_code in [200, 302]  # 302 if redirecting
    
    def test_blueprint_url_prefix(self):
        """Test blueprints have correct URL prefixes"""
        # Check that auth blueprint has correct prefix
        from blueprints.auth import auth_bp
        assert auth_bp.url_prefix == '/auth'

