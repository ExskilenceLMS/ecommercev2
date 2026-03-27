import sys
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
import math

# Add Development directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils import get_db_connection

product_bp = Blueprint('product', __name__, url_prefix='/products')


# Product listing page (with category filter, search, and pagination)
@product_bp.route('/')
def list():
    """Product listing page with search and filters"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'newest')  # newest, price_low, price_high, name
    
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed. Please check your database configuration.', 'error')
            return render_template('product/list.html', 
                                 products=[],
                                 categories=[],
                                 current_page=1,
                                 total_pages=0,
                                 category_id=None,
                                 search_query='',
                                 sort_by='newest')
        
        cursor = conn.cursor()
        
        # Build query
        query = """
            SELECT p.id, p.name, p.description, p.price, p.image_url, p.sku,
                   c.name as category_name, s.store_name, i.quantity
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN sellers s ON p.seller_id = s.id
            LEFT JOIN inventory i ON p.id = i.product_id
            WHERE p.is_active = TRUE AND (i.quantity > 0 OR i.quantity IS NULL)
        """
        params = []
        
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
        
        if search_query:
            query += " AND (p.name LIKE %s OR p.description LIKE %s)"
            params.extend([f'%{search_query}%', f'%{search_query}%'])
        
        # Sorting
        if sort_by == 'price_low':
            query += " ORDER BY p.price ASC"
        elif sort_by == 'price_high':
            query += " ORDER BY p.price DESC"
        elif sort_by == 'name':
            query += " ORDER BY p.name ASC"
        else:  # newest
            query += " ORDER BY p.created_at DESC"
        
        # Get total count
        count_query = query.replace(
            "SELECT p.id, p.name, p.description, p.price, p.image_url, p.sku, c.name as category_name, s.store_name, i.quantity",
            "SELECT COUNT(*)"
        )
        cursor.execute(count_query, params)
        count_result = cursor.fetchone()
        total = count_result[0] if count_result else 0
        
        # Get paginated results
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        cursor.execute(query, params)
        products = cursor.fetchall()
        
        # Get categories for filter
        cursor.execute("SELECT id, name FROM categories WHERE parent_id IS NULL ORDER BY name")
        categories = cursor.fetchall()
        
        cursor.close()
        if conn:
            conn.close()
        
        total_pages = math.ceil(total / per_page) if total > 0 else 0
        
        return render_template('product/list.html', 
                             products=products,
                             categories=categories,
                             current_page=page,
                             total_pages=total_pages,
                             category_id=category_id,
                             search_query=search_query,
                             sort_by=sort_by)
    except Exception as e:
        flash(f'Error loading products: {str(e)}', 'error')
        return render_template('product/list.html', 
                             products=[],
                             categories=[],
                             current_page=1,
                             total_pages=0,
                             category_id=None,
                             search_query='',
                             sort_by='newest')

# Product details page
@product_bp.route('/<int:product_id>')
def details(product_id):
    """Product details page"""
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed. Please check your database configuration.', 'error')
            return redirect(url_for('product.list'))
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.*, c.name as category_name, s.store_name, s.id as seller_id,
                   i.quantity, i.low_stock_threshold
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN sellers s ON p.seller_id = s.id
            LEFT JOIN inventory i ON p.id = i.product_id
            WHERE p.id = %s AND p.is_active = TRUE
        """, (product_id,))
        product = cursor.fetchone()
        
        cursor.close()
        if conn:
            conn.close()
        
        if not product:
            flash('Product not found.', 'error')
            return redirect(url_for('product.list'))
        
        return render_template('product/details.html', product=product)
    except Exception as e:
        flash(f'Error loading product: {str(e)}', 'error')
        return redirect(url_for('product.list'))


@product_bp.route('/category/<int:category_id>')
def by_category(category_id):
    """View products by category"""
    return list()

