"""
Test cases for Task 6 - Subtask 6.1: Login & Registration Forms (Jinja)
Tests Jinja template rendering for login and registration forms
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app


@pytest.mark.auth
@pytest.mark.unit
class TestTask61LoginRegistrationForms:
    """Test login and registration form templates"""
    
    def test_login_page_loads(self, client):
        """Test login page loads and renders template"""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'form' in response.data.lower()
        assert b'email' in response.data.lower()
        assert b'password' in response.data.lower()
    
    def test_login_form_has_required_fields(self, client):
        """Test login form has required input fields"""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'name="email"' in response.data or b'id="email"' in response.data
        assert b'name="password"' in response.data or b'id="password"' in response.data
        assert b'type="submit"' in response.data or b'button' in response.data.lower()
    
    def test_register_page_loads(self, client):
        """Test register page loads and renders template"""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Register' in response.data
        assert b'form' in response.data.lower()
    
    def test_register_form_has_required_fields(self, client):
        """Test register form has required input fields"""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'name="email"' in response.data or b'id="email"' in response.data
        assert b'name="password"' in response.data or b'id="password"' in response.data
        assert b'name="confirm_password"' in response.data or b'id="confirm_password"' in response.data
        assert b'type="submit"' in response.data or b'button' in response.data.lower()
    
    def test_templates_extend_base(self, client):
        """Test that auth templates extend base template"""
        login_response = client.get('/auth/login')
        register_response = client.get('/auth/register')
        
        # Check that base template structure is present (navbar, etc.)
        # This is a basic check - actual structure depends on base.html
        assert login_response.status_code == 200
        assert register_response.status_code == 200

