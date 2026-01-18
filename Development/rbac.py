"""
Role-Based Access Control (RBAC) Module
"""
from functools import wraps
from flask import redirect, url_for, flash, session, abort
from flask_login import current_user

# Define roles & permissions

class RBAC:
    """Role-Based Access Control manager"""
    
    # Define role hierarchy
    ROLE_HIERARCHY = {
        'admin': ['admin', 'seller', 'customer'],
        'seller': ['seller'],
        'customer': ['customer']
    }
    
    # Define permissions per role
    PERMISSIONS = {
        'admin': [
            'manage_sellers',
            'manage_categories',
            'view_all_orders',
            'view_all_products',
            'view_reports',
            'manage_settings'
        ],
        'seller': [
            'manage_products',
            'manage_inventory',
            'view_store_orders',
            'update_order_status',
            'view_store_reports'
        ],
        'customer': [
            'browse_products',
            'manage_cart',
            'place_orders',
            'view_own_orders',
            'manage_profile'
        ]
    }
    
    @staticmethod
    def has_role(user_role, required_role):
        """Check if user has required role"""
        if not user_role:
            return False
        return user_role == required_role
    
    @staticmethod
    def has_permission(user_role, permission):
        """Check if user role has specific permission"""
        if not user_role or user_role not in RBAC.PERMISSIONS:
            return False
        return permission in RBAC.PERMISSIONS[user_role]
    
    @staticmethod
    def get_user_permissions(user_role):
        """Get all permissions for a role"""
        if not user_role or user_role not in RBAC.PERMISSIONS:
            return []
        return RBAC.PERMISSIONS[user_role]
    