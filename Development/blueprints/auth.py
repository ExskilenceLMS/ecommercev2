import sys
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Login & registration forms (Jinja)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'seller':
            return redirect(url_for('seller.dashboard'))
        elif current_user.role == 'customer':
            return redirect(url_for('customer.dashboard'))
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return render_template('auth/login.html')
        
        user = User.get_by_email(email)
        
        if user and user.check_password(password) and user.is_active:
            # Subtask 6.3: Flask-Login integration - login_user call
            login_user(user)
            flash(f'Welcome back, {user.first_name or user.email}!', 'success')
            
            # Redirect based on role
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'seller':
                return redirect(url_for('seller.dashboard'))
            elif user.role == 'customer':
                return redirect(url_for('customer.dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        # Validation
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/register.html')
        
        # Check if user already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            flash('Email already registered. Please login instead.', 'error')
            return redirect(url_for('auth.login'))
        
        # Create customer user
        try:
            user = User.create(
                email=email,
                password=password,
                role='customer',
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('auth/register.html')


# Logout
@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
