"""
User Model
"""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin):
    """User model for Flask-Login"""
    
    def __init__(self, id, email, password_hash, role, first_name=None, last_name=None, 
                 phone=None, is_active=True):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        # is_active is a property in UserMixin, so store it in a private attribute
        self._is_active = is_active
    
    @property
    def is_active(self):
        """Override UserMixin's is_active property"""
        return self._is_active
    
    @is_active.setter
    def is_active(self, value):
        """Allow setting is_active"""
        self._is_active = value
    
    def get_id(self):
        """Return user ID as string (required by Flask-Login)"""
        return str(self.id)
    
    def check_password(self, password):
        """Check if provided password matches"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def hash_password(password):
        """Hash a password"""
        return generate_password_hash(password)
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        from utils import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, email, password_hash, role, first_name, last_name, phone, is_active
            FROM users WHERE id = %s
        """, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return User(*row)
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        from utils import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, email, password_hash, role, first_name, last_name, phone, is_active
            FROM users WHERE email = %s
        """, (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return User(*row)
        return None
    
    @staticmethod
    def create(email, password, role, first_name=None, last_name=None, phone=None):
        """Create a new user"""
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        from utils import get_db_connection
        password_hash = User.hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, password_hash, role, first_name, last_name, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (email, password_hash, role, first_name, last_name, phone))
        user_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return User.get_by_id(user_id)

