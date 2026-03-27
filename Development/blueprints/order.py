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
