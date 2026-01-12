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

        # continue in task 11.3
    
    cursor.close()
    conn.close()
    
    return render_template('payment/process.html', order=order, existing_payment=existing_payment)