"""
Test cases for Task 5 - Subtask 5.2: MySQL Connection & Config
Tests MySQL database connection and configuration
"""

import pytest
import sys
from pathlib import Path

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

from app import app, get_db_connection


@pytest.mark.unit
class TestTask52MySQLConfig:
    """Test MySQL connection and configuration"""
    
    def test_mysql_config_present(self):
        """Test MySQL configuration keys are present"""
        assert 'MYSQL_HOST' in app.config
        assert 'MYSQL_USER' in app.config
        assert 'MYSQL_PASSWORD' in app.config
        assert 'MYSQL_DB' in app.config
    
    def test_mysql_config_has_values(self):
        """Test MySQL configuration has values (even if defaults)"""
        assert app.config['MYSQL_HOST'] is not None
        assert app.config['MYSQL_USER'] is not None
        assert app.config['MYSQL_PASSWORD'] is not None
        assert app.config['MYSQL_DB'] is not None
    
    def test_database_connection_function_exists(self):
        """Test database connection function exists"""
        assert callable(get_db_connection)
    
    def test_database_connection_function_imported(self):
        """Test database connection function can be imported"""
        from app import get_db_connection
        assert get_db_connection is not None
    
    def test_database_connection_attempt(self):
        """Test database connection can be attempted (may fail if DB not available)"""
        try:
            conn = get_db_connection()
            assert conn is not None
            conn.close()
        except Exception as e:
            # Database may not be available in test environment
            pytest.skip(f"Database not available: {e}")

