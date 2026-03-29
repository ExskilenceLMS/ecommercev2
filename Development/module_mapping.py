"""
Module to Role Mapping

This file documents which blueprints/modules are accessible by which roles.
"""

# Module to Role Mapping
MODULE_ROLE_MAPPING = {
    # Admin-only modules
    'admin': {
        'blueprint': 'admin',
        'routes': [
            '/admin/dashboard',
            '/admin/sellers',
            '/admin/categories',
            '/admin/orders'
        ],
        'required_role': 'admin',
        'permissions': [
            'manage_sellers',
            'manage_categories',
            'view_all_orders',
            'view_all_products',
            'view_reports',
            'manage_settings'
        ]
    },
    
    # Seller modules (admin can also access)
    'seller': {
        'blueprint': 'seller',
        'routes': [
            '/seller/dashboard',
            '/seller/products',
            '/seller/inventory',
            '/seller/orders'
        ],
        'required_role': 'seller',
        'allowed_roles': ['admin', 'seller'],
        'permissions': [
            'manage_products',
            'manage_inventory',
            'view_store_orders',
            'update_order_status',
            'view_store_reports'
        ]
    },
    
    # Customer modules (admin can also access)
    'customer': {
        'blueprint': 'customer',
        'routes': [
            '/customer/dashboard',
            '/customer/profile',
            '/customer/orders',
            '/customer/addresses'
        ],
        'required_role': 'customer',
        'allowed_roles': ['admin', 'customer'],
        'permissions': [
            'browse_products',
            'manage_cart',
            'place_orders',
            'view_own_orders',
            'manage_profile'
        ]
    },
    
    # Product browsing (public, but customer actions require customer role)
    'product': {
        'blueprint': 'product',
        'routes': [
            '/products',
            '/products/<id>'
        ],
        'required_role': None,  # Public access
        'permissions': ['browse_products']
    },
    
    # Cart management (customer only)
    'cart': {
        'blueprint': 'cart',
        'routes': [
            '/cart',
            '/cart/add',
            '/cart/update',
            '/cart/remove'
        ],
        'required_role': 'customer',
        'allowed_roles': ['admin', 'customer'],
        'permissions': ['manage_cart']
    },
    
    # Checkout (customer only)
    'checkout': {
        'blueprint': 'checkout',
        'routes': [
            '/checkout/review',
            '/checkout/place'
        ],
        'required_role': 'customer',
        'allowed_roles': ['admin', 'customer'],
        'permissions': ['place_orders']
    },
    
    # Orders (role-based access)
    'order': {
        'blueprint': 'order',
        'routes': [
            '/orders',
            '/orders/<id>'
        ],
        'required_role': None,  # Access depends on user role
        'permissions': {
            'admin': ['view_all_orders'],
            'seller': ['view_store_orders'],
            'customer': ['view_own_orders']
        }
    },
    
    # Payment (customer only)
    'payment': {
        'blueprint': 'payment',
        'routes': [
            '/payment/process',
            '/payment/success',
            '/payment/invoice'
        ],
        'required_role': 'customer',
        'allowed_roles': ['admin', 'customer'],
        'permissions': ['place_orders']
    }
}


def get_modules_for_role(role):
    """Get all modules accessible by a given role"""
    accessible_modules = []
    
    for module_name, module_info in MODULE_ROLE_MAPPING.items():
        required_role = module_info.get('required_role')
        allowed_roles = module_info.get('allowed_roles', [])
        
        if required_role is None:  # Public module
            accessible_modules.append(module_name)
        elif role == required_role or role in allowed_roles:
            accessible_modules.append(module_name)
        elif role == 'admin':  # Admin can access everything
            accessible_modules.append(module_name)
    
    return accessible_modules


def get_role_for_module(module_name):
    """Get the required role(s) for a module"""
    if module_name not in MODULE_ROLE_MAPPING:
        return None
    
    module_info = MODULE_ROLE_MAPPING[module_name]
    return {
        'required_role': module_info.get('required_role'),
        'allowed_roles': module_info.get('allowed_roles', [])
    }

