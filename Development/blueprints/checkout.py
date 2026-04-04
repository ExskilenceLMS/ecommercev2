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


# Place order logic
@checkout_bp.route('/place-order', methods=['POST'])
@login_required
@customer_required
def place_order():
    """Place order"""
    shipping_address_id = request.form.get('shipping_address_id', type=int)
    
    if not shipping_address_id:
        flash('Please select a shipping address.', 'error')
        return redirect(url_for('checkout.review'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verify address belongs to user
        cursor.execute("""
            SELECT id FROM addresses WHERE id = %s AND user_id = %s
        """, (shipping_address_id, current_user.id))
        address = cursor.fetchone()
        
        if not address:
            flash('Invalid shipping address.', 'error')
            return redirect(url_for('checkout.review'))
        
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
        
        # Get cart items grouped by seller
        cursor.execute("""
            SELECT ci.product_id, ci.quantity, p.price, p.seller_id, s.store_name
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            JOIN sellers s ON p.seller_id = s.id
            WHERE ci.cart_id = %s
        """, (cart_id,))
        cart_items = cursor.fetchall()
        
        if not cart_items:
            flash('Your cart is empty.', 'error')
            return redirect(url_for('product.list'))
        
        # Group items by seller and create orders
        orders_created = []
        
        # Group by seller
        seller_items = {}
        for item in cart_items:
            seller_id = item[3]
            if seller_id not in seller_items:
                seller_items[seller_id] = []
            seller_items[seller_id].append(item)
        
        # Create order for each seller
        for seller_id, items in seller_items.items():
            # Calculate totals for this seller's items
            subtotal = sum(float(item[2]) * item[1] for item in items)
            tax = subtotal * 0.10
            shipping = 10.00
            total = subtotal + tax + shipping
            
            order_number = generate_order_number()
            
            # Create order
            cursor.execute("""
                INSERT INTO orders (order_number, customer_id, seller_id, shipping_address_id,
                                  status, subtotal, tax, shipping_cost, total)
                VALUES (%s, %s, %s, %s, 'placed', %s, %s, %s, %s)
            """, (order_number, current_user.id, seller_id, shipping_address_id,
                  subtotal, tax, shipping, total))
            order_id = cursor.lastrowid
            
            # Create order items
            for item in items:
                product_id, quantity, price = item[0], item[1], item[2]
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, product_id, quantity, price, float(price) * quantity))
                
                # Update inventory
                cursor.execute("""
                    UPDATE inventory SET quantity = quantity - %s WHERE product_id = %s
                """, (quantity, product_id))
            
            orders_created.append(order_number)
        
        # Clear cart
        cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Order placed successfully! Order number(s): {", ".join(orders_created)}', 'success')
        return redirect(url_for('checkout.confirmation', order_numbers=','.join(orders_created)))
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        flash(f'Error placing order: {str(e)}', 'error')
        return redirect(url_for('checkout.review'))


# Order confirmation page
@checkout_bp.route('/confirmation')
@login_required
@customer_required
def confirmation():
    """Order confirmation page"""
    order_numbers = request.args.get('order_numbers', '').split(',')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    orders = []
    for order_num in order_numbers:
        if order_num:
            cursor.execute("""
                SELECT id, order_number, total, created_at, status
                FROM orders
                WHERE order_number = %s AND customer_id = %s
            """, (order_num.strip(), current_user.id))
            order = cursor.fetchone()
            if order:
                orders.append(order)
    
    cursor.close()
    conn.close()
    
    return render_template('checkout/confirmation.html', orders=orders)

