# E-Commerce Web Application — Internship Project

**Tech Stack:** Python, Flask, Jinja2, MySQL  
**Roles:** Admin, Seller (Store Staff), Customer  
**Modules:** Product, Category, Inventory, Cart, Order, Payment

## Project Overview

This is a comprehensive 15-task e-commerce web application project designed for learning and internship purposes. The project is divided into 3 phases, building from system design to full implementation.

## Project Structure

The project uses a flat structure with all application code in `Development/` and all testing code in `Testing/`:

```
ecommerce_project_updated/
├── Development/                    # All application code
│   ├── app.py                     # Main Flask application
│   ├── utils.py                   # Utility functions
│   ├── decorators.py              # Role-based decorators
│   ├── rbac.py                    # RBAC implementation
│   ├── setup_database.py          # Database setup script
│   ├── blueprints/                # Flask blueprints
│   │   ├── auth.py               # Authentication
│   │   ├── admin.py              # Admin dashboard
│   │   ├── seller.py             # Seller dashboard
│   │   ├── customer.py           # Customer dashboard
│   │   ├── product.py            # Product listing
│   │   ├── cart.py               # Cart management
│   │   ├── checkout.py           # Checkout flow
│   │   ├── order.py              # Order management
│   │   └── payment.py            # Payment handling
│   ├── models/                    # Data models
│   │   └── user.py               # User model
│   ├── database/                  # Database files
│   │   ├── schema.sql            # Database schema
│   │   ├── seed_data.sql         # Seed data
│   │   └── test_database_validation.sql
│   ├── templates/                 # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/                 # Authentication templates
│   │   ├── admin/                # Admin templates
│   │   ├── seller/               # Seller templates
│   │   ├── customer/             # Customer templates
│   │   ├── product/              # Product templates
│   │   ├── cart/                 # Cart templates
│   │   ├── checkout/             # Checkout templates
│   │   ├── order/                # Order templates
│   │   ├── payment/              # Payment templates
│   │   └── errors/               # Error pages
│   ├── static/                    # Static assets
│   │   └── css/
│   │       └── style.css
│   └── tests/                     # Shared test fixtures
│       ├── conftest.py
│       └── fixtures/
│
├── Testing/                       # All testing infrastructure
│   ├── check_test.py             # Test runner (single task)
│   ├── run_all_tests.py          # Test runner (all tasks)
│   ├── test_configs/             # Test configurations
│   │   ├── task_01.json
│   │   ├── task_02.json
│   │   └── ... (task_03.json through task_15.json)
│   ├── tests/                    # All test files
│   │   ├── test_database_schema.py
│   │   ├── test_rbac.py
│   │   ├── test_auth_ui.py
│   │   ├── test_task_5.py
│   │   ├── test_task_6.py
│   │   └── ... (all test files)
│   └── results/                  # Test result HTML reports
│       ├── task_02_result.html
│       ├── task_03_result.html
│       └── ... (all result files)
│
├── commit_readme.md              # Commit history documentation
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── pytest.ini                   # Pytest configuration
└── README.md                    # This file
```

## Phase Breakdown

### 🔷 PHASE 1 — SYSTEM UNDERSTANDING & DESIGN
**Goal:** Understand requirements, finalize data model, UI flow & access control.

#### Task 1: Identify Roles & Features
- Admin, Seller, Customer roles
- Feature mapping per role
- Documentation and requirements
##### Create Folder Structure 
**File** `file_structure.sh`

#### Task 2: Database Design
- Entity identification (Users, Products, Categories, Orders, Payments, etc.)
- Relationship mapping
- Normalization (3NF)
- ER Diagram
- MySQL schema creation
- **Files:** `Development/database/schema.sql`, `Development/database/seed_data.sql`

#### Task 3: Authorization Design (RBAC)
- Role & permission mapping
- Route access control
- Module-to-role mapping
- **Files:** `Development/rbac.py`, `Development/decorators.py`

#### Task 4: UI Wireframes
- Login & registration pages
- Admin/Seller/Customer dashboards
- Product pages
- Cart & checkout flow
- **Files:** `Development/templates/` (base templates and auth pages)

### 🔷 PHASE 2 — CORE SYSTEM (AUTH + DASHBOARDS)
**Goal:** Build authentication, authorization, and basic dashboards.

#### Task 5: Application Setup
- Flask project structure (MVC pattern)
- MySQL connection & configuration
- Environment setup (.env support)
- Base templates (navbar, footer)
- Blueprint structure
- User model with password hashing
- **Files:** `Development/app.py`, `Development/models/user.py`, `Development/utils.py`

