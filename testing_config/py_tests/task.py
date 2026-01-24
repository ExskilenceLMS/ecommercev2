"""
Backend Test Suite for E-Commerce Project
All backend pytest cases should be added to this file.
Tests are grouped by subtask (branch name) with clear headers.
"""

import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add Development directory to Python path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
if str(development_dir) not in sys.path:
    sys.path.insert(0, str(development_dir))

load_dotenv()

# Try to import MySQLdb, fallback to PyMySQL
try:
    import MySQLdb
except ImportError:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb
    except ImportError:
        pytest.skip("PyMySQL not installed", allow_module_level=True)


# =====================================================
# Subtask: task_2
# Description: Database Design - Entity identification, relationship mapping, normalization, ER Diagram, MySQL schema
# =====================================================

@pytest.fixture(scope="module")
def db_connection():
    """Create database connection for testing"""
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    db_name = os.getenv("MYSQL_DB", "ecommerce_db")
    
    try:
        conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=db_name,
            charset='utf8mb4'
        )
        yield conn
        conn.close()
    except MySQLdb.Error as e:
        pytest.skip(f"Cannot connect to database: {e}", allow_module_level=True)


@pytest.fixture(scope="module")
def cursor(db_connection):
    """Create database cursor"""
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()


@pytest.mark.integration
class TestDatabaseExistence:
    """Test if database exists and is accessible"""
    
    def test_database_exists(self, db_connection):
        """Test that the database exists and is accessible"""
        assert db_connection is not None
        cursor = db_connection.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        assert db_name is not None
        assert db_name == os.getenv("MYSQL_DB", "ecommerce_db")
        cursor.close()
    
    def test_database_connection_works(self, db_connection):
        """Test that we can execute queries on the database"""
        cursor = db_connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1
        cursor.close()


@pytest.mark.integration
class TestTableExistence:
    """Test if all required tables exist"""
    
    @pytest.mark.parametrize("table_name", [
        "users",
        "sellers",
        "categories",
        "products",
        "inventory",
        "addresses",
        "cart",
        "cart_items",
        "orders",
        "order_items",
        "payments"
    ])
    def test_table_exists(self, cursor, table_name):
        """Test that each required table exists"""
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = %s
        """, (table_name,))
        result = cursor.fetchone()
        assert result[0] == 1, f"Table '{table_name}' does not exist"
    
    def test_all_tables_count(self, cursor):
        """Test that exactly 11 tables exist"""
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_type = 'BASE TABLE'
        """)
        result = cursor.fetchone()
        assert result[0] == 11, f"Expected 11 tables, found {result[0]}"


