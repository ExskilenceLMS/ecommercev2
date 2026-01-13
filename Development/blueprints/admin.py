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


# Seller management
@admin_bp.route('/sellers')
@login_required
@admin_required
def sellers():
    """View all sellers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.store_name, u.email, u.first_name, u.last_name, 
               s.contact_email, s.contact_phone, s.created_at
        FROM sellers s
        JOIN users u ON s.user_id = u.id
        ORDER BY s.created_at DESC
    """)
    sellers = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/sellers.html', sellers=sellers)


@admin_bp.route('/sellers/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_seller():
    """Create new seller"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        store_name = request.form.get('store_name')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        
        from models.user import User
        
        try:
            # Create user
            user = User.create(
                email=email,
                password=password,
                role='seller',
                first_name=first_name,
                last_name=last_name
            )
            
            # Create seller
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sellers (user_id, store_name, contact_email, contact_phone)
                VALUES (%s, %s, %s, %s)
            """, (user.id, store_name, contact_email, contact_phone))
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Seller created successfully!', 'success')
            return redirect(url_for('admin.sellers'))
        except Exception as e:
            flash(f'Error creating seller: {str(e)}', 'error')
    
    return render_template('admin/create_seller.html')
