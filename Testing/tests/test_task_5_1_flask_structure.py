"""
Test cases for Task 5 - Subtask 5.1: Flask Project Structure (MVC style)
Tests Flask application initialization and MVC structure
"""

import pytest
import json
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app


@pytest.mark.unit
class TestTask51FlaskStructure:
    """Test Flask project structure (MVC style)"""
    
    def test_flask_app_initialized(self):
        """Test Flask app is initialized correctly"""
        assert app is not None
        assert app.template_folder == 'templates'
        assert app.static_folder == 'static'
    
    def test_app_config_has_secret_key(self):
        """Test app has SECRET_KEY configured"""
        assert 'SECRET_KEY' in app.config
        assert app.config['SECRET_KEY'] is not None
    
    def test_models_directory_structure(self):
        """Test models directory exists with proper structure"""
        # Test that models can be imported
        try:
            from models import __init__ as models_init
            from models.user import User
            assert User is not None
        except ImportError as e:
            pytest.fail(f"Models directory structure issue: {e}")
    
    def test_app_has_correct_name(self):
        """Test app has correct name"""
        assert app.name == 'app' or 'ecommerce' in app.name.lower()
    
    def test_app_is_flask_instance(self):
        """Test app is a Flask instance"""
        from flask import Flask
        assert isinstance(app, Flask)