@pytest.mark.integration
class TestUsersTable:
    """Test users table structure"""
    
    def test_users_table_columns(self, cursor):
        """Test that users table has all required columns"""
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY, EXTRA
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'users'
            ORDER BY ORDINAL_POSITION
        """)
        columns = {row[0]: {
            'type': row[1],
            'nullable': row[2],
            'default': row[3],
            'key': row[4],
            'extra': row[5]
        } for row in cursor.fetchall()}
        
        # Check required columns exist
        required_columns = ['id', 'email', 'password_hash', 'role', 'first_name', 
                          'last_name', 'phone', 'is_active', 'created_at', 'updated_at']
        for col in required_columns:
            assert col in columns, f"Column '{col}' missing in users table"
        
        # Check primary key
        assert columns['id']['key'] == 'PRI', "Column 'id' should be PRIMARY KEY"
        assert 'auto_increment' in columns['id']['extra'].lower(), "Column 'id' should be AUTO_INCREMENT"
        
        # Check NOT NULL constraints
        assert columns['email']['nullable'] == 'NO', "Column 'email' should be NOT NULL"
        assert columns['password_hash']['nullable'] == 'NO', "Column 'password_hash' should be NOT NULL"
        assert columns['role']['nullable'] == 'NO', "Column 'role' should be NOT NULL"
        
        # Check UNIQUE constraint on email
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE table_schema = DATABASE() 
            AND table_name = 'users' 
            AND constraint_type = 'UNIQUE'
            AND constraint_name LIKE '%email%'
        """)
        assert cursor.fetchone()[0] >= 1, "Email should have UNIQUE constraint"
        
        # Check ENUM for role
        cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM information_schema.columns
            WHERE table_schema = DATABASE() 
            AND table_name = 'users' 
            AND column_name = 'role'
        """)
        role_type = cursor.fetchone()[0]
        assert 'enum' in role_type.lower(), "Role should be ENUM type"
        assert 'admin' in role_type.lower() and 'seller' in role_type.lower() and 'customer' in role_type.lower()
    
    def test_users_table_indexes(self, cursor):
        """Test that users table has required indexes"""
        cursor.execute("""
            SELECT INDEX_NAME, COLUMN_NAME
            FROM information_schema.statistics
            WHERE table_schema = DATABASE() AND table_name = 'users'
            AND INDEX_NAME != 'PRIMARY'
        """)
        indexes = {row[0]: [] for row in cursor.fetchall()}
        cursor.execute("""
            SELECT INDEX_NAME, COLUMN_NAME
            FROM information_schema.statistics
            WHERE table_schema = DATABASE() AND table_name = 'users'
            AND INDEX_NAME != 'PRIMARY'
        """)
        for row in cursor.fetchall():
            if row[0] not in indexes:
                indexes[row[0]] = []
            indexes[row[0]].append(row[1])
        
        # Check for email index
        has_email_idx = any('email' in cols for cols in indexes.values())
        assert has_email_idx, "Users table should have index on email"
        
        # Check for role index
        has_role_idx = any('role' in cols for cols in indexes.values())
        assert has_role_idx, "Users table should have index on role"


@pytest.mark.integration
class TestSellersTable:
    """Test sellers table structure"""
    
    def test_sellers_table_columns(self, cursor):
        """Test that sellers table has all required columns"""
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'sellers'
            ORDER BY ORDINAL_POSITION
        """)
        columns = {row[0]: {
            'type': row[1],
            'nullable': row[2],
            'default': row[3],
            'key': row[4]
        } for row in cursor.fetchall()}
        
        required_columns = ['id', 'user_id', 'store_name', 'store_description', 
                          'contact_email', 'contact_phone', 'address', 'created_at']
        for col in required_columns:
            assert col in columns, f"Column '{col}' missing in sellers table"
        
        assert columns['id']['key'] == 'PRI', "Column 'id' should be PRIMARY KEY"
        assert columns['user_id']['nullable'] == 'NO', "Column 'user_id' should be NOT NULL"
        assert columns['store_name']['nullable'] == 'NO', "Column 'store_name' should be NOT NULL"
    
    def test_sellers_foreign_key(self, cursor):
        """Test that sellers table has foreign key to users"""
        cursor.execute("""
            SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE() 
            AND table_name = 'sellers' 
            AND referenced_table_name IS NOT NULL
        """)
        fks = cursor.fetchall()
        assert len(fks) > 0, "Sellers table should have foreign key"
        user_fk = [fk for fk in fks if fk[1] == 'users' and fk[2] == 'id']
        assert len(user_fk) > 0, "Sellers table should have foreign key to users.id"
    
    def test_sellers_unique_constraint(self, cursor):
        """Test that user_id has UNIQUE constraint"""
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE table_schema = DATABASE() 
            AND table_name = 'sellers' 
            AND constraint_type = 'UNIQUE'
        """)
        assert cursor.fetchone()[0] >= 1, "user_id should have UNIQUE constraint"


@pytest.mark.integration
class TestCategoriesTable:
    """Test categories table structure"""
    
    def test_categories_table_columns(self, cursor):
        """Test that categories table has all required columns"""
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'categories'
            ORDER BY ORDINAL_POSITION
        """)
        columns = {row[0]: {
            'type': row[1],
            'nullable': row[2],
            'key': row[3]
        } for row in cursor.fetchall()}
        
        required_columns = ['id', 'name', 'parent_id', 'description', 'slug', 'created_at']
        for col in required_columns:
            assert col in columns, f"Column '{col}' missing in categories table"
        
        assert columns['id']['key'] == 'PRI', "Column 'id' should be PRIMARY KEY"
        assert columns['name']['nullable'] == 'NO', "Column 'name' should be NOT NULL"
    
    def test_categories_self_referential_foreign_key(self, cursor):
        """Test that categories table has self-referential foreign key"""
        cursor.execute("""
            SELECT REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE() 
            AND table_name = 'categories' 
            AND column_name = 'parent_id'
            AND referenced_table_name IS NOT NULL
        """)
        fk = cursor.fetchone()
        assert fk is not None, "parent_id should have foreign key"
        assert fk[0] == 'categories', "parent_id should reference categories table"
        assert fk[1] == 'id', "parent_id should reference categories.id"


