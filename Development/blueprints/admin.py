import sys
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

# Add Development directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from decorators import admin_required
from utils import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin routes

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'seller'")
    seller_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'customer'")
    customer_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT SUM(total) FROM orders WHERE status != 'cancelled'
    """)
    total_revenue = cursor.fetchone()[0] or 0
    
    cursor.close()
    conn.close()
    
    stats = {
        'sellers': seller_count,
        'customers': customer_count,
        'products': product_count,
        'orders': order_count,
        'categories': category_count,
        'revenue': float(total_revenue)
    }
    
    return render_template('admin/dashboard.html', stats=stats)
