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


# Category management
@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """View all categories"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, c.name, c.parent_id, p.name as parent_name, c.description, c.slug
        FROM categories c
        LEFT JOIN categories p ON c.parent_id = p.id
        ORDER BY c.parent_id, c.name
    """)
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    """Create new category"""
    if request.method == 'POST':
        name = request.form.get('name')
        parent_id = request.form.get('parent_id') or None
        description = request.form.get('description')
        slug = request.form.get('slug') or name.lower().replace(' ', '-')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO categories (name, parent_id, description, slug)
                VALUES (%s, %s, %s, %s)
            """, (name, parent_id, description, slug))
            conn.commit()
            flash('Category created successfully!', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            flash(f'Error creating category: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    # Get parent categories for dropdown
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE parent_id IS NULL")
    parent_categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/create_category.html', parent_categories=parent_categories)

# Order overview page
@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    """View all orders"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.order_number, o.status, o.total, o.created_at,
               u.email as customer_email, s.store_name
        FROM orders o
        JOIN users u ON o.customer_id = u.id
        JOIN sellers s ON o.seller_id = s.id
        ORDER BY o.created_at DESC
        LIMIT 50
    """)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/orders.html', orders=orders)
