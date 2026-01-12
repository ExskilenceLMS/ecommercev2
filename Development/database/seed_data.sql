-- Seed Data for E-Commerce Database

-- Insert default categories
INSERT INTO categories (name, parent_id, description, slug) VALUES
('Electronics', NULL, 'Electronic devices and gadgets', 'electronics'),
('Clothing', NULL, 'Apparel and fashion items', 'clothing'),
('Home & Garden', NULL, 'Home improvement and garden supplies', 'home-garden'),
('Books', NULL, 'Books and publications', 'books'),
('Sports', NULL, 'Sports and outdoor equipment', 'sports'),
('Laptops', 1, 'Laptop computers', 'laptops'),
('Smartphones', 1, 'Mobile phones', 'smartphones'),
('Men\'s Clothing', 2, 'Clothing for men', 'mens-clothing'),
('Women\'s Clothing', 2, 'Clothing for women', 'womens-clothing'),
('Fiction', 4, 'Fiction books', 'fiction'),
('Non-Fiction', 4, 'Non-fiction books', 'non-fiction');

-- Insert admin user (password: admin123)
INSERT INTO users (email, password_hash, role, first_name, last_name, is_active) VALUES
('admin@ecommerce.com', 'pbkdf2:sha256:600000$...', 'admin', 'Admin', 'User', TRUE);

-- Insert sample seller user (password: seller123)
INSERT INTO users (email, password_hash, role, first_name, last_name, phone, is_active) VALUES
('seller1@store.com', 'pbkdf2:sha256:600000$...', 'seller', 'John', 'Seller', '1234567890', TRUE),
('seller2@store.com', 'pbkdf2:sha256:600000$...', 'seller', 'Jane', 'Merchant', '0987654321', TRUE);

-- Insert seller details
INSERT INTO sellers (user_id, store_name, store_description, contact_email, contact_phone) VALUES
(2, 'Tech Store', 'Best electronics and gadgets', 'seller1@store.com', '1234567890'),
(3, 'Fashion Hub', 'Trendy clothing and accessories', 'seller2@store.com', '0987654321');

-- Insert sample customer user (password: customer123)
INSERT INTO users (email, password_hash, role, first_name, last_name, phone, is_active) VALUES
('customer1@email.com', 'pbkdf2:sha256:600000$...', 'customer', 'Alice', 'Customer', '1111111111', TRUE),
('customer2@email.com', 'pbkdf2:sha256:600000$...', 'customer', 'Bob', 'Buyer', '2222222222', TRUE);

-- Insert sample addresses
INSERT INTO addresses (user_id, address_line1, city, state, postal_code, country, is_default) VALUES
(4, '123 Main St', 'New York', 'NY', '10001', 'USA', TRUE),
(5, '456 Oak Ave', 'Los Angeles', 'CA', '90001', 'USA', TRUE);

-- Note: Actual password hashes should be generated using Werkzeug's generate_password_hash()
-- Example: from werkzeug.security import generate_password_hash
-- generate_password_hash('admin123')

