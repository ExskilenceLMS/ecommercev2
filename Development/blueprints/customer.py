import sys
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

# Add Development directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from decorators import customer_required
from utils import get_db_connection

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')


@customer_bp.route('/dashboard')
@login_required
@customer_required
def dashboard():
    """Customer dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get customer statistics
    cursor.execute("""
        SELECT COUNT(*) FROM orders WHERE customer_id = %s
    """, (current_user.id,))
    order_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM orders WHERE customer_id = %s AND status = 'placed'
    """, (current_user.id,))
    pending_orders = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM addresses WHERE user_id = %s
    """, (current_user.id,))
    address_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    stats = {
        'total_orders': order_count,
        'pending_orders': pending_orders,
        'addresses': address_count
    }
    
    return render_template('customer/dashboard.html', stats=stats)


# Subtask 10.1: Profile page
# ============================
@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@customer_required
def profile():
    """Customer profile page"""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET first_name = %s, last_name = %s, phone = %s
                WHERE id = %s
            """, (first_name, last_name, phone, current_user.id))
            conn.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating profile: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('customer.profile'))
    
    return render_template('customer/profile.html')


@customer_bp.route('/addresses')
@login_required
@customer_required
def addresses():
    """View customer addresses"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, address_line1, address_line2, city, state, postal_code, country, is_default
        FROM addresses
        WHERE user_id = %s
        ORDER BY is_default DESC, created_at DESC
    """, (current_user.id,))
    addresses = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('customer/addresses.html', addresses=addresses)


@customer_bp.route('/addresses/create', methods=['GET', 'POST'])
@login_required
@customer_required
def create_address():
    """Create new address"""
    if request.method == 'POST':
        address_line1 = request.form.get('address_line1')
        address_line2 = request.form.get('address_line2')
        city = request.form.get('city')
        state = request.form.get('state')
        postal_code = request.form.get('postal_code')
        country = request.form.get('country', 'USA')
        is_default = request.form.get('is_default') == 'on'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # If setting as default, unset other defaults
            if is_default:
                cursor.execute("""
                    UPDATE addresses SET is_default = FALSE WHERE user_id = %s
                """, (current_user.id,))
            
            cursor.execute("""
                INSERT INTO addresses (user_id, address_line1, address_line2, city, state, postal_code, country, is_default)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (current_user.id, address_line1, address_line2, city, state, postal_code, country, is_default))
            conn.commit()
            flash('Address added successfully!', 'success')
            return redirect(url_for('customer.addresses'))
        except Exception as e:
            conn.rollback()
            flash(f'Error adding address: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('customer/create_address.html')


# Order history
@customer_bp.route('/orders')
@login_required
@customer_required
def orders():
    """View customer order history"""
    conn = get_db_connection()
    cursor = conn.cursor()
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
    
    return render_template('customer/orders.html', orders=orders)