#### Task 6: Login & Session Management
- Login/registration forms
- Password hashing (Werkzeug)
- Flask-Login integration
- Session handling
- **Files:** `Development/blueprints/auth.py`, `Development/templates/auth/`

#### Task 7: Role-Based Access Control
- Role decorators (@admin_required, @seller_required, @customer_required)
- Protected routes
- Unauthorized access handling (403 pages)
- **Files:** `Development/decorators.py`, `Development/templates/errors/403.html`

#### Task 8: Admin Dashboard
- Seller management (CRUD)
- Category management (CRUD)
- Order overview
- Dashboard statistics
- **Files:** `Development/blueprints/admin.py`, `Development/templates/admin/`

#### Task 9: Seller Dashboard
- Product CRUD operations
- Inventory management
- Order management
- Sales dashboard
- **Files:** `Development/blueprints/seller.py`, `Development/templates/seller/`

#### Task 10: Customer Dashboard
- Profile page
- Order history
- Address management
- **Files:** `Development/blueprints/customer.py`, `Development/templates/customer/`

### 🔷 PHASE 3 — BUSINESS FEATURES
**Goal:** Implement core e-commerce workflows.

#### Task 11: Product Listing & Search
- Product listing with pagination
- Category filtering
- Search functionality
- Product details page
- **Files:** `Development/blueprints/product.py`, `Development/templates/product/`

#### Task 12: Cart Management
- Add/update/remove items
- Session-based cart
- Cart summary
- **Files:** `Development/blueprints/cart.py`, `Development/templates/cart/`

#### Task 13: Checkout Flow
- Address management
- Order review
- Price calculation
- Order placement
- **Files:** `Development/blueprints/checkout.py`, `Development/templates/checkout/`

#### Task 14: Order Management
- Order creation
- Status lifecycle (Placed → Confirmed → Packed → Shipped → Delivered)
- Order views per role
- **Files:** `Development/blueprints/order.py`, `Development/templates/order/`

#### Task 15: Payment Handling
- Payment table design
- Mock payment gateway
- Payment processing
- Invoice generation
- **Files:** `Development/blueprints/payment.py`, `Development/templates/payment/`

## Getting Started

### Prerequisites
- Python 3.9+
- MySQL 5.7+ or 8.0+
- pip

### Installation

1. **Clone the repository** (if applicable)

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DB=ecommerce_db
```

5. **Set up database:**
```bash
python Development/setup_database.py
```

6. **Run the application:**
```bash
python Development/app.py
```

The application will be available at `http://localhost:5001` (port 5000 may be used by macOS AirPlay).

## Running Tests

### Run All Tests
```bash
source venv/bin/activate
./venv/bin/python Testing/run_all_tests.py
```

This will:
- Run all test cases for tasks 1-15
- Generate HTML reports in `Testing/results/`
- Show summary of passed/failed tests

### Run Tests for a Specific Task
```bash
source venv/bin/activate
./venv/bin/python Testing/check_test.py <task_id>
```

Example:
```bash
./venv/bin/python Testing/check_test.py 5
```

### Run Tests with Optional Tests
```bash
./venv/bin/python Testing/check_test.py 5 --optional
```

### List All Available Tasks
```bash
./venv/bin/python Testing/check_test.py --list
```

### View Test Results
Test results are saved as HTML files in `Testing/results/`:
- `task_02_result.html` through `task_15_result.html`
- Open these files in a browser to view detailed test results

## Role Features

### Admin
- Login & logout
- Create/manage sellers
- Create categories & subcategories
- View all products & orders
- Manage platform settings
- View sales reports

### Seller / Store Staff
- Login
- Add/update products
- Manage inventory (stock)
- View received orders
- Update order status (Packed, Shipped)

### Customer
- Register & login
- Browse products & categories
- Add products to cart
- Place orders
- View order history
- Manage addresses

## Development Guidelines

- Each task is independently testable
- Tasks build upon previous ones
- Follow MVC architecture
- Use Flask blueprints for organization
- Implement proper error handling
- Include test cases for each task
- All code follows flat structure (no PHASE_/PART_/TASK_ folders)

## Testing Structure

- **Test Configurations:** `Testing/test_configs/task_XX.json` - Define mandatory and optional tests
- **Test Files:** `Testing/tests/test_*.py` - All test implementations
- **Test Runner:** `Testing/check_test.py` - Run tests for individual tasks
- **Test Runner (All):** `Testing/run_all_tests.py` - Run all tests and generate reports
- **Test Results:** `Testing/results/task_XX_result.html` - HTML test reports

## Project Commits

See `commit_readme.md` for detailed commit history and files to commit for each task (1-15).

## License


