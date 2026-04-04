"""
Role-Based Access Control Decorators
Task 7: Role-Based Access Control

Commit Structure:
- Subtask 7.1: Role decorators - Decorator definitions with redirect logic and unauthorized access handling

Note: Redirect logic and unauthorized access handling (abort(403)) are part of the decorator implementations.
"""

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


#  Role decorators
def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.role != 'admin':
            flash('Admin access required.', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def seller_required(f):
    """Decorator to require seller role (admin can also access)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.role not in ['admin', 'seller']:
            flash('Seller access required.', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def customer_required(f):
    """Decorator to require customer role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.role not in ['admin', 'customer']:
            flash('Customer access required.', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require one of the specified roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'error')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

