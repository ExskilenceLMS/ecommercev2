import sys
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from decorators import customer_required
from utils import get_db_connection

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


def get_or_create_cart():
    """Get or create cart for current user (helper function - already implemented)"""
    """Get or create cart for current user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get existing cart
    cursor.execute("""
        SELECT id FROM cart WHERE customer_id = %s
        ORDER BY created_at DESC LIMIT 1
    """, (current_user.id,))
    cart = cursor.fetchone()
    
    if cart:
        cart_id = cart[0]
    else:
        # Create new cart
        cursor.execute("""
            INSERT INTO cart (customer_id) VALUES (%s)
        """, (current_user.id,))
        cart_id = cursor.lastrowid
        conn.commit()
    
    cursor.close()
    conn.close()
    return cart_id


# Add product to cart
@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
@customer_required
def add(product_id):
    """Add product to cart"""
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity < 1:
        flash('Quantity must be at least 1.', 'error')
        return redirect(url_for('product.details', product_id=product_id))
    
    # Check product availability
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.is_active, i.quantity
        FROM products p
        LEFT JOIN inventory i ON p.id = i.product_id
        WHERE p.id = %s
    """, (product_id,))
    product = cursor.fetchone()
    
    if not product or not product[1]:  # is_active
        flash('Product not available.', 'error')
        return redirect(url_for('product.list'))
    
    if product[2] and product[2] < quantity:  # stock quantity
        flash(f'Only {product[2]} items available in stock.', 'error')
        return redirect(url_for('product.details', product_id=product_id))
    
    cart_id = get_or_create_cart()
    
    # Check if item already in cart
    cursor.execute("""
        SELECT id, quantity FROM cart_items 
        WHERE cart_id = %s AND product_id = %s
    """, (cart_id, product_id))
    existing_item = cursor.fetchone()
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item[1] + quantity
        if product[2] and new_quantity > product[2]:
            flash(f'Cannot add more. Only {product[2]} items available.', 'error')
            return redirect(url_for('product.details', product_id=product_id))
        
        cursor.execute("""
            UPDATE cart_items SET quantity = %s WHERE id = %s
        """, (new_quantity, existing_item[0]))
    else:
        # Add new item
        cursor.execute("""
            INSERT INTO cart_items (cart_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (cart_id, product_id, quantity))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Product added to cart!', 'success')
    return redirect(url_for('cart.view'))