@pytest.mark.integration
class TestProductsTable:
    """Test products table structure"""
    
    def test_products_table_columns(self, cursor):
        """Test that products table has all required columns"""
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'products'
            ORDER BY ORDINAL_POSITION
        """)
        columns = {row[0]: {
            'type': row[1],
            'nullable': row[2],
            'default': row[3],
            'key': row[4]
        } for row in cursor.fetchall()}
        
        required_columns = ['id', 'seller_id', 'category_id', 'name', 'description', 
                          'price', 'sku', 'image_url', 'is_active', 'created_at', 'updated_at']
        for col in required_columns:
            assert col in columns, f"Column '{col}' missing in products table"
        
        assert columns['id']['key'] == 'PRI', "Column 'id' should be PRIMARY KEY"
        assert columns['seller_id']['nullable'] == 'NO', "Column 'seller_id' should be NOT NULL"
        assert columns['category_id']['nullable'] == 'NO', "Column 'category_id' should be NOT NULL"
        assert columns['name']['nullable'] == 'NO', "Column 'name' should be NOT NULL"
        assert columns['price']['nullable'] == 'NO', "Column 'price' should be NOT NULL"
    
    def test_products_foreign_keys(self, cursor):
        """Test that products table has foreign keys to sellers and categories"""
        cursor.execute("""
            SELECT REFERENCED_TABLE_NAME
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE() 
            AND table_name = 'products' 
            AND referenced_table_name IS NOT NULL
        """)
        fks = [row[0] for row in cursor.fetchall()]
        assert 'sellers' in fks, "Products table should have foreign key to sellers"
        assert 'categories' in fks, "Products table should have foreign key to categories"
    
    def test_products_indexes(self, cursor):
        """Test that products table has required indexes"""
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM information_schema.statistics
            WHERE table_schema = DATABASE() AND table_name = 'products'
            AND INDEX_NAME != 'PRIMARY'
        """)
        indexed_columns = [row[0] for row in cursor.fetchall()]
        assert 'seller_id' in indexed_columns, "Products should have index on seller_id"
        assert 'category_id' in indexed_columns, "Products should have index on category_id"
        assert 'sku' in indexed_columns, "Products should have index on sku"


@pytest.mark.integration
class TestInventoryTable:
    """Test inventory table structure"""
    
    def test_inventory_table_columns(self, cursor):
        """Test that inventory table has all required columns"""
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'inventory'
            ORDER BY ORDINAL_POSITION
        """)
        columns = {row[0]: {
            'type': row[1],
            'nullable': row[2],
            'default': row[3],
            'key': row[4]
        } for row in cursor.fetchall()}
        
        required_columns = ['id', 'product_id', 'quantity', 'low_stock_threshold', 'last_updated']
        for col in required_columns:
            assert col in columns, f"Column '{col}' missing in inventory table"
        
        assert columns['id']['key'] == 'PRI', "Column 'id' should be PRIMARY KEY"
        assert columns['product_id']['nullable'] == 'NO', "Column 'product_id' should be NOT NULL"
        assert columns['quantity']['nullable'] == 'NO', "Column 'quantity' should be NOT NULL"
    
    def test_inventory_foreign_key(self, cursor):
        """Test that inventory table has foreign key to products"""
        cursor.execute("""
            SELECT REFERENCED_TABLE_NAME
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE() 
            AND table_name = 'inventory' 
            AND column_name = 'product_id'
            AND referenced_table_name IS NOT NULL
        """)
        fk = cursor.fetchone()
        assert fk is not None, "Inventory should have foreign key to products"
        assert fk[0] == 'products', "Inventory should reference products table"
    
    def test_inventory_unique_constraint(self, cursor):
        """Test that product_id has UNIQUE constraint"""
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_schema = DATABASE() 
            AND tc.table_name = 'inventory' 
            AND tc.constraint_type = 'UNIQUE'
            AND kcu.column_name = 'product_id'
        """)
        assert cursor.fetchone()[0] >= 1, "product_id should have UNIQUE constraint"


