from flask import Flask, render_template
from flask_login import LoginManager
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load environment variables
load_dotenv()

# MySQL connection & config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'ecommerce_db')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Database connection helper
def get_db_connection():
    """Create and return MySQL database connection"""
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb
    except ImportError:
        try:
            import MySQLdb
        except ImportError:
            raise ImportError("Please install PyMySQL: pip install PyMySQL")
    
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4'
    )

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user from database for Flask-Login"""
    from models.user import User
    return User.get_by_id(int(user_id))

# Set database connection function in utils
from utils import set_db_connection_func
set_db_connection_func(get_db_connection)


# Import and register blueprints
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.seller import seller_bp
from blueprints.customer import customer_bp
from blueprints.product import product_bp
from blueprints.cart import cart_bp
from blueprints.checkout import checkout_bp
from blueprints.order import order_bp
from blueprints.payment import payment_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(seller_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(order_bp)
app.register_blueprint(payment_bp)

# Error handlers
@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

# Main route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting E-Commerce Application")
    print("Visit: http://localhost:5001")
    print("Make sure MySQL is running and database is set up")
    app.run(debug=True, host='0.0.0.0', port=5001)

