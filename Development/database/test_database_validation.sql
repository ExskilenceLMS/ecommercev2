-- SQL-based validation tests for Task 2: Database Design
-- These queries can be run directly in MySQL to validate database structure

-- ============================================
-- 1. DATABASE EXISTENCE VALIDATION
-- ============================================

-- Check if database exists
SELECT 
    SCHEMA_NAME as 'Database Name',
    DEFAULT_CHARACTER_SET_NAME as 'Character Set',
    DEFAULT_COLLATION_NAME as 'Collation'
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME = DATABASE();

-- Expected: Should return 1 row with database name, utf8mb4 character set

-- ============================================
-- 2. TABLE EXISTENCE VALIDATION
-- ============================================

-- Check all tables exist
SELECT 
    table_name as 'Table Name',
    table_rows as 'Row Count',
    table_type as 'Type'
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Expected: Should return 11 tables:
-- addresses, cart, cart_items, categories, inventory, order_items, orders, payments, products, sellers, users

-- Count total tables
SELECT COUNT(*) as 'Total Tables'
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_type = 'BASE TABLE';

-- Expected: Should return 11

-- ============================================
-- 3. USERS TABLE VALIDATION
-- ============================================

-- Check users table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_DEFAULT as 'Default',
    COLUMN_KEY as 'Key',
    EXTRA as 'Extra'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'users'
ORDER BY ORDINAL_POSITION;

-- Expected columns: id, email, password_hash, role, first_name, last_name, phone, is_active, created_at, updated_at

-- Check users table indexes
SELECT 
    INDEX_NAME as 'Index Name',
    COLUMN_NAME as 'Column',
    NON_UNIQUE as 'Non-Unique'
FROM information_schema.statistics
WHERE table_schema = DATABASE() 
AND table_name = 'users'
ORDER BY INDEX_NAME, SEQ_IN_INDEX;

-- Expected: PRIMARY on id, INDEX on email, INDEX on role

-- Check users table constraints
SELECT 
    CONSTRAINT_NAME as 'Constraint',
    CONSTRAINT_TYPE as 'Type'
FROM information_schema.table_constraints
WHERE table_schema = DATABASE() 
AND table_name = 'users';

-- Expected: PRIMARY KEY, UNIQUE on email

-- ============================================
-- 4. SELLERS TABLE VALIDATION
-- ============================================

-- Check sellers table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_KEY as 'Key'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'sellers'
ORDER BY ORDINAL_POSITION;

-- Check sellers foreign key to users
SELECT 
    CONSTRAINT_NAME as 'FK Name',
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table',
    REFERENCED_COLUMN_NAME as 'References Column'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'sellers'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: user_id -> users.id

-- ============================================
-- 5. CATEGORIES TABLE VALIDATION
-- ============================================

-- Check categories table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'categories'
ORDER BY ORDINAL_POSITION;

-- Check self-referential foreign key
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table',
    REFERENCED_COLUMN_NAME as 'References Column'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'categories'
AND column_name = 'parent_id'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: parent_id -> categories.id

-- ============================================
-- 6. PRODUCTS TABLE VALIDATION
-- ============================================

-- Check products table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_DEFAULT as 'Default'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'products'
ORDER BY ORDINAL_POSITION;

-- Check products foreign keys
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table',
    REFERENCED_COLUMN_NAME as 'References Column'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'products'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: seller_id -> sellers.id, category_id -> categories.id

-- Check products indexes
SELECT 
    INDEX_NAME as 'Index',
    COLUMN_NAME as 'Column'
FROM information_schema.statistics
WHERE table_schema = DATABASE() 
AND table_name = 'products'
AND INDEX_NAME != 'PRIMARY'
ORDER BY INDEX_NAME;

-- Expected: Indexes on seller_id, category_id, sku

-- ============================================
-- 7. INVENTORY TABLE VALIDATION
-- ============================================

-- Check inventory table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_DEFAULT as 'Default'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'inventory'
ORDER BY ORDINAL_POSITION;

-- Check inventory foreign key and unique constraint
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table',
    CONSTRAINT_NAME as 'Constraint'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'inventory'
AND column_name = 'product_id';

-- Expected: product_id -> products.id with UNIQUE constraint

-- ============================================
-- 8. ADDRESSES TABLE VALIDATION
-- ============================================

-- Check addresses table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_DEFAULT as 'Default'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'addresses'
ORDER BY ORDINAL_POSITION;

-- Check addresses foreign key
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'addresses'
AND column_name = 'user_id'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: user_id -> users.id

-- ============================================
-- 9. CART TABLE VALIDATION
-- ============================================

-- Check cart table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'cart'
ORDER BY ORDINAL_POSITION;

-- Check cart foreign key
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'cart'
AND column_name = 'customer_id'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: customer_id -> users.id

-- ============================================
-- 10. CART_ITEMS TABLE VALIDATION
-- ============================================

-- Check cart_items table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_DEFAULT as 'Default'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'cart_items'
ORDER BY ORDINAL_POSITION;

-- Check cart_items foreign keys
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'cart_items'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: cart_id -> cart.id, product_id -> products.id

-- Check unique constraint on (cart_id, product_id)
SELECT 
    CONSTRAINT_NAME as 'Constraint',
    COLUMN_NAME as 'Column'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'cart_items'
AND CONSTRAINT_NAME IN (
    SELECT CONSTRAINT_NAME 
    FROM information_schema.table_constraints 
    WHERE table_schema = DATABASE() 
    AND table_name = 'cart_items' 
    AND constraint_type = 'UNIQUE'
);