@pytest.mark.integration
class TestOrdersTable:
    """Test orders table structure"""
    
    def test_orders_table_columns(self, cursor):
        """Test that orders table has all required columns"""
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'orders'
            ORDER BY ORDINAL_POSITION
        """)
        columns = {row[0]: {
            'type': row[1],
            'nullable': row[2],
            'default': row[3],
            'key': row[4]
        } for row in cursor.fetchall()}
        
        required_columns = ['id', 'order_number', 'customer_id', 'seller_id', 
                          'shipping_address_id', 'status', 'subtotal', 'tax', 
                          'shipping_cost', 'total', 'notes', 'created_at', 'updated_at']
        for col in required_columns:
            assert col in columns, f"Column '{col}' missing in orders table"
        
        assert columns['id']['key'] == 'PRI', "Column 'id' should be PRIMARY KEY"
        assert columns['order_number']['nullable'] == 'NO', "Column 'order_number' should be NOT NULL"
        assert columns['customer_id']['nullable'] == 'NO', "Column 'customer_id' should be NOT NULL"
        assert columns['seller_id']['nullable'] == 'NO', "Column 'seller_id' should be NOT NULL"
        assert columns['shipping_address_id']['nullable'] == 'NO', "Column 'shipping_address_id' should be NOT NULL"
        assert columns['subtotal']['nullable'] == 'NO', "Column 'subtotal' should be NOT NULL"
        assert columns['total']['nullable'] == 'NO', "Column 'total' should be NOT NULL"
    
    def test_orders_foreign_keys(self, cursor):
        """Test that orders table has foreign keys"""
        cursor.execute("""
            SELECT REFERENCED_TABLE_NAME
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE() 
            AND table_name = 'orders' 
            AND referenced_table_name IS NOT NULL
        """)
        fks = [row[0] for row in cursor.fetchall()]
        assert 'users' in fks, "Orders should have foreign key to users (customer_id)"
        assert 'sellers' in fks, "Orders should have foreign key to sellers"
        assert 'addresses' in fks, "Orders should have foreign key to addresses"
    
    def test_orders_status_enum(self, cursor):
        """Test that status is ENUM with correct values"""
        cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM information_schema.columns
            WHERE table_schema = DATABASE() 
            AND table_name = 'orders' 
            AND column_name = 'status'
        """)
        status_type = cursor.fetchone()[0].lower()
        assert 'enum' in status_type, "Status should be ENUM type"
        required_statuses = ['placed', 'confirmed', 'packed', 'shipped', 'delivered', 'cancelled']
        for status in required_statuses:
            assert status in status_type, f"Status ENUM should include '{status}'"
    
    def test_orders_indexes(self, cursor):
        """Test that orders table has required indexes"""
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM information_schema.statistics
            WHERE table_schema = DATABASE() AND table_name = 'orders'
            AND INDEX_NAME != 'PRIMARY'
        """)
        indexed_columns = [row[0] for row in cursor.fetchall()]
        assert 'customer_id' in indexed_columns, "Orders should have index on customer_id"
        assert 'seller_id' in indexed_columns, "Orders should have index on seller_id"
        assert 'status' in indexed_columns, "Orders should have index on status"
        assert 'order_number' in indexed_columns, "Orders should have index on order_number"


@pytest.mark.integration
class TestPaymentsTable:
    """Test payments table structure"""
    
    def test_payments_table_columns(self, cursor):
        """Test that payments table has all required columns"""
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'payments'
            ORDER BY ORDINAL_POSITION
        """)
        columns = {row[0]: {
            'type': row[1],
            'nullable': row[2],
            'default': row[3],
            'key': row[4]
        } for row in cursor.fetchall()}
        
        required_columns = ['id', 'order_id', 'amount', 'payment_method', 'status', 
                          'transaction_id', 'invoice_number', 'payment_date', 'created_at']
        for col in required_columns:
            assert col in columns, f"Column '{col}' missing in payments table"
        
        assert columns['id']['key'] == 'PRI', "Column 'id' should be PRIMARY KEY"
        assert columns['order_id']['nullable'] == 'NO', "Column 'order_id' should be NOT NULL"
        assert columns['amount']['nullable'] == 'NO', "Column 'amount' should be NOT NULL"
        assert columns['payment_method']['nullable'] == 'NO', "Column 'payment_method' should be NOT NULL"
    
    def test_payments_foreign_key(self, cursor):
        """Test that payments table has foreign key to orders"""
        cursor.execute("""
            SELECT REFERENCED_TABLE_NAME
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE() 
            AND table_name = 'payments' 
            AND column_name = 'order_id'
            AND referenced_table_name IS NOT NULL
        """)
        fk = cursor.fetchone()
        assert fk is not None, "Payments should have foreign key to orders"
        assert fk[0] == 'orders', "Payments should reference orders table"
    
    def test_payments_enums(self, cursor):
        """Test that payment_method and status are ENUMs"""
        cursor.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE 
            FROM information_schema.columns
            WHERE table_schema = DATABASE() 
            AND table_name = 'payments' 
            AND column_name IN ('payment_method', 'status')
        """)
        enums = {row[0]: row[1].lower() for row in cursor.fetchall()}
        
        assert 'enum' in enums['payment_method'], "payment_method should be ENUM"
        assert 'enum' in enums['status'], "status should be ENUM"
        
        # Check payment_method values
        payment_methods = ['credit_card', 'debit_card', 'paypal', 'cash_on_delivery']
        for method in payment_methods:
            assert method in enums['payment_method'], f"payment_method ENUM should include '{method}'"
        
        # Check status values
        statuses = ['pending', 'completed', 'failed', 'refunded']
        for status in statuses:
            assert status in enums['status'], f"status ENUM should include '{status}'"
    
    def test_payments_indexes(self, cursor):
        """Test that payments table has required indexes"""
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM information_schema.statistics
            WHERE table_schema = DATABASE() AND table_name = 'payments'
            AND INDEX_NAME != 'PRIMARY'
        """)
        indexed_columns = [row[0] for row in cursor.fetchall()]
        assert 'order_id' in indexed_columns, "Payments should have index on order_id"
        assert 'status' in indexed_columns, "Payments should have index on status"
        assert 'transaction_id' in indexed_columns, "Payments should have index on transaction_id"


