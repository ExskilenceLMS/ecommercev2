import sys
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from utils import get_db_connection

order_bp = Blueprint('order', __name__, url_prefix='/orders')


# Order status lifecycle
@order_bp.route('/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_status(order_id):
    """Update order status (seller/admin only)"""
    if current_user.role not in ['admin', 'seller']:
        flash('Permission denied.', 'error')
        return redirect(url_for('order.list'))
    
    new_status = request.form.get('status')
    valid_statuses = ['placed', 'confirmed', 'packed', 'shipped', 'delivered', 'cancelled']
    
    if new_status not in valid_statuses:
        flash('Invalid status.', 'error')
        return redirect(url_for('order.details', order_id=order_id))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify access
    if current_user.role == 'seller':
        cursor.execute("SELECT id FROM sellers WHERE user_id = %s", (current_user.id,))
        seller = cursor.fetchone()
        if seller:
            cursor.execute("""
                SELECT seller_id FROM orders WHERE id = %s
            """, (order_id,))
            order = cursor.fetchone()
            if not order or order[0] != seller[0]:
                flash('Order not found.', 'error')
                return redirect(url_for('order.list'))
    
    try:
        cursor.execute("""
            UPDATE orders SET status = %s WHERE id = %s
        """, (new_status, order_id))
        conn.commit()
        flash('Order status updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating order: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('order.details', order_id=order_id))


@order_bp.route('/')
@login_required
def list():
    """List orders based on user role"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Role Based access
    # Seller order view
    if current_user.role == 'seller':
        # Seller sees their orders
        cursor.execute("SELECT id FROM sellers WHERE user_id = %s", (current_user.id,))
        seller = cursor.fetchone()
        if seller:
            cursor.execute("""
                SELECT o.id, o.order_number, o.status, o.total, o.created_at,
                       u.email as customer_email, u.first_name, u.last_name
                FROM orders o
                JOIN users u ON o.customer_id = u.id
                WHERE o.seller_id = %s
                ORDER BY o.created_at DESC
            """, (seller[0],))
        else:
            cursor.close()
            conn.close()
            flash('Seller profile not found.', 'error')
            return redirect(url_for('index'))
        
    else:
        cursor.execute("""
            SELECT o.id, o.order_number, o.status, o.total, o.created_at, s.store_name
            FROM orders o
            JOIN sellers s ON o.seller_id = s.id
            WHERE o.customer_id = %s
            ORDER BY o.created_at DESC
        """, (current_user.id,))
    
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('order/list.html', orders=orders)


@order_bp.route('/<int:order_id>')
@login_required
def details(order_id):
    """Order details - shared across roles"""
    """Order details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get order with access control
    if current_user.role == 'admin':
        cursor.execute("""
            SELECT o.*, u.email as customer_email, u.first_name, u.last_name,
                   s.store_name, a.address_line1, a.address_line2, a.city, a.state, a.postal_code
            FROM orders o
            JOIN users u ON o.customer_id = u.id
            JOIN sellers s ON o.seller_id = s.id
            JOIN addresses a ON o.shipping_address_id = a.id
            WHERE o.id = %s
        """, (order_id,))
    elif current_user.role == 'seller':
        cursor.execute("SELECT id FROM sellers WHERE user_id = %s", (current_user.id,))
        seller = cursor.fetchone()
        if seller:
            cursor.execute("""
                SELECT o.*, u.email as customer_email, u.first_name, u.last_name,
                       s.store_name, a.address_line1, a.address_line2, a.city, a.state, a.postal_code
                FROM orders o
                JOIN users u ON o.customer_id = u.id
                JOIN sellers s ON o.seller_id = s.id
                JOIN addresses a ON o.shipping_address_id = a.id
                WHERE o.id = %s AND o.seller_id = %s
            """, (order_id, seller[0]))
        else:
            cursor.close()
            conn.close()
            flash('Order not found.', 'error')
            return redirect(url_for('order.list'))
    else:
        cursor.execute("""
            SELECT o.*, u.email as customer_email, u.first_name, u.last_name,
                   s.store_name, a.address_line1, a.address_line2, a.city, a.state, a.postal_code
            FROM orders o
            JOIN users u ON o.customer_id = u.id
            JOIN sellers s ON o.seller_id = s.id
            JOIN addresses a ON o.shipping_address_id = a.id
            WHERE o.id = %s AND o.customer_id = %s
        """, (order_id, current_user.id))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        conn.close()
        flash('Order not found.', 'error')
        return redirect(url_for('order.list'))
    
    # Get order items
    cursor.execute("""
        SELECT oi.*, p.name as product_name, p.image_url, p.sku
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    """, (order_id,))
    order_items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('order/details.html', order=order, order_items=order_items)