-- Expected: UNIQUE constraint on (cart_id, product_id)

-- ============================================
-- 11. ORDERS TABLE VALIDATION
-- ============================================

-- Check orders table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_DEFAULT as 'Default'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'orders'
ORDER BY ORDINAL_POSITION;

-- Check orders foreign keys
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table',
    REFERENCED_COLUMN_NAME as 'References Column'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'orders'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: customer_id -> users.id, seller_id -> sellers.id, shipping_address_id -> addresses.id

-- Check orders status ENUM
SELECT 
    COLUMN_TYPE as 'Status ENUM Values'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'orders' 
AND column_name = 'status';

-- Expected: ENUM('placed','confirmed','packed','shipped','delivered','cancelled')

-- Check orders indexes
SELECT 
    INDEX_NAME as 'Index',
    COLUMN_NAME as 'Column'
FROM information_schema.statistics
WHERE table_schema = DATABASE() 
AND table_name = 'orders'
AND INDEX_NAME != 'PRIMARY'
ORDER BY INDEX_NAME;

-- Expected: Indexes on customer_id, seller_id, status, order_number

-- ============================================
-- 12. ORDER_ITEMS TABLE VALIDATION
-- ============================================

-- Check order_items table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'order_items'
ORDER BY ORDINAL_POSITION;

-- Check order_items foreign keys
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'order_items'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: order_id -> orders.id, product_id -> products.id

-- ============================================
-- 13. PAYMENTS TABLE VALIDATION
-- ============================================

-- Check payments table structure
SELECT 
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_DEFAULT as 'Default'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'payments'
ORDER BY ORDINAL_POSITION;

-- Check payments foreign key
SELECT 
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() 
AND table_name = 'payments'
AND column_name = 'order_id'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected: order_id -> orders.id

-- Check payments ENUMs
SELECT 
    COLUMN_NAME as 'Column',
    COLUMN_TYPE as 'ENUM Values'
FROM information_schema.columns
WHERE table_schema = DATABASE() 
AND table_name = 'payments' 
AND column_name IN ('payment_method', 'status');

-- Expected: 
-- payment_method: ENUM('credit_card','debit_card','paypal','cash_on_delivery')
-- status: ENUM('pending','completed','failed','refunded')

-- Check payments indexes
SELECT 
    INDEX_NAME as 'Index',
    COLUMN_NAME as 'Column'
FROM information_schema.statistics
WHERE table_schema = DATABASE() 
AND table_name = 'payments'
AND INDEX_NAME != 'PRIMARY'
ORDER BY INDEX_NAME;

-- Expected: Indexes on order_id, status, transaction_id

-- ============================================
-- 14. FOREIGN KEY CONSTRAINTS VALIDATION
-- ============================================

-- Check all foreign keys and their delete rules
SELECT 
    kcu.TABLE_NAME as 'Table',
    kcu.COLUMN_NAME as 'Column',
    kcu.REFERENCED_TABLE_NAME as 'References Table',
    kcu.REFERENCED_COLUMN_NAME as 'References Column',
    rc.DELETE_RULE as 'Delete Rule',
    rc.UPDATE_RULE as 'Update Rule'
FROM information_schema.key_column_usage kcu
JOIN information_schema.referential_constraints rc 
    ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
WHERE kcu.table_schema = DATABASE()
AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY kcu.TABLE_NAME, kcu.COLUMN_NAME;

-- Expected: Various CASCADE, RESTRICT, and SET NULL rules based on schema

-- ============================================
-- 15. DATA TYPE VALIDATION
-- ============================================

-- Check DECIMAL columns (prices, amounts)
SELECT 
    TABLE_NAME as 'Table',
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    NUMERIC_PRECISION as 'Precision',
    NUMERIC_SCALE as 'Scale'
FROM information_schema.columns
WHERE table_schema = DATABASE()
AND DATA_TYPE = 'decimal'
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Expected: All price/amount columns should be DECIMAL(10,2)

-- Check TIMESTAMP columns
SELECT 
    TABLE_NAME as 'Table',
    COLUMN_NAME as 'Column',
    DATA_TYPE as 'Type',
    COLUMN_DEFAULT as 'Default',
    EXTRA as 'Extra'
FROM information_schema.columns
WHERE table_schema = DATABASE()
AND COLUMN_NAME IN ('created_at', 'updated_at')
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Expected: created_at with DEFAULT CURRENT_TIMESTAMP, updated_at with ON UPDATE CURRENT_TIMESTAMP

-- ============================================
-- 16. SUMMARY VALIDATION QUERY
-- ============================================

-- Overall database structure summary
SELECT 
    'Tables' as 'Item',
    COUNT(*) as 'Count'
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_type = 'BASE TABLE'
UNION ALL
SELECT 
    'Foreign Keys' as 'Item',
    COUNT(*) as 'Count'
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE()
AND REFERENCED_TABLE_NAME IS NOT NULL
UNION ALL
SELECT 
    'Indexes' as 'Item',
    COUNT(DISTINCT INDEX_NAME) as 'Count'
FROM information_schema.statistics
WHERE table_schema = DATABASE()
UNION ALL
SELECT 
    'Unique Constraints' as 'Item',
    COUNT(*) as 'Count'
FROM information_schema.table_constraints
WHERE table_schema = DATABASE()
AND constraint_type = 'UNIQUE';

-- Expected:
-- Tables: 11
-- Foreign Keys: Multiple (check based on schema)
-- Indexes: Multiple (check based on schema)
-- Unique Constraints: Multiple (email, user_id in sellers, sku, etc.)