@pytest.mark.integration
class TestDataTypes:
    """Test that columns have correct data types"""
    
    def test_decimal_columns(self, cursor):
        """Test that price/amount columns are DECIMAL"""
        decimal_columns = [
            ('products', 'price'),
            ('orders', 'subtotal'),
            ('orders', 'tax'),
            ('orders', 'shipping_cost'),
            ('orders', 'total'),
            ('order_items', 'price'),
            ('order_items', 'subtotal'),
            ('payments', 'amount')
        ]
        
        for table, column in decimal_columns:
            cursor.execute("""
                SELECT DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE
                FROM information_schema.columns
                WHERE table_schema = DATABASE()
                AND table_name = %s
                AND column_name = %s
            """, (table, column))
            result = cursor.fetchone()
            assert result is not None, f"{table}.{column} should exist"
            assert result[0] == 'decimal', f"{table}.{column} should be DECIMAL type"
            assert result[1] == 10, f"{table}.{column} should have precision 10"
            assert result[2] == 2, f"{table}.{column} should have scale 2"


# =====================================================
# Subtask: task_3_1_define_roles_and_permissions
# Description: RBAC class with role hierarchy and permissions matrix
# Files Changed: Development/rbac.py (RBAC class definition)
# =====================================================

# Import RBAC class for testing
from Development.rbac import RBAC

