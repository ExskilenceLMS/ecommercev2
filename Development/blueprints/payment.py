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

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')


# Mock payment gateway integration
def generate_transaction_id():
    """Generate mock transaction ID"""
    return 'TXN-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


# Mock payment gateway integration
@payment_bp.route('/process/<int:order_id>', methods=['GET', 'POST'])
@login_required
@customer_required
def process(order_id):
    """Process payment for order"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get order
    cursor.execute("""
        SELECT o.id, o.order_number, o.total, o.status
        FROM orders o
        WHERE o.id = %s AND o.customer_id = %s
    """, (order_id, current_user.id))
    order = cursor.fetchone()
    
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('customer.orders'))
    
    if order[3] != 'placed':  # status
        flash('Order has already been processed.', 'error')
        return redirect(url_for('order.details', order_id=order_id))
    
    # Check if payment already exists
    cursor.execute("""
        SELECT id, status FROM payments WHERE order_id = %s
    """, (order_id,))
    existing_payment = cursor.fetchone()
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        if not payment_method:
            flash('Please select a payment method.', 'error')
            return render_template('payment/process.html', order=order, existing_payment=existing_payment)
        
        # Mock payment processing
        # In real application, this would integrate with payment gateway
        payment_status = 'completed'  # Mock: always succeeds
        transaction_id = generate_transaction_id()
        invoice_number = "" # we'll genrate in task 15.4
        
        try:
            # Subtask 15.3: Link payment to orders
            if existing_payment:
                # Update existing payment
                cursor.execute("""
                    UPDATE payments
                    SET payment_method = %s, status = %s, transaction_id = %s,
                        invoice_number = %s, payment_date = NOW()
                    WHERE order_id = %s
                """, (payment_method, payment_status, transaction_id, invoice_number, order_id))
            else:
                # Create new payment
                cursor.execute("""
                    INSERT INTO payments (order_id, amount, payment_method, status, transaction_id, invoice_number, payment_date)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """, (order_id, order[2], payment_method, payment_status, transaction_id, invoice_number))
            
            # Update order status to confirmed
            cursor.execute("""
                UPDATE orders SET status = 'confirmed' WHERE id = %s
            """, (order_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Payment processed successfully!', 'success')
            return redirect(url_for('payment.success', order_id=order_id))
            
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            flash(f'Payment processing failed: {str(e)}', 'error')
    
    cursor.close()
    conn.close()
    
    return render_template('payment/process.html', order=order, existing_payment=existing_payment)
    
    cursor.close()
    conn.close()
    
    return render_template('payment/process.html', order=order, existing_payment=existing_payment)


# Payment success & failure handling
@payment_bp.route('/success/<int:order_id>')
@login_required
@customer_required
def success(order_id):
    """Payment success page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, o.order_number, o.total
        FROM payments p
        JOIN orders o ON p.order_id = o.id
        WHERE p.order_id = %s AND o.customer_id = %s
    """, (order_id, current_user.id))
    payment = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not payment:
        flash('Payment not found.', 'error')
        return redirect(url_for('customer.orders'))
    
    return render_template('payment/success.html', payment=payment)
