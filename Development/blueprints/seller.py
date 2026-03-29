import sys
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

# Add Development directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from decorators import seller_required
from utils import get_db_connection

seller_bp = Blueprint('seller', __name__, url_prefix='/seller')


@seller_bp.route('/dashboard')
@login_required
@seller_required
def dashboard():
    """Seller dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get seller ID
    cursor.execute("SELECT id FROM sellers WHERE user_id = %s", (current_user.id,))
    seller = cursor.fetchone()
    if not seller:
        flash('Seller profile not found.', 'error')
        return redirect(url_for('index'))
    
    seller_id = seller[0]
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM products WHERE seller_id = %s", (seller_id,))
    product_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM orders WHERE seller_id = %s
    """, (seller_id,))
    order_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM orders WHERE seller_id = %s AND status = 'placed'
    """, (seller_id,))
    pending_orders = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT SUM(total) FROM orders WHERE seller_id = %s AND status != 'cancelled'
    """, (seller_id,))
    total_revenue = cursor.fetchone()[0] or 0
    
    cursor.close()
    conn.close()
    
    stats = {
        'products': product_count,
        'orders': order_count,
        'pending_orders': pending_orders,
        'revenue': float(total_revenue)
    }
    
    return render_template('seller/dashboard.html', stats=stats)

# Product CRUD pages
@seller_bp.route('/products')
@login_required
@seller_required
def products():
    """View seller's products"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get seller ID
    cursor.execute("SELECT id FROM sellers WHERE user_id = %s", (current_user.id,))
    seller = cursor.fetchone()
    if not seller:
        flash('Seller profile not found.', 'error')
        return redirect(url_for('index'))
    
    seller_id = seller[0]
    
    cursor.execute("""
        SELECT p.id, p.name, p.price, p.sku, p.is_active, p.created_at,
               c.name as category_name, i.quantity
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN inventory i ON p.id = i.product_id
        WHERE p.seller_id = %s
        ORDER BY p.created_at DESC
    """, (seller_id,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('seller/products.html', products=products)


@seller_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
@seller_required
def create_product():
    """Create new product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get seller ID
    cursor.execute("SELECT id FROM sellers WHERE user_id = %s", (current_user.id,))
    seller = cursor.fetchone()
    if not seller:
        flash('Seller profile not found.', 'error')
        return redirect(url_for('index'))
    
    seller_id = seller[0]
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        sku = request.form.get('sku')
        quantity = request.form.get('quantity', 0)
        
        try:
            # Create product
            cursor.execute("""
                INSERT INTO products (seller_id, category_id, name, description, price, sku)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (seller_id, category_id, name, description, price, sku))
            product_id = cursor.lastrowid
            
            # Create inventory
            cursor.execute("""
                INSERT INTO inventory (product_id, quantity)
                VALUES (%s, %s)
            """, (product_id, quantity))
            
            conn.commit()
            flash('Product created successfully!', 'success')
            return redirect(url_for('seller.products'))
        except Exception as e:
            conn.rollback()
            flash(f'Error creating product: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    # Get categories for dropdown
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('seller/create_product.html', categories=categories)


@seller_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@seller_required
def edit_product(product_id):
    """Edit product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get seller ID
    cursor.execute("SELECT id FROM sellers WHERE user_id = %s", (current_user.id,))
    seller = cursor.fetchone()
    if not seller:
        flash('Seller profile not found.', 'error')
        return redirect(url_for('index'))
    
    seller_id = seller[0]
    
    # Get product
    cursor.execute("""
        SELECT p.*, i.quantity
        FROM products p
        LEFT JOIN inventory i ON p.id = i.product_id
        WHERE p.id = %s AND p.seller_id = %s
    """, (product_id, seller_id))
    product = cursor.fetchone()
    
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('seller.products'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        sku = request.form.get('sku')
        is_active = request.form.get('is_active') == 'on'
        quantity = request.form.get('quantity', 0)
        
        try:
            cursor.execute("""
                UPDATE products
                SET name = %s, description = %s, price = %s, category_id = %s, sku = %s, is_active = %s
                WHERE id = %s
            """, (name, description, price, category_id, sku, is_active, product_id))
            
            cursor.execute("""
                UPDATE inventory SET quantity = %s WHERE product_id = %s
            """, (quantity, product_id))
            
            conn.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('seller.products'))
        except Exception as e:
            conn.rollback()
            flash(f'Error updating product: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    # Get categories
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('seller/edit_product.html', product=product, categories=categories)