@pytest.mark.unit
class TestRBACClass:
    """Test RBAC class methods and structure"""
    
    def test_rbac_has_role(self):
        """Test RBAC.has_role method"""
        assert RBAC.has_role('admin', 'admin') is True
        assert RBAC.has_role('seller', 'admin') is False
        assert RBAC.has_role(None, 'admin') is False
    
    def test_rbac_has_permission(self):
        """Test RBAC.has_permission method"""
        # Test Admin Permissions
        assert RBAC.has_permission('admin', 'manage_sellers') is True
        assert RBAC.has_permission('admin', 'place_orders') is False  # Admin doesn't have customer permissions
        
        # Test Seller Permissions
        assert RBAC.has_permission('seller', 'manage_inventory') is True
        assert RBAC.has_permission('seller', 'manage_sellers') is False
        
        # Test Customer Permissions
        assert RBAC.has_permission('customer', 'manage_cart') is True
        
        # Edge Cases
        assert RBAC.has_permission(None, 'manage_cart') is False
        assert RBAC.has_permission('hacker', 'manage_cart') is False
    
    def test_rbac_get_user_permissions(self):
        """Test RBAC.get_user_permissions method"""
        perms = RBAC.get_user_permissions('seller')
        assert 'manage_inventory' in perms
        assert 'view_store_orders' in perms
        assert 'manage_sellers' not in perms
        
        assert RBAC.get_user_permissions('unknown') == []
        assert RBAC.get_user_permissions(None) == []
    
    def test_rbac_role_hierarchy(self):
        """Test RBAC.ROLE_HIERARCHY structure"""
        assert 'admin' in RBAC.ROLE_HIERARCHY
        assert 'seller' in RBAC.ROLE_HIERARCHY
        assert 'customer' in RBAC.ROLE_HIERARCHY
        assert len(RBAC.ROLE_HIERARCHY['admin']) == 3
        assert len(RBAC.ROLE_HIERARCHY['seller']) == 1
        assert len(RBAC.ROLE_HIERARCHY['customer']) == 1
    
    def test_rbac_permissions_structure(self):
        """Test RBAC.PERMISSIONS structure"""
        assert 'admin' in RBAC.PERMISSIONS
        assert 'seller' in RBAC.PERMISSIONS
        assert 'customer' in RBAC.PERMISSIONS
        assert len(RBAC.PERMISSIONS['admin']) > 0
        assert len(RBAC.PERMISSIONS['seller']) > 0
        assert len(RBAC.PERMISSIONS['customer']) > 0
    
    def test_rbac_admin_permissions(self):
        """Test that admin has all admin-specific permissions"""
        admin_perms = RBAC.get_user_permissions('admin')
        assert 'manage_sellers' in admin_perms
        assert 'manage_categories' in admin_perms
        assert 'view_all_orders' in admin_perms
        assert 'view_all_products' in admin_perms
    
    def test_rbac_seller_permissions(self):
        """Test that seller has seller-specific permissions"""
        seller_perms = RBAC.get_user_permissions('seller')
        assert 'manage_products' in seller_perms
        assert 'manage_inventory' in seller_perms
        assert 'view_store_orders' in seller_perms
        assert 'update_order_status' in seller_perms
    
    def test_rbac_customer_permissions(self):
        """Test that customer has customer-specific permissions"""
        customer_perms = RBAC.get_user_permissions('customer')
        assert 'browse_products' in customer_perms
        assert 'manage_cart' in customer_perms
        assert 'place_orders' in customer_perms
        assert 'view_own_orders' in customer_perms
        assert 'manage_profile' in customer_perms


# =====================================================
# Subtask: task_3_2_restrict_actions
# Description: RBAC decorators for route protection and action restrictions
# Files Changed: Development/rbac.py (decorators: role_required, admin_required, seller_required, customer_required, permission_required)
# =====================================================

from unittest.mock import patch
from werkzeug.exceptions import Forbidden


@pytest.fixture
def flask_app():
    """Create a Flask app context for decorator tests"""
    try:
        from flask_login import LoginManager
        from app import app as flask_app
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        
        ctx = flask_app.app_context()
        ctx.push()
        yield flask_app
        ctx.pop()
    except ImportError:
        pytest.skip("Flask app not available", allow_module_level=True)


