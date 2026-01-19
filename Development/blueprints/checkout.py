import sys
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
import random
import string

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from decorators import customer_required
from utils import get_db_connection

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')


# Order review page (with address selection and price calculation)
@checkout_bp.route('/')
@login_required
@customer_required
def review():
    """Order review page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get cart
    cursor.execute("""
        SELECT id FROM cart WHERE customer_id = %s
        ORDER BY created_at DESC LIMIT 1
    """, (current_user.id,))
    cart = cursor.fetchone()
    
    if not cart:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('product.list'))
    
    cart_id = cart[0]
    
    # Get cart items
    cursor.execute("""
        SELECT ci.product_id, ci.quantity, p.name, p.price, p.sku, s.id as seller_id, s.store_name
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        JOIN sellers s ON p.seller_id = s.id
        WHERE ci.cart_id = %s
    """, (cart_id,))
    cart_items = cursor.fetchall()
    
    if not cart_items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('product.list'))
    
    # Get addresses
    cursor.execute("""
        SELECT id, address_line1, address_line2, city, state, postal_code, country, is_default
        FROM addresses
        WHERE user_id = %s
        ORDER BY is_default DESC
    """, (current_user.id,))
    addresses = cursor.fetchall()
    
    # Calculate totals
    subtotal = sum(float(item[3]) * item[1] for item in cart_items)
    tax = subtotal * 0.10  # 10% tax
    shipping = 10.00  # Fixed shipping cost
    total = subtotal + tax + shipping
    
    cursor.close()
    conn.close()
    
    return render_template('checkout/review.html',
                         cart_items=cart_items,
                         addresses=addresses,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total)

