"""
Shared utilities for the application
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Database connection (will be set by app.py)
_db_connection_func = None

def set_db_connection_func(func):
    """Set the database connection function"""
    global _db_connection_func
    _db_connection_func = func

def get_db_connection():
    """Get database connection"""
    if _db_connection_func:
        return _db_connection_func()
    raise RuntimeError("Database connection function not set")