@pytest.mark.unit
class TestRBACDecorators:
    """Test RBAC decorators for route protection"""
    
    @patch('rbac.current_user')
    def test_role_required_success(self, mock_user, flask_app):
        """Test role_required allows access if roles match exactly"""
        from rbac import role_required
        
        mock_user.is_authenticated = True
        mock_user.role = 'seller'
        
        @role_required('seller')
        def protected_view():
            return "Success"
            
        with flask_app.test_request_context():
            assert protected_view() == "Success"
    
    @patch('rbac.current_user')
    def test_role_required_fail_wrong_role(self, mock_user, flask_app):
        """Test role_required raises 403 if role does not match"""
        from rbac import role_required
        
        mock_user.is_authenticated = True
        mock_user.role = 'customer'  # Wrong role
        
        @role_required('seller')
        def protected_view():
            return "Success"
            
        with flask_app.test_request_context():
            with pytest.raises(Forbidden):
                protected_view()
    
    @patch('rbac.current_user')
    def test_admin_required_success(self, mock_user, flask_app):
        """Test admin_required allows admin access"""
        from Development.rbac import admin_required
        
        mock_user.is_authenticated = True
        mock_user.role = 'admin'
        
        @admin_required
        def admin_view():
            return "Admin Area"
        
        with flask_app.test_request_context():
            assert admin_view() == "Admin Area"
    
    @patch('rbac.current_user')
    def test_admin_required_fail_wrong_role(self, mock_user, flask_app):
        """Test that a seller cannot access admin area"""
        from Development.rbac import admin_required
        
        mock_user.is_authenticated = True
        mock_user.role = 'seller'
        
        @admin_required
        def admin_view():
            return "Admin Area"
        
        with flask_app.test_request_context():
            with pytest.raises(Forbidden):
                admin_view()
    
    @patch('rbac.current_user')
    def test_seller_required_hierarchy(self, mock_user, flask_app):
        """Test seller_required logic: admin and seller can access, customer cannot"""
        from Development.rbac import seller_required
        
        @seller_required
        def seller_view():
            return "Seller Area"

        with flask_app.test_request_context():
            # Case 1: Seller accesses Seller View -> Pass
            mock_user.role = 'seller'
            mock_user.is_authenticated = True
            assert seller_view() == "Seller Area"

            # Case 2: Admin accesses Seller View -> Pass (Hierarchy check)
            mock_user.role = 'admin'
            assert seller_view() == "Seller Area"

            # Case 3: Customer accesses Seller View -> Fail
            mock_user.role = 'customer'
            with pytest.raises(Forbidden):
                seller_view()
    
    @patch('rbac.current_user')
    def test_customer_required_hierarchy(self, mock_user, flask_app):
        """Test customer_required logic: admin and customer can access, seller cannot"""
        from Development.rbac import customer_required
        
        @customer_required
        def customer_view():
            return "Customer Area"

        with flask_app.test_request_context():
            # Case 1: Customer -> Pass
            mock_user.role = 'customer'
            mock_user.is_authenticated = True
            assert customer_view() == "Customer Area"
            
            # Case 2: Seller -> Fail
            mock_user.role = 'seller'
            with pytest.raises(Forbidden):
                customer_view()
    
    @patch('rbac.current_user')
    def test_permission_required(self, mock_user, flask_app):
        """Test permission_required decorator"""
        from rbac import permission_required
        
        mock_user.is_authenticated = True
        mock_user.role = 'seller'
        
        @permission_required('manage_inventory')
        def inventory_view():
            return "Inventory"

        @permission_required('manage_sellers')
        def admin_view():
            return "Sellers"

        with flask_app.test_request_context():
            # Seller has 'manage_inventory' -> Pass
            assert inventory_view() == "Inventory"
            
            # Seller does NOT have 'manage_sellers' -> Fail
            with pytest.raises(Forbidden):
                admin_view()
    
    @patch('rbac.current_user')
    def test_unauthenticated_redirect(self, mock_user, flask_app):
        """Test that unauthenticated users are redirected to login for all decorators"""
        from Development.rbac import role_required, admin_required, seller_required, customer_required, permission_required
        
        mock_user.is_authenticated = False
        
        # Create dummy wrapped functions
        wrapped_funcs = [
            role_required('admin')(lambda: 'ok'),
            admin_required(lambda: 'ok'),
            seller_required(lambda: 'ok'),
            customer_required(lambda: 'ok'),
            permission_required('any_perm')(lambda: 'ok')
        ]
        
        with flask_app.test_request_context():
            for func in wrapped_funcs:
                response = func()
                # Assert 302 Redirect
                assert response.status_code == 302, f"Expected 302 redirect, got {response.status_code}"
                # Assert redirect to login page
                location = response.headers.get('Location', '')
                assert '/login' in location or '/auth/login' in location, \
                    f"Expected redirect to login, got: {location}"


# =====================================================
# Subtask: task_3_3_rbac_intro
# Description: Module-to-role mapping documentation and helper functions
# Files Changed: Development/module_mapping.py (MODULE_ROLE_MAPPING, get_modules_for_role, get_role_for_module)
# =====================================================

@pytest.mark.unit
class TestModuleMapping:
    """Test module-to-role mapping functionality"""

    def test_module_mapping_structure(self):
        """Test that MODULE_ROLE_MAPPING has expected structure"""
        from Development.module_mapping import MODULE_ROLE_MAPPING

        assert 'admin' in MODULE_ROLE_MAPPING
        assert 'seller' in MODULE_ROLE_MAPPING
        assert 'customer' in MODULE_ROLE_MAPPING
        assert 'product' in MODULE_ROLE_MAPPING
        assert 'cart' in MODULE_ROLE_MAPPING
        assert 'checkout' in MODULE_ROLE_MAPPING
        assert 'order' in MODULE_ROLE_MAPPING
        assert 'payment' in MODULE_ROLE_MAPPING

    def test_module_mapping_admin(self):
        """Test admin module mapping"""
        from Development.module_mapping import MODULE_ROLE_MAPPING

        admin_module = MODULE_ROLE_MAPPING['admin']
        assert admin_module['required_role'] == 'admin'
        assert 'blueprint' in admin_module
        assert 'routes' in admin_module
        assert 'permissions' in admin_module
        assert 'manage_sellers' in admin_module['permissions']

    def test_module_mapping_seller(self):
        """Test seller module mapping"""
        from Development.module_mapping import MODULE_ROLE_MAPPING

        seller_module = MODULE_ROLE_MAPPING['seller']
        assert seller_module['required_role'] == 'seller'
        assert 'allowed_roles' in seller_module
        assert 'admin' in seller_module['allowed_roles']
        assert 'seller' in seller_module['allowed_roles']
        assert 'manage_products' in seller_module['permissions']

    def test_module_mapping_customer(self):
        """Test customer module mapping"""
        from Development.module_mapping import MODULE_ROLE_MAPPING

        customer_module = MODULE_ROLE_MAPPING['customer']
        assert customer_module['required_role'] == 'customer'
        assert 'allowed_roles' in customer_module
        assert 'admin' in customer_module['allowed_roles']
        assert 'customer' in customer_module['allowed_roles']
        assert 'manage_cart' in customer_module['permissions']

    def test_get_modules_for_role_admin(self):
        """Test get_modules_for_role for admin (should have access to all)"""
        from Development.module_mapping import get_modules_for_role

        modules = get_modules_for_role('admin')
        assert 'admin' in modules
        assert 'seller' in modules
        assert 'customer' in modules
        assert 'product' in modules
        assert 'cart' in modules
        assert 'checkout' in modules
        assert 'order' in modules
        assert 'payment' in modules

    def test_get_modules_for_role_seller(self):
        """Test get_modules_for_role for seller"""
        from Development.module_mapping import get_modules_for_role

        modules = get_modules_for_role('seller')
        assert 'seller' in modules
        assert 'product' in modules  # Public module
        assert 'admin' not in modules  # Seller cannot access admin module
        assert 'customer' not in modules  # Seller cannot access customer module

    def test_get_modules_for_role_customer(self):
        """Test get_modules_for_role for customer"""
        from Development.module_mapping import get_modules_for_role

        modules = get_modules_for_role('customer')
        assert 'customer' in modules
        assert 'product' in modules  # Public module
        assert 'cart' in modules
        assert 'checkout' in modules
        assert 'payment' in modules
        assert 'admin' not in modules  # Customer cannot access admin module
        assert 'seller' not in modules  # Customer cannot access seller module

    def test_get_role_for_module(self):
        """Test get_role_for_module function"""
        from Development.module_mapping import get_role_for_module

        admin_role_info = get_role_for_module('admin')
        assert admin_role_info['required_role'] == 'admin'

        seller_role_info = get_role_for_module('seller')
        assert seller_role_info['required_role'] == 'seller'
        assert 'admin' in seller_role_info['allowed_roles']

        product_role_info = get_role_for_module('product')
        assert product_role_info['required_role'] is None  # Public module

    def test_get_role_for_module_invalid(self):
        """Test get_role_for_module with invalid module"""
        from Development.module_mapping import get_role_for_module

        result = get_role_for_module('invalid_module')
        assert result is None